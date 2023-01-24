import asyncio
import platform

import aiohttp

from understat import Understat
from xpoints import calcXPoints

import argparse
import sys
from pitch import plotShots




#prettify
#save all-plots as png;
# tweet?


async def get_table(league='epl', season="2022"):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_table(league, season)
        return data


async def team_results_latest(team_name="Chelsea", season="2022"):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_team_results(team_name, season)
        return data

async def get_match_shots(match_id):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_match_shots(match_id)
        return data

if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    if(platform.system()=='Windows'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.set_event_loop(loop)
    # team_stats = loop.run_until_complete(get_stats("epl", "2022", "Chelsea"))

    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--season", default="2022", help="season")
    # ap.add_argument("-t", "--team", default="Chelsea", help="team name")
    ap.add_argument("-l", "--league", default="epl", help='League name')
    args = vars(ap.parse_args())

    table = loop.run_until_complete(get_table(args['league'], args['season']))

    # print(table)
    team_names = [team[0] for team in table]
    # print(team_names[1:])


    # results = loop.run_until_complete(team_results_latest(team_name=args['team'], season=args['season']))
    team_list = team_names[1:]
    season = '2022'
    league = 'epl' 

    games =[]
    for team in team_list:


        results = loop.run_until_complete(team_results_latest(team_name=team, season=season))

        latest_results = results[-1]

        scoreline = 'Score: ' +latest_results['goals']['h'] + ' - ' + latest_results['goals']['a']
        latest_game =  latest_results['h']['title'] + ' vs ' + latest_results['a']['title']
        xgs = 'xGs: ' + latest_results['xG']['h'] + ' - ' + latest_results['xG']['a']
        print(latest_game)
        match_id = latest_results['id']
        print(match_id)

        if latest_game in games:
            continue
        else:
            games.append(latest_game)
    
        all_shots_latest_game = loop.run_until_complete(get_match_shots(match_id=match_id))
        # print(all_shots_latest_game)

        home_shots = []
        away_shots = []
        for  shot in all_shots_latest_game['h']:
            home_shots.append([shot['xG'], shot['X'], shot['Y'], shot['result']])
            # print("Home shots: ", shot['xG'])
        for shot in all_shots_latest_game['a']:
            away_shots.append([shot['xG'], shot['X'], shot['Y'], shot['result']])


        home_xg = [home_shot[0] for home_shot in home_shots]
        away_xg = [away_shot[0] for away_shot in away_shots]

        #converting values to float
        flo_value_0 = [float(i) for i in home_xg] 
        flo_value_1 = [float(i) for i in away_xg]

        #calculate xps and deviation of xgs
        homexp, awayxp, homesd, awaysd = calcXPoints(flo_value_0, flo_value_1)
        latest_shots = [home_shots, away_shots]
        print(homexp, awayxp, homesd, awaysd)
        # print(latest_shots)

        hxp = str(homexp)
        axp = str(awayxp)
        xps = 'xPs: ' + hxp + ' - ' + axp
        # #plot shots of latest game
        matchTitle = latest_game + '\n' + scoreline + '\n' + xgs + '\n' +xps
        fig,ax = plotShots(latest_shots, matchTitle)