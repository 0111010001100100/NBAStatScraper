import pandas as pd 
import sys 

sys.path.append('../../')
import teams
import db


def prep_teams(team):
    '''
    Prepares the scraped data to be added to the database. Specifically gets data from the 2002 season to present.
        Parameters: 
            team (string): The 3 letter abbreviation of a team (e.g. 'BOS')
        Returns:
            A Pandas dataframe containing the per game steam stats prepared for the database. 
    '''
    df = teams.get_team_stats_per_game(team)
    df = df.drop(['Lg', 'MP'], axis=1)
    df.columns = ['year', 'teamId', 'wins', 'losses', 'finish', 'avgAge', 'avgHeight', 'avgWeight', 
                  'gamesPlayed', 'fg', 'fga', 'fgp', 'three', 'threeA', 'threeP', 'two', 'twoA', 'twoP',
                  'ft', 'fta', 'ftp', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
    df['year'] = df['year'].apply(db.prep_year)
    return df[df.year > 2001]
    