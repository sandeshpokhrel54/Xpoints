import random
from signal import NSIG

Team1 = [0.02,0.02,0.03,0.04,0.04,0.05,0.06,0.07,0.09,0.10,0.12,0.13,0.76] # home team
team1XG  = sum(Team1)
# print(team1XG)

Team2 = [0.01,0.02,0.02,0.02,0.03,0.05,0.05,0.05,0.06,0.22,0.30,0.43,0.48,0.63] #away team
team2XG  = sum(Team2)
# print(team2XG)


def scorecount(team):

    goals = 0
    for i in team:
        rand = random.randint(1,1000)/1000

        if rand < i:
            goals +=1

    return goals


N_SIMULATIONS  = 100000 # number of simulations
def play(N_SIMULATIONS):

    homewins = 0
    awaywins = 0
    draws = 0

    for i in range(N_SIMULATIONS):
        goalsHome = scorecount(Team1)
        goalsAway = scorecount(Team2)
        # print(goalsHome, goalsAway)

        if(goalsHome>goalsAway):
            homewins = homewins + 1
        elif(goalsHome==goalsAway):
            draws = draws + 1
        else:
            awaywins = awaywins + 1

    return homewins, draws, awaywins


homewins,draws,awaywins = play(N_SIMULATIONS)

shots_team_1 = len(Team1)
shots_team_2 = len(Team2)
meanTeam1 = team1XG/shots_team_1
meanTeam2 = team2XG/shots_team_2

sdteam1 = round((sum((i-meanTeam1)**2 for i in Team1)/shots_team_1)**0.5,3)
sdteam2 = round((sum((i-meanTeam2)**2 for i in Team2)/shots_team_2)**0.5,3)

print(homewins/N_SIMULATIONS,draws/N_SIMULATIONS,awaywins/N_SIMULATIONS)
home_win_rate = homewins/N_SIMULATIONS
draw_rate = draws/N_SIMULATIONS
away_win_rate = awaywins/N_SIMULATIONS

home_expected_points = round(home_win_rate*3 + draw_rate,3) #homewinpercentage * 3 points + drawpercentage * 1 point = expected points
away_expected_points = round(away_win_rate*3 + draw_rate,3) #awaywinpercentage * 3 points + drawpercentage * 1 point = expected points
print(f'Home Team: {team1XG} +- {sdteam1}, Away Team:{team2XG} +- {sdteam2}')

print(f'Home Team: {home_expected_points}, Away Team:{away_expected_points}')

#calculate expected points after standard deviation
