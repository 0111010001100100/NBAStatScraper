import sqlite3
from sqlite3 import Error
import pandas as pd
import unicodedata, unidecode
import sys

sys.path.append('../')
import teams 
import players
import standings_db as standings

def connect():
    '''
    Connect to the nbadatabase.
        Returns:
            The sqlite3 connection object
    '''
    try:
        conn = sqlite3.connect('nbadatabase.db')
        print("Connection is established...")
        return conn
    except Error:
        print(Error)
    
def decode_names(name):
    '''
    Removes all accents from name.
        Parameters:
            name (string): A name to decode.
        Returns:
            The name with all accents removed. 
    '''
    return unidecode.unidecode(unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8"))

def prep_year(yr):
    '''
    Converts the season string to a year (e.g. 2001-02 to 2002)
        Parameters:
            yr (string): The season string.
        Returns:
            The year of the season.
    '''
    return int(yr.split('-')[0]) + 1


def create_db():
    '''
    Create and populate all tables in the database.
    '''
    conn = connect()
    # players.create_player_table(conn)
    # players.create_player_stats_table(conn)
    # teams.create_team_table(conn)
    # teams.create_team_stats_table(conn)
    standings.create_standings_table(conn)

    # players.populate_player_table(conn)
    # players.populate_player_stats_table(conn)
    # teams.populate_team_table(conn)
    # teams.populate_team_stats_table(conn)
    standings.populate_standings_table(conn)
    conn.close()

create_db()