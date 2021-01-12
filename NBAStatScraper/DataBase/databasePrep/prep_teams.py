import pandas as pd 
import sys 

sys.path.append('../../')
import teams

# Function to prepare the team stats table 
# Does it for the 2001-02 to 2019-20 seasons
# Pelicans, Hornets, Nets have strange naming, may need to do someething with it
def prep_teams(team):
    df = teams.get_team_stats_per_game(team)
    df = df.drop(['Lg', 'MP'], axis=1)
    df.columns = ['year', 'teamId', 'wins', 'losses', 'finish', 'avgAge', 'avgHeight', 'avgWeight', 
                  'gamesPlayed', 'fg', 'fga', 'fgp', 'three', 'threeA', 'threeP', 'two', 'twoA', 'twoP',
                  'ft', 'fta', 'ftp', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
    df['year'] = df['year'].apply(prep_year)
    return df[df.year > 2001]
    
def prep_year(yr):
    return int(yr.split('-')[0]) + 1