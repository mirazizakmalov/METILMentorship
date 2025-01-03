import sqlite3
import json

def export_questions_to_json():
    try:
        # Connect to the database
        with sqlite3.connect("combined_dataset.db") as conn:
            cursor = conn.cursor()
            # Query all questions
            cursor.execute("SELECT question FROM qa")
            questions = [row[0] for row in cursor.fetchall()]

        # Convert to JSON
        questions_json = {"questions": questions}
        with open("questions.json", "w", encoding="utf-8") as json_file:
            json.dump(questions_json, json_file, indent=4, ensure_ascii=False)

        print("Questions exported to questions.json")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    export_questions_to_json()
