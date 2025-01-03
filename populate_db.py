import sqlite3

def add_to_database(question, answer):
    
    conn = sqlite3.connect("knowledge_base.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resources (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    add_to_database("What is uranium?", "Uranium is a radioactive element")
    add_to_database("What is a safety protocol?", "A safety protocol ensures safe handling of materials.")
    print("Data added successfully.")