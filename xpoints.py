import random

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


N  = 100000 # number of simulations
def play(N):

    homewins = 0
    awaywins = 0
    draws = 0

    for i in range(N):
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


homewins,draws,awaywins = play(N)

print(homewins/N,draws/N,awaywins/N)

home_expected_points = homewins/N*3 + draws/N #homewinpercentage * 3 points + drawpercentage * 1 point = expected points
away_expected_points = awaywins/N*3 + draws/N #awaywinpercentage * 3 points + drawpercentage * 1 point = expected points
print(home_expected_points, away_expected_points)