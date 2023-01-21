# Xpoints
Exploring *XGphilosophy*, some basic implementations using data from understat.com's API.  
**XG** - expected goals (The number of goals you would expect a team to score based on the chances they created.)  
**XP** - expected points (The number of points a team is expected to get based on their chances being converted to goals)  

Test it on your desired team(EPL, La Liga, Ligue 1, Bundesliga, Seria A, RFPL ):
- Clone the repo  
    `git clone https://github.com/sandeshpokhrel54/Xpoints.git  `  
    
- install requirements  
    `cd Xpoints`  
    `pip install -r requirements.txt`    
    
- Run fetch_main.py  
    - `python fetch_main.py --t "Chelsea" --s "2022" `  

You also get a plot at the end, of the latest fixture the team played.  
![Chelsea vs Manchester United](https://github.com/sandeshpokhrel54/Xpoints/blob/main/Xg.png)  

To get the plots of all the matches of the latest gameweek; latest_gw.py file can be used.


TODO:
- add scoreline and xg score in plot
- maybe a bot to tweet xpoints after each game

