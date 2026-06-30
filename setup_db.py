import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rocketleague.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    date TEXT,
    tournament TEXT,
    tier TEXT,
    bestof INTEGER,
    match_type TEXT,
    team_a TEXT,
    team_b TEXT,
    score_a INTEGER,
    score_b INTEGER,
    winner INTEGER
)
""")

conn.commit()
conn.close()
print("Database created.")