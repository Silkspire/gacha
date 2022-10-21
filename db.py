import sqlite3
import atexit

db = 'database.db'
conn = sqlite3.connect(db)
print(conn.execute("SELECT name FROM keys LIMIT 1").fetchone()[0])


def get_discord_token():
    return conn.execute("SELECT key FROM keys WHERE name = ?", ('discord',)).fetchone()[0]



def close_database():
    conn.close()
    print(">>>>>>>>>SUCCESSFULLY CLOSED DATABASE")