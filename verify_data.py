import sqlite3

def verify_database():

    try:
        conn = sqlite3.connect("knowledge_base.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM resources")
        rows = cursor.fetchall()

        if rows:
            print("Data in 'resources' table:")
            for row in rows:
                print(f"ID: {row[0]}, Question: {row[1]}, Answer: {row[2]}")
        else:
            print("The 'resources' table is empty.")

        conn.close()
    except sqlite3.Error as e:
        print(f"An error occureed: {e}")

if __name__ == "__main__":
    verify_database()
