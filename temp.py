import sqlite3
import json

# Connect to SQLite database (create if it doesn't exist)
conn = sqlite3.connect("combined_dataset.db")
cursor = conn.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source TEXT
);
""")

# Insert data from JSON
with open("qa_dataset.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)
    for item in json_data:
        cursor.execute("INSERT INTO qa (question, answer, source) VALUES (?, ?, ?)",
                       (item["question"], item["answer"], "JSON Dataset"))

# Insert data from the existing SQLite database
existing_conn = sqlite3.connect("knowledge_base.db")
existing_cursor = existing_conn.cursor()
existing_cursor.execute("SELECT question, answer FROM resources")
for row in existing_cursor.fetchall():
    cursor.execute("INSERT INTO qa (question, answer, source) VALUES (?, ?, ?)",
                   (row[0], row[1], "Database"))

# Commit and close connections
conn.commit()
existing_conn.close()
conn.close()
print("Data merged successfully into combined_dataset.db")
