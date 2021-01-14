import pandas as pd 
import sys 

sys.path.append('../../')
sys.path.append('NBAStatScraper/')
import game 

def prep_season_results(team, year):
    df = game.get_team_season_results(team, year)
    df = df.drop(df.columns[df.columns.str.contains('Unnamed',case = False)],axis = 1)
    df = df.drop(columns=['G', 'Date', 'Start (ET)', 'Opponent', 'W', 'L', 'Streak', 'Notes'])
    return df 