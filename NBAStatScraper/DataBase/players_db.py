import sqlite3
from sqlite3 import Error
import pandas as pd
import string

import databasePrep.prep_players as prep
import db

def create_player_table(conn):
    '''
    Create the players table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS players(id integer PRIMARY KEY, name text, playerId text, start integer, end integer, pos text, height text, weight integer, birth text, college text)")
    conn.commit()

def populate_player_table(conn):
    '''
    Add all players to the players table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    for letter in (string.ascii_lowercase[:23] + string.ascii_lowercase[24:]):
        df = prep.prep_players(letter)
        df.to_sql("players", conn, if_exists='append', index=False)

def create_player_stats_table(conn):
    '''
    Create the players.perGame table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS "players.perGame"(id integer PRIMARY KEY, year text, age integer, tm text, lg text,
        pos text, g integer, gs integer, mp float, fg float, fga float, fgp float, three float, threeA float, 
        threeP float, two float, twoA float, twoP float, efg float, ft float, fta float, ftp float, orb float,
        drb float, trb float, ast float, stl float, blk float, tov float, pf float, pts float , playerid text,
        FOREIGN KEY (playerid) REFERENCES players(id))"""
    cursor.execute(query)
    conn.commit()

def populate_player_stats_table(conn):
    '''
    Add all per game player stats to the players.perGame table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    for player in get_player_ids(conn):
        df = prep.prep_player_stats(player[0])
        df.to_sql('players.perGame', conn, if_exists='append', index=False)

def get_player_ids(conn):
    '''
    Query the playerIds from the players table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    query = "SELECT playerId FROM players"
    cursor.execute(query)
    return cursor.fetchall()
