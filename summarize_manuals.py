import os
from transformers import pipeline
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    #Extract text from a PDF file
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

#Split the extracted text from the manual into smaller, manageable chunks before summarizing
def chunk_text(text, max_chunk_size=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1  # +1 for the space
        if current_length > max_chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = len(word) + 1
        current_chunk.append(word)

    # Add the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def summarize_text(text, max_length=512, min_length=50):
    import torch  # Imported only when needed
    #Summarize  text with BART
    device = 0 if torch.cuda.is_available() else -1  # Use GPU if available, otherwise CPU
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
    try:
        return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summarization failed."

def process_manuals(input_folder, output_file):
    #Process all PDFs then write summaries to an output file
    try:
        with open(output_file, "w", encoding="utf-8") as output:
            for filename in os.listdir(input_folder):
                if filename.endswith(".pdf"):
                    pdf_path = os.path.join(input_folder, filename)
                    print(f"Processing: {filename}")
                    
                    # Extract text from the PDF
                    text = extract_text_from_pdf(pdf_path)
                    if not text.strip():
                        print(f"No text extracted from {filename}. Skipping.")
                        continue

                    # Chunk the text
                    print(f"Chunking text for {filename}...")
                    chunks = chunk_text(text)

                    # Summarize each chunk and combine the summaries
                    print(f"Summarizing chunks for {filename}...")
                    final_summary = []
                    for i, chunk in enumerate(chunks):
                        print(f"Summarizing chunk {i + 1}/{len(chunks)}...")
                        summary = summarize_text(chunk)
                        final_summary.append(summary)

                    # Write the final summary to the output file
                    output.write(f"\n--- Summary of {filename} ---\n")
                    output.write(" ".join(final_summary) + "\n")
        print(f"Summarization completed! Output saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_folder = "./Resources"
    output_file = "summarized_text.txt"
    process_manuals(input_folder, output_file)
