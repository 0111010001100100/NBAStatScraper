import pandas as pd
import sys

sys.path.append('../../')
import standings

def prep_standings(year):
    '''
    Get the transformed standings for a given year.
        Parameters: 
            year (string): The year to get the standings for (e.g. '2020')
        Returns:
            A Pandas dataframe containing the league standings.
    '''
    west = _prep_standings('W', year)
    east = _prep_standings('E', year)
    return pd.concat([west, east])

def _prep_standings(conference, year):
    '''
    Helper function for transforming the scraped standings for the database.
        Parameters:
            conference (string): The conference to get the division standings of. Can be either 'W' or 'E'.
            year (string): year (string): The year to get the standings for (e.g. '2020')
        Returns:
            A Pandas dataframe containing the transformed standings for a the conference in the year.
    '''
    df = standings.get_division_standings(conference, year) 
    df.columns = ['teamId', 'wins', 'losses', 'ratio', 'gamesBack', 'ppg', 'oppg', 'srs']
    df = df.drop(['srs', 'gamesBack'], axis=1)
    df = df.drop(df[df['teamId'].str.contains("Division")].index)
    df = df.replace('\*', '', regex=True)
    df['year'] = year
    df['conference'] = conference
    df['teamId'] = df['teamId'].apply(team_to_id)
    return df

def team_to_id(team):
    '''
    Convert team name to the team identifier.
        Parameters:
            team (string): The name of a team.
        Returns:
            The 3 letter abbreviation of the team.
    '''
    teams = pd.read_csv('../csv/teams.csv')
    return teams.loc[teams['name'] == team, 'abbrv'].iloc[0]
