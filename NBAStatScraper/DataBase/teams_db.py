import sqlite3
from sqlite3 import Error
import pandas as pd

import databasePrep.prep_teams as prep

def create_team_table(conn):
    '''
    Create the teams table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS teams(id integer PRIMARY KEY, name text, abbrv text, location text)"""
    cursor.execute(query)
    conn.commit()

def populate_team_table(conn):
    '''
    Add all teams to the teams table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    teams_df = pd.read_csv('../csv/teams.csv') 
    teams_df.to_sql('team', conn, if_exists='append', index=False)

def create_team_stats_table(conn):
    '''
    Create the team.perGame stats table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS "teams.perGame"(id integer PRIMARY KEY, year integer, teamId integer, wins integer, losses integer, 
               finish integer, avgAge float, avgHeight text, avgWeight integer, gamesPlayed integer, fg integer, fga integer, fgp float, 
               three integer, threeA integer, threeP float, two integer, twoA integer, twoP float, ft integer, fta integer, ftp float, 
               orb integer, drb integer, trb integer, ast integer, stl integer, blk integer, tov integer, pf integer, pts integer, 
               FOREIGN KEY (teamID) REFERENCES teams(abbrv))"""
    cursor.execute(query)
    conn.commit()

def populate_team_stats_table(conn):
    '''
    Add all per game team stats to the teams.perGame table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    teams = pd.read_csv('../csv/teams.csv')
    for team in teams['abbrv']:
        df = prep.prep_teams(team)
        df.to_sql("teams.perGame", conn, if_exists='append', index=False)