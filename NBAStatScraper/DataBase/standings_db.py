import sqlite3
from sqlite3 import Error
import pandas as pd

import databasePrep.prep_standings as prep

def create_standings_table(conn):
    '''
    Create the standings table.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS standings(id integer PRIMARY KEY, teamId text, wins integer, losses integer,
                ratio float, ppg float, oppg float, year integer, conference text, FOREIGN KEY (teamID) REFERENCES teams(abbrv))"""
    cursor.execute(query)
    conn.commit()

def populate_standings_table(conn):
    '''
    Add all standings to the table from 2001-02 season through 2020 season.
        Parameters:
            conn (object): Sqlite3 connection object.
    '''
    cursor = conn.cursor()
    for year in range(2002, 2021):
        df = prep.prep_standings(year)
        df.to_sql('standings', conn, if_exists='append', index=False)
