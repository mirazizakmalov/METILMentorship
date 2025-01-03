import os
from PyPDF2 import PdfReader
import sqlite3

def extract_text_with_metadata(pdf_path):
    # Extract text from a PDF file with page metadata
    reader = PdfReader(pdf_path)
    data = []
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text.strip():
            data.append({
                "page_number": page_number,
                "text": page_text.strip()
            })
    return data

def save_to_database(manual_data, db_path):
    # Save extracted text and metadata to a database
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                manual_name TEXT,
                page_number INTEGER,
                content TEXT
            )
        """)
        # Insert the data
        for entry in manual_data:
            cursor.execute("""
                INSERT INTO qa (manual_name, page_number, content)
                VALUES (?, ?, ?)
            """, (entry["manual_name"], entry["page_number"], entry["text"]))
        conn.commit()

if __name__ == "__main__":
    folder_path = "./Resources"  # Folder where manuals are stored
    db_path = "knowledge_base.db"

    all_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Extracting text from: {filename}")
            manual_data = extract_text_with_metadata(pdf_path)
            
            # Add manual name to each entry
            for entry in manual_data:
                entry["manual_name"] = filename

            all_data.extend(manual_data)
    
    if all_data:
        print(f"Saving data to the database: {db_path}")
        save_to_database(all_data, db_path)
        print("Database updated successfully!")
    else:
        print("No data extracted from manuals.")
