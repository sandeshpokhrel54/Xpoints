import asyncio
import platform

import aiohttp

from understat import Understat
from xpoints import calcXPoints

import argparse
import sys
from pitch import plotShots



#get the latest games of all teams, right now looks like fetching all games played and then selecting the last one is the solution; 
#get match xg of all games, but also need the shots if I am to plot
#use poission distribution to simulate match scores or simulate from shots, get xp
#get plots and xps
#tweet?
