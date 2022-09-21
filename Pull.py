import asyncio
import platform

import aiohttp

from understat import Understat


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
async def team_results(team_name, season):
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

if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    if(platform.system()=='Windows'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.set_event_loop(loop)
    # team_stats = loop.run_until_complete(get_stats("epl", "2022", "Chelsea"))
    # for player in team_stats:
    #     print(player['id'], player['player_name'])
    #     print()
    results = loop.run_until_complete(team_results("Chelsea", "2022"))

    # print(results)

    allGames = {}
    for game in results:
        print(game['h']['title'],game['goals']['h'], game['xG']['h'], game['a']['title'], game['goals']['a'] , game['xG']['a'])
        shots = loop.run_until_complete(get_match_shots(game['id']))
        
        home_shots = []
        away_shots = []
        for  shot in shots['h']:
            home_shots.append(shot['xG'])
            print("Home shots: ", shot['xG'])
        for shot in shots['a']:
            away_shots.append(shot['xG'])
            print("Away shots: ", shot['xG'])
        
        allGames[game['id']] = [home_shots, away_shots]
        print(allGames) #xgs of each shot, for each game for home and away team

        print()
