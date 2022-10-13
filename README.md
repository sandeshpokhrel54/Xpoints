# Xpoints
Exploring XGphilosophy, some basic implementations using data from understat.com's functions.  
XG - expected goals (The number of goals you would expect a team to score based on the chances they created.)  
XP - expected points (The number of points a team is expected to get based on their chances being converted to goals)  

Test it on your desired team(EPL, La Liga, Ligue 1, Bundesliga, Seria A, RFPL ):
- Clone the repo
- install requirements
- python fetch_main.py --t *team_name* --s *season*
    - Eg. fetch_main.py --t "Chelsea" --s "2022"

TODO:
- currently fetches and calculates for all the games of a particular season; try for latest matchweek of all teams
- maybe a bot to tweet xpoints after each game

