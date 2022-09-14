import random
import numpy.random as npr

Team1 = [0.02,0.02,0.03,0.04,0.04,0.05,0.06,0.07,0.09,0.10,0.12,0.13,0.76] # home team
team1XG  = sum(Team1)
# print(team1XG)

Team2 = [0.01,0.02,0.02,0.02,0.03,0.05,0.05,0.05,0.06,0.22,0.30,0.43,0.48,0.63] #away team
team2XG  = sum(Team2)
# print(team2XG)

team_coin = [0.5,0.5,0.5,0.5]
coinXG = sum(team_coin)

team_dice = [0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167]
diceXG = sum(team_dice)


#checking with understats value chelsea vs westham
chelsea = [0.01, 0.03, 0.02, 0.02, 0.07, 0.10, 0.12, 0.34]
chelseaXG = sum(chelsea)

westham = [0.03, 0.08, 0.03, 0.94, 0.33]
westhamXG = sum(westham)



N_SIMULATIONS  = 100000 # number of simulations
PRECISION = 1000

def scorecount(team):

    goals = 0
    for i in team:
        rand = random.randint(1,PRECISION)/PRECISION

        if rand < i:
            goals +=1

    return goals



def play(Team1, Team2, N_SIMULATIONS):

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


def xpoints(Team1, Team2,N_SIMULATIONS):
    
    homewins, draws, awaywins = play(Team1, Team2,N_SIMULATIONS)
    
    # print("homeWins: ", homewins)
    # print("draws:", draws)
    # print("awayWins:", awaywins)
    print(homewins/N_SIMULATIONS,draws/N_SIMULATIONS,awaywins/N_SIMULATIONS)

    home_win_rate = homewins/N_SIMULATIONS
    draw_rate = draws/N_SIMULATIONS
    away_win_rate = awaywins/N_SIMULATIONS
    xpointsHome = round(home_win_rate*3 + draw_rate,3) #homewinpercentage * 3 points + drawpercentage * 1 point = expected points
    xpointsAway = round(away_win_rate*3 + draw_rate,3) #awaywinpercentage * 3 points + drawpercentage * 1 point = expected points
    
    return xpointsHome, xpointsAway


#standard deviation on the quality of chances each team creates
#another useful factor might be the standard deviation of the goals scored by each team which is
#taken into account in the xG model
def deviation(Team1, Team2):
    shots_team_1 = len(Team1)
    shots_team_2 = len(Team2)
    meanTeam1 = team1XG/shots_team_1
    meanTeam2 = team2XG/shots_team_2

    sdteam1 = round((sum((i-meanTeam1)**2 for i in Team1)/shots_team_1)**0.5,3)
    sdteam2 = round((sum((i-meanTeam2)**2 for i in Team2)/shots_team_2)**0.5,3)
    return sdteam1,sdteam2

# homewins,draws,awaywins = play(N_SIMULATIONS)

home_expected_points, away_expected_points = xpoints(Team1, Team2, N_SIMULATIONS)
sdteam1, sdteam2 = deviation(Team1, Team2)

print(f'Home Team: {team1XG} +- {sdteam1}, Away Team:{team2XG} +- {sdteam2}')
print(f'Home Team: {home_expected_points}, Away Team:{away_expected_points}')

coinXP, diceXP = xpoints(team_coin, team_dice, N_SIMULATIONS)
sdcoin, sddice = deviation(team_coin, team_dice)
print(f'Coin: {coinXG} +- {sdcoin}, Dice:{diceXG} +- {sddice}')
print(f'Coin: {coinXP}, Dice:{diceXP}')


#to compare understat's xp and the one i calculated
chelseaXP, westhamXP = xpoints(chelsea, westham, N_SIMULATIONS)
sdchelsea, sdwestham = deviation(chelsea, westham)

print(f'Chelsea: {chelseaXG} +- {sdchelsea}, Dice:{westhamXG} +- {sdwestham}')
print(f'Chelsea: {chelseaXP}, Dice:{westhamXP}')
#calculate expected points after standard deviation of number of goals each team can score




