import random
import numpy.random as npr

N_SIMULATIONS  = 100000 # number of simulations
PRECISION = 1000

def scorecount(team):

    goals = 0
    for i in team:
        rand = random.randint(1,PRECISION)/PRECISION

        if rand < i:
            goals +=1

    return goals


def play(Team1, Team2, N_SIMULATIONS=1000):

    homewins = 0
    awaywins = 0
    draws = 0

    home_goals_count = {}
    away_goals_count = {}

    for i in range(N_SIMULATIONS):
        goalsHome = scorecount(Team1)
        goalsAway = scorecount(Team2)
        # print(goalsHome, goalsAway)
        home_goals_count.update({goalsHome:home_goals_count.get(goalsHome,0)+1})
        away_goals_count.update({goalsAway:away_goals_count.get(goalsAway,0)+1})

        if(goalsHome>goalsAway):
            homewins = homewins + 1
        elif(goalsHome==goalsAway):
            draws = draws + 1
        else:
            awaywins = awaywins + 1

    return homewins, draws, awaywins,home_goals_count, away_goals_count

#standard deviation on the quality of chances each team creates
#another useful factor might be the standard deviation of the goals scored by each team which is
#taken into account in the xG model
def deviation(Team1, Team2):
    shots_team_1 = len(Team1)
    shots_team_2 = len(Team2)
    meanTeam1 = sum(Team1)/shots_team_1
    meanTeam2 = sum(Team2)/shots_team_2

    sdteam1 = round((sum((i-meanTeam1)**2 for i in Team1)/shots_team_1)**0.5,3)
    sdteam2 = round((sum((i-meanTeam2)**2 for i in Team2)/shots_team_2)**0.5,3)
    return sdteam1,sdteam2

def deviationGoals(team1_goal_counts, team2_goal_counts):
    #for x ranging from 0 to number of shots
    #find the probability of scoring x goals
    #and calculate standard deviation
    team1_goal_counts_prob = {k:v/N_SIMULATIONS for k,v in team1_goal_counts.items()}
    team2_goal_counts_prob = {k:v/N_SIMULATIONS for k,v in team2_goal_counts.items()}

    #now that the probailites are known
    #find mean and standard deviation of goals scored
    meanTeam1 = sum([k*v for k,v in team1_goal_counts_prob.items()])
    meanTeam2 = sum([k*v for k,v in team2_goal_counts_prob.items()])
    sdteam1 = round((sum((k-meanTeam1)**2*v for k,v in team1_goal_counts_prob.items()))**0.5,3)
    sdteam2 = round((sum((k-meanTeam2)**2*v for k,v in team2_goal_counts_prob.items()))**0.5,3)

    # print(team1_goal_counts_prob, team2_goal_counts_prob)
    return sdteam1, sdteam2


def xpoints(Team1, Team2,N_SIMULATIONS=1000):
    
    homewins, draws, awaywins, home_goals_count, away_goals_count  = play(Team1, Team2,N_SIMULATIONS)
    
    # print(home_goals_count, away_goals_count)
    # print("homeWins: ", homewins)
    # print("draws:", draws)
    # print("awayWins:", awaywins)
    # print(homewins/N_SIMULATIONS,draws/N_SIMULATIONS,awaywins/N_SIMULATIONS)
    
    team1dev, team2dev = deviationGoals(home_goals_count, away_goals_count)
    
    home_win_rate = homewins/N_SIMULATIONS
    draw_rate = draws/N_SIMULATIONS
    away_win_rate = awaywins/N_SIMULATIONS
    xpointsHome = round(home_win_rate*3 + draw_rate,3) #homewinpercentage * 3 points + drawpercentage * 1 point = expected points
    xpointsAway = round(away_win_rate*3 + draw_rate,3) #awaywinpercentage * 3 points + drawpercentage * 1 point = expected points
    
    return xpointsHome, xpointsAway, team1dev, team2dev


def calcXPoints(Team1, Team2, N_SIMULATIONS=1000):
    xpointsHome, xpointsAway, team1dev, team2dev = xpoints(Team1, Team2,N_SIMULATIONS)
    # sdteam1,sdteam2 = deviation(Team1, Team2)
    # print(f'Home Team: {sum(Team1)} +- {team1dev}, Away Team:{sum(Team2)} +- {team2dev}')
    # print(f'Home Team: {xpointsHome}, Away Team:{xpointsAway}')
    # print(f'psst Dev team1: {team1dev}, psst Dev team2:{team2dev}')

    return xpointsHome, xpointsAway, team1dev, team2dev


def samplefromPoi(lam, N_SIMULATIONS=1000):
    samples = npr.poisson(lam, N_SIMULATIONS)
    return samples

#test
if __name__== '__main__':

    #TEST DATA
    Team1 = [0.02,0.02,0.03,0.04,0.04,0.05,0.06,0.07,0.09,0.10,0.12,0.13,0.76] # home team
    team1XG  = sum(Team1)
    Team2 = [0.01,0.02,0.02,0.02,0.03,0.05,0.05,0.05,0.06,0.22,0.30,0.43,0.48,0.63] #away team
    team2XG  = sum(Team2)

    team_coin = [0.5,0.5,0.5,0.5]
    coinXG = sum(team_coin)
    team_dice = [0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167,0.167]
    diceXG = sum(team_dice)

    #checking with understats value chelsea vs westham
    chelsea = [0.01, 0.03, 0.02, 0.02, 0.07, 0.10, 0.12, 0.34]
    chelseaXG = sum(chelsea)
    westham = [0.03, 0.08, 0.03, 0.94, 0.33]
    westhamXG = sum(westham)

    #RUN TESTS
    # homexp, awayexp, sdteam1, sdteam2 = calcXPoints(Team1, Team2, N_SIMULATIONS)
    coinxp, dicexp, sdteam1, sdteam2 = calcXPoints(team_coin, team_dice, N_SIMULATIONS)
    print(coinxp, dicexp)

    #to compare understat's xp and the one i calculated
    # chelseaxp, westhamxp, sdteam1, sdteam2 = calcXPoints(chelsea, westham, N_SIMULATIONS)



    #simulation from poission distribution; 
    #seems close enough but the one from shots is better
    testsim = 100000
    team_coin_poi = samplefromPoi(coinXG, testsim)
    team_dice_poi = samplefromPoi(diceXG, testsim)
    # print(team_coin_poi, team_dice_poi)
    coinWins = team_coin_poi > team_dice_poi
    diceWins = team_dice_poi > team_coin_poi
    diceWins = sum(diceWins.astype(int))
    coinWins = sum(coinWins.astype(int))
    Draws = testsim - diceWins - coinWins
    # print(coinWins)
    # print(diceWins)
    # print(Draws)
    coinxp = 3 * coinWins/testsim + 1 * Draws/testsim
    dicexp = 3 * diceWins/testsim + 1 * Draws/testsim
    print(coinxp)
    print(dicexp)


#The sampling of the match scores has been done from Poisson distribution. Is it a fair reflection on match scores if both teams accumulate the same xG values? 
#assuming a case of golden chances and weak chances, the golden chances win out at least in the case of coin with on average 0.1 xp more.
#not exactly same but similar
#the expected points values are far close to each other when win rate are derived from poission distribution rather than game simulation.

#expected goals not added but conditionally added(in cases of chances coming off of rebounds), this is already incorporated in the xg data we collect,
#done by the vendors of data



