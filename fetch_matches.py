import os
import time
import sqlite3
import requests

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rocketleague.db")
print("Using database at:", DB_PATH)

API_KEY = os.environ.get("LIQUIPEDIA_API_KEY")
BASE_URL = "https://api.liquipedia.net/api/v3/match"

headers = {"Authorization": f"Apikey {API_KEY}"}

QUERY_FIELDS = "match2id,date,tournament,liquipediatier,bestof,type,finished,match2opponents,winner"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

offset = 0
limit = 100
total_inserted = 0

while True:
    params = {
        "wiki": "rocketleague",
        "limit": limit,
        "offset": offset,
        "query": QUERY_FIELDS,
        "conditions": "[[finished::1]] AND ([[liquipediatier::1]] OR [[liquipediatier::2]])"
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 429:
        print("Rate limited. Waiting 60 seconds...")
        time.sleep(60)
        continue  # retry same offset, don't move on

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        break

    data = response.json()
    results = data.get("result", [])

    if not results:
        print("No more results. Done.")
        break

    for match in results:
        try:
            opponents = match.get("match2opponents", [])
            if len(opponents) != 2:
                continue

            team_a = opponents[0].get("name", "")
            team_b = opponents[1].get("name", "")
            score_a = opponents[0].get("score", None)
            score_b = opponents[1].get("score", None)

            cursor.execute("""
                INSERT OR IGNORE INTO matches
                (match_id, date, tournament, tier, bestof, match_type, team_a, team_b, score_a, score_b, winner)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match.get("match2id"),
                match.get("date"),
                match.get("tournament"),
                match.get("liquipediatier"),
                match.get("bestof"),
                match.get("type"),
                team_a,
                team_b,
                score_a,
                score_b,
                match.get("winner")
            ))
            total_inserted += 1
        except Exception as e:
            print("Skipped a match due to error:", e)

    conn.commit()
    print(f"Inserted batch at offset {offset}. Total so far: {total_inserted}")

    offset += limit
    time.sleep(2)  # slower pace to avoid hitting the limit again

conn.close()
print("Finished. Total matches inserted:", total_inserted)