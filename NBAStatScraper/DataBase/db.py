import sqlite3
from sqlite3 import Error
import pandas as pd
import unicodedata, unidecode
import string
import sys
import uuid

sys.path.append('../')
import player

def connect():
    try:
        conn = sqlite3.connect('nbadatabase.db')
        print("Connection is established...")
        return conn
    except Error:
        print(Error)
    




# conn = connect()
# # conn.set_trace_callback(print)
# # create_player_table(conn)
# # populate_player_table(conn)
# # create_player_stats_table(conn)
# rows = get_player_ids(conn)
# pd.options.display.width = 0
# # for row in rows:
# #     print(row[0])
#     # print(populate_player_stats_tables(conn, row[0]))
# print(player.get_career_player_stats('abdulma01', 'playoffGame'))
# conn.close()
