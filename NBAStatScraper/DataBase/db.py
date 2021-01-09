import sqlite3
from sqlite3 import Error
import pandas as pd
import unicodedata, unidecode
import string

def connect():
    try:
        conn = sqlite3.connect('nbadatabase.db')
        print("Connection is established...")
        return conn
    except Error:
        print(Error)
    
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

def create_player_stats_table(conn):
    cursor = conn.cursor()
    measurement = ['game', 'total', 'min', 'pos', 'shooting', 'playoffTotal', 'playoffGame', 'playoffMin', 'playoffPos', 
                'playoffShooting','careerHighs', 'playoffCareerHighs','college', 'salary', 'contract']
    for i in measurement:
        try:
            cursor.execute("DROP TABLE {}".format(i))
        finally:
            query = """CREATE TABLE {}(id integer PRIMARY KEY, Season text, Age integer, Tm text, Lg text
            Pos text, G integer, GS integer, MP float, FG float, FGA float, FGPerc float, Threes float, ThreesA float, 
            ThreesPerc float, Twos float, TwosA float, TwosPerc float, eFG float, FT float, FTA float, FTPerc float, ORB float,
            DRB float, TRB float, AST float, STL float, BLK float, TOV float, PF float, PTS float, playerid text,
            FOREIGN KEY (playerid) REFERENCES players(id))""".format(i)
            cursor.execute(query)

conn = connect()
conn.set_trace_callback(print)
# create_player_table(conn)
# populate_player_table(conn)
create_player_stats_table(conn)
conn.close()
