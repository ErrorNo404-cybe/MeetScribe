import sqlite3
import os

DB_PATH = "data/meetscribe.db"

def get_conn():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs("sql", exist_ok=True)
    with open("sql/schema.sql", "r", encoding="utf-8") as f:
        conn = get_conn()
        conn.executescript(f.read())
        conn.close()

def log_meeting(title, transcript, attendees):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO dim_meeting (meeting_title, transcript, attendees) VALUES (?,?,?)",
                (title, transcript, attendees))
    meeting_id = cur.lastrowid
    conn.commit(); conn.close()
    return meeting_id

def log_actions(meeting_id, actions_list):
    conn = get_conn()
    for a in actions_list:
        conn.execute("INSERT INTO fact_actions (meeting_id, action_type, action_text, owner, due_date) VALUES (?,?,?,?,?)",
                     (meeting_id, a['type'], a['text'], a['owner'], a['due']))
    conn.commit(); conn.close()