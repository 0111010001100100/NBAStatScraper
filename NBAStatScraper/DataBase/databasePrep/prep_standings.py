import pandas as pd
import sys

sys.path.append('../../')
import standings

def prep_standings(year):
    west = _prep_standings(year, 'W')
    east = _prep_standings(year, 'E')
    return pd.concat([west, east])

def _prep_standings(year, conference):
    df = standings.get_conference_standings(conference, year) 
    df = df.drop('SRS', axis=1)
    df.columns = ['team', 'wins', 'losses', 'ratio', 'gamesBack', 'ppg', 'oppg']
    df = df.replace('\*', '', regex=True)
    df['gamesBack'][0] = 0
    df['year'] = year
    df['conference'] = conference
    return df