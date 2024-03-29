import asyncio
import platform

import aiohttp

from understat import Understat
from xpoints import calcXPoints

import argparse
import sys
from pitch import plotShots

''' league = epl, laliga, etc...
    season = 2021, 2020, etc...
    team = Arsenal, Aston Villa, etc...'''

#league player stats
async def get_stats(league, season, team):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_players(league, season, {"team_title": team})
        return data

#league team stats
async def team_results(team_name="Chelsea", season="2022"):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_team_results(team_name, season)
        return data


#get match shots
async def get_match_shots(match_id):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_match_shots(match_id)
        return data

#parse for my convenience
def get_shots_by_game_dict(results):
    allGames = {} #for game id and shots only
    allGameinfo = {} #for team names, xgs and shots
    for game in results:
        # print(game['h']['title'],game['goals']['h'], game['xG']['h'], game['a']['title'], game['goals']['a'] , game['xG']['a'])
        shots = loop.run_until_complete(get_match_shots(game['id']))
        
        home_shots = []
        away_shots = []
        for  shot in shots['h']:
            home_shots.append([shot['xG'], shot['X'], shot['Y'], shot['result']])
            # print("Home shots: ", shot['xG'])
        for shot in shots['a']:
            away_shots.append([shot['xG'], shot['X'], shot['Y'], shot['result']])
            # print("Away shots: ", shot['xG'])
        
        allGames[game['id']] = [home_shots, away_shots] #dict with key game id and value list of home and away shots
        allGameinfo[game['h']['title'] + " vs " + game['a']['title']] = [game['goals']['h'], game['xG']['h'], game['goals']['a'] , game['xG']['a'],[home_shots, away_shots]]
        # print()
    return allGames, allGameinfo


def parse_all_games(allGames):
   
    for k,v in allGames[1].items(): #allGamesinfo

        values = v[-1] #last element in list is the list of shots home and away shots
        
        latest_game = k
        latest_game_shots = values
        
        home_shots = values[0]
        away_shots = values[1]

        home_xg = [home_shot[0] for home_shot in home_shots]
        away_xg = [away_shot[0] for away_shot in away_shots]
        #converting values to float
        flo_value_0 = [float(i) for i in home_xg] 
        flo_value_1 = [float(i) for i in away_xg]

        #calculate xps and deviation of xgs
        homexp, awayxp, homesd, awaysd = calcXPoints(flo_value_0, flo_value_1)
        print(k)
        print("Home xG: ", v[1]," +- ", homesd, "   Away xG: ", v[3], " +- ", awaysd)
        print("Home xP: ", homexp, "   Away xP: ", awayxp)
        # print(k,homexp, homesd, awayxp, awaysd)
        print()
    return [latest_game,latest_game_shots, homexp, awayxp, homesd, awaysd]

if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    if(platform.system()=='Windows'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.set_event_loop(loop)
    # team_stats = loop.run_until_complete(get_stats("epl", "2022", "Chelsea"))

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--season", default="2022", help="season")
    ap.add_argument("-t", "--team", default="Chelsea", help="team name")
    args = vars(ap.parse_args())
    
    results = loop.run_until_complete(team_results(team_name=args['team'], season=args['season']))
    allGames = get_shots_by_game_dict(results)

    # print(allGames)    
    latest_game, latest_game_shots, homexp, awayxp, homesd, awaysd  = parse_all_games(allGames)
    print(latest_game, latest_game_shots)
    #plot shots of latest game
    fig,ax = plotShots(latest_game_shots, latest_game)

