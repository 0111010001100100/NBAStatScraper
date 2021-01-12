import sqlite3
from sqlite3 import Error
import pandas as pd
import unicodedata, unidecode
import string
import sys
import uuid

sys.path.append('../')
import player

def create_player_table(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS players(name text, id text PRIMARY KEY, start integer, end integer, pos text, height text, weight integer, birth text, college text)")
    conn.commit()

def decode_names(name):
    return unidecode.unidecode(unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8"))

def populate_player_table(conn):
    print("Writing to player table...")
    for letter in (string.ascii_lowercase[:23] + string.ascii_lowercase[24:]):
        f = "../csv/{}.csv".format(letter)
        print(f)
        df = pd.read_csv(f, header=None, names=['name','id','start','end','pos','height','weight','birth','college'])
        df['name'] = df['name'].apply(decode_names)
        df['college'] = df['college'].fillna('BallSoHardU')
        df.to_sql("players", conn, if_exists='append', index=False)

def create_game_table(conn):
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS "players.game"(id integer PRIMARY KEY, season text, age integer, tm text, lg text,
        pos text, g integer, gs integer, mp float, fg float, fga float, fgperc float, threes float, threesa float, 
        threesperc float, twos float, twosa float, twosperc float, efg float, ft float, fta float, ftperc float, orb float,
        drb float, trb float, ast float, stl float, blk float, tov float, pf float, pts float , playerid text,
        FOREIGN KEY (playerid) REFERENCES players(id))"""
    cursor.execute(query)
    conn.commit()

def populate_game_table(conn, extension):
    df = player.get_career_player_stats(extension, 'game')
    df['playerid'] = extension
    df.to_sql('players.game', conn, if_exists='append', index=False)

def create_player_stats_table(conn):
    cursor = conn.cursor()
    measurement = ['game', 'playoffGame']
    for i in measurement:
        try:
            cursor.execute("DROP TABLE {}".format(i))
        finally:
            query = """CREATE TABLE "players.{}"(id integer PRIMARY KEY, season text, age integer, tm text, lg text,
            pos text, g integer, gs integer, mp float, fg float, fga float, fgperc float, threes float, threesa float, 
            threesperc float, twos float, twosa float, twosperc float, efg float, ft float, fta float, ftperc float, orb float,
            drb float, trb float, ast float, stl float, blk float, tov float, pf float, pts float , playerid text,
            FOREIGN KEY (playerid) REFERENCES players(id))""".format(i)
            cursor.execute(query)
            conn.commit()

def get_player_ids(conn):
    cursor = conn.cursor()
    query = "SELECT id FROM players"
    cursor.execute(query)
    return cursor.fetchall()

def populate_player_stats_tables(conn, extension):
    cursor = conn.cursor()
    measurement = ['game', 'playoffGame']
    for i in measurement:
        df = player.get_career_player_stats(extension, i)
        df['playerid'] = extension
        df.to_sql("players.{}".format(i), conn, if_exists='append', index=False)