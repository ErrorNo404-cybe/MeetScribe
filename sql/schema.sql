CREATE TABLE IF NOT EXISTS dim_meeting (
    meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_title TEXT,
    meeting_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transcript TEXT,
    attendees TEXT
);

CREATE TABLE IF NOT EXISTS fact_actions (
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meeting_id INT REFERENCES dim_meeting(meeting_id),
    action_type TEXT,
    action_text TEXT,
    owner TEXT,
    due_date DATE,
    status TEXT DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);