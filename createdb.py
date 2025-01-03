import sqlite3
import json

# Define database and JSON file paths
new_db_path = "dataset.db"
json_files = ["GeneralEmployee.json", "GoodPractices.json", "Radiological.json"]  # Replace with your JSON file names

def create_and_populate_database(new_db_path, json_files):
    try:
        # Connect to the new database
        with sqlite3.connect(new_db_path) as conn:
            cursor = conn.cursor()
            
            # Create a new table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS qa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    page_number INTEGER NOT NULL,
                    manual_name TEXT NOT NULL
                );
            """)
            
            # Process each JSON file
            for json_file in json_files:
                with open(json_file, "r") as file:
                    data = json.load(file)
                    
                    # Ensure the data is under 'questions_and_answers'
                    if "questions_and_answers" in data:
                        entries = data["questions_and_answers"]
                    else:
                        raise ValueError(f"Invalid JSON format in file: {json_file}")
                    
                    # Insert each Q&A into the database
                    for entry in entries:
                        cursor.execute("""
                            INSERT INTO qa (question, answer, page_number, manual_name) 
                            VALUES (?, ?, ?, ?);
                        """, (
                            entry["question"], 
                            entry["answer"], 
                            entry["page_number"], 
                            json_file
                        ))
            
            conn.commit()
            print(f"Database '{new_db_path}' created and populated successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the script
create_and_populate_database(new_db_path, json_files)
