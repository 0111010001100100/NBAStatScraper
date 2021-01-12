import pandas as pd 
import unicodedata, unidecode 
import sys

sys.path.append('../../')
import players
import db

def prep_players(letter):
    '''
    Prepare the player information for the database.
        Parameters:
            letter (string): A letter for which players to add ('a' will return players whose last name beings with 'a')
        Returns:
            A Pandas dataframe containing player information.
    note::
        Players who did not go to college are filled with BallSoHardU to handle the missing value.
    '''
    f = "../csv/players/{}.csv".format(letter)
    df = pd.read_csv(f, header=None, names=['name','playerId','start','end','pos','height','weight','birth','college'])
    df['name'] = df['name'].apply(db.decode_names)
    df['college'] = df['college'].fillna('BallSoHardU')
    return df

def prep_player_stats(extension):
    '''
    Prepare the player stats for the database.
        Parameters:
            extension (string): The URL extension of a given player (e.g. 'hardenja01')
        Returns:
            A Pandas dataframe containing player stats, transformed for the database.
    '''
    df = players.get_career_player_stats(extension, 'game')
    cols = ['year', 'age', 'tm', 'lg', 'pos', 'g', 'gs', 'mp', 'fg', 'fga', 'fgp', 'three',
                  'threeA', 'threeP', 'two', 'twoA', 'twoP', 'efg', 'ft', 'fta', 'ftp', 'orb',
                  'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
    pre_cols = ['Season', 'Age', 'Tm', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 
                '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 
                'TOV', 'PF', 'PTS']
    df = df.drop(df[df['Season'].str.contains("season")].index)
    df = df.drop(df[df['Season'].str.contains("Career")].index)
    for stat in pre_cols:
        if not df.columns.isin([stat]).any():
            df[stat] = 0
    renames = {pre_cols[i] : cols[i] for i in range(len(cols))}
    df = df.rename(columns = renames)
    df['playerid'] = extension
    df['year'] = df['year'].apply(db.prep_year)
    return df