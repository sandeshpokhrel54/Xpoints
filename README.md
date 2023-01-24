# Xpoints
Exploring *XGphilosophy*, some basic implementations using data from understat.com's API.  
**XG** - expected goals (The number of goals you would expect a team to score based on the chances they created.)  
**XP** - expected points (The number of points a team is expected to get based on their chances being converted to goals)  

### Get Xpoints for all games of the season
Test it on your desired team(EPL, La Liga, Ligue 1, Bundesliga, Seria A, RFPL ):  
- Clone the repo  
    `git clone https://github.com/sandeshpokhrel54/Xpoints.git  `  
    
- install requirements  
    `cd Xpoints`  
    `pip install -r requirements.txt`    
    
- Run fetch_main.py  
    - `python fetch_main.py --t "Chelsea" --s "2022" `  

You also get a plot at the end, of the latest fixture the team played.  
![Liverpool vs Chelsea](https://github.com/sandeshpokhrel54/Xpoints/blob/main/Xg1.png) 


### Get plots of the latest games of any league  
- Clone the repo  
    `git clone https://github.com/sandeshpokhrel54/Xpoints.git  `  
    
- install requirements  
    `cd Xpoints`  
    `pip install -r requirements.txt`    
    
- Run fetch_main.py  
    - `python latest_gw.py --l "la liga" --s "2022" `  
 
 One by one plot of the latest games played by each team in the league of the given season in matplotlib.  
![One of the fixtures of last week(epl)](https://github.com/sandeshpokhrel54/Xpoints/blob/main/xPs.png)  
  
TODO:  
- maybe a bot to tweet xpoints after each game

