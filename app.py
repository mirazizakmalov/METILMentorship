# AI-Powered Virtual Mentorship System

# # Project Overview
# The goal is to build a secure and scalable mentorship system for DOE employees to:
# 1. **Answer queries** from a knowledge base (manuals, guidelines, and FAQs).
# 2. **Provide resource suggestions** for broader context.
# 3. **Test employees** with curated questions to evaluate their understanding.
# 4. **Identify knowledge gaps** and recommend further training.

import sqlite3
import logging
import json
from flask import Flask, jsonify, request
from sentence_transformers import SentenceTransformer, util
# from flask_caching import Cache
from transformers import pipeline
import torch
import time
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # enables cross-origin requests for Flask app.

# Load the QA model for domain-specific questions
device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU
qa_pipeline = pipeline("question-answering", model="./models/distilbert-base-uncased", tokenizer="./models/distilbert-base-uncased", device=device)

# Load a general-purpose model for answering general questions
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
if torch.cuda.is_available():
    embedding_model = embedding_model.to('cuda')  # Move model to GPU
    
# Configure caching
# cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
#Caching improves response time by storing frequently used results.

# Configure logging, log data like request times, query types, and user inputs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    return text.strip()

# Precompute question embeddings
PRECOMPUTED_EMBEDDINGS = {}

def preload_embeddings():
    try:
        with sqlite3.connect("dataset.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT question FROM qa")
            questions = cursor.fetchall()
        
        global PRECOMPUTED_EMBEDDINGS
        PRECOMPUTED_EMBEDDINGS = {}

        for q in questions:
            question_text = q[0]
            try:
                normalized_question = normalize_text(question_text)
                PRECOMPUTED_EMBEDDINGS[normalized_question] = embedding_model.encode(normalized_question, convert_to_tensor=True)
                logging.info(f"Embedding preloaded for question: {question_text}")
            except Exception as e:
                logging.error(f"Failed to encode question: {question_text}. Error: {e}")

        logging.info(f"Total questions preloaded: {len(PRECOMPUTED_EMBEDDINGS)}")
    except sqlite3.Error as e:
        logging.error(f"Database error while preloading embeddings: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while preloading embeddings: {e}")


preload_embeddings()



def check_answer_correctness(user_answer, correct_answer):
    user_embedding = embedding_model.encode(user_answer, convert_to_tensor=True)
    correct_embedding = embedding_model.encode(correct_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(user_embedding, correct_embedding).item()

    if similarity > 0.8:
        correctness = "Correct"
    elif similarity > 0.5:
        correctness = "Partially Correct"
    else:
        correctness = "Incorrect"

    return correctness, similarity


def query_dataset(question):
    try:
        with sqlite3.connect("dataset.db") as conn:
            cursor = conn.cursor()
            
            # Normalize user input
            normalized_user_question = normalize_text(question)
            
            # Attempt exact match
            cursor.execute("""
                SELECT question, answer, manual_name, page_number 
                FROM qa 
                WHERE LOWER(question) = LOWER(?)
            """, (normalized_user_question,))
            exact_match = cursor.fetchone()

            if exact_match:
                logging.info(f"Exact match found for question: {question}")
                return {
                    "question": exact_match[0],
                    "answer": exact_match[1],
                    "manual_name": exact_match[2],
                    "page_number": exact_match[3],
                    "similarity_score": 1.0
                }

            # Retrieve all rows for similarity matching
            logging.info(f"No exact match for question: {question}. Proceeding with similarity search.")
            cursor.execute("SELECT question, answer, manual_name, page_number FROM qa")
            rows = cursor.fetchall()
        
        # Perform similarity matching
        question_embedding = embedding_model.encode(normalized_user_question, convert_to_tensor=True)  # User question embedding
        best_match = None
        highest_similarity = 0.0

        for row in rows:
            stored_question, answer, manual_name, page_number = row
            normalized_stored_question = normalize_text(stored_question)
            stored_embedding = PRECOMPUTED_EMBEDDINGS.get(normalized_stored_question)
            
            if stored_embedding is None:
                logging.warning(f"Precomputed embedding missing for: {stored_question}")
                continue
            
            # Calculate similarity
            similarity = util.pytorch_cos_sim(question_embedding, stored_embedding).item()
            logging.debug(f"Similarity for '{stored_question}' with '{question}': {similarity}")
            
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = {
                    "question": stored_question,
                    "answer": answer,
                    "manual_name": manual_name,
                    "page_number": page_number,
                    "similarity_score": similarity
                }

        # Return the best match if it exceeds the threshold
        if best_match and highest_similarity > 0.6:
            logging.info(f"Best match found for question: {question} with similarity: {highest_similarity}")
            return best_match
        
        # Provide a suggestion if partial similarity is found
        if best_match and 0.4 < highest_similarity <= 0.6:
            logging.info(f"Suggestion provided for question: {question}")
            return {
                "suggestion": f"Did you mean: '{best_match['question']}'?",
                "data": None
            }
        
        # No suitable match found
        logging.info(f"No suitable match found for question: {question}.")
        return {"message": "No suitable match found."}

    except sqlite3.Error as e:
        logging.error(f"SQLite error in query_dataset: {e}")
        return {"error": "Database operation failed"}
    except Exception as e:
        logging.error(f"Unexpected error in query_dataset: {e}")
        return {"error": "Unexpected operation error"}





@app.route('/ask', methods=['POST'])
# @cache.cached(query_string=True)
def ask_question():
    start_time = time.time()
    try:
        data = request.json
        question = data.get('question')
        user_answer = data.get('user_answer', None) #Optional
        # context = data.get('context', "This system provides information about radioactive materials, safety protocols, and general knowledge related to DOE operations.")

        if not question:
            return jsonify({"status": "error", "message": "Question is required", "data": None}), 400
            
        # Check the database
        dataset_result = query_dataset(question)
        logging.info(f"Exact match found: {dataset_result}" if dataset_result and dataset_result.get("similarity_score") == 1.0 else "No exact match, using similarity search.")
        
        if dataset_result:
            logging.info(f"Best similarity score: {dataset_result.get('similarity_score')}")
            correct_answer = dataset_result.get("answer")
            manual_name = dataset_result.get("manual_name")
            page_number = dataset_result.get("page_number")
            similarity_score = dataset_result.get("similarity_score", None)

            response_data = {
                "question": dataset_result.get("question"),
                "answer": correct_answer,
                "manual_name": manual_name,
                "page_number": page_number,
                "question_similarity_score": similarity_score,
            }
            
            # If user_answer is provided, check correctness and similarity
            if user_answer:
                correctness, answer_similarity = check_answer_correctness(user_answer, correct_answer)
                response_data.update({
                    "user_answer": user_answer,
                    "answer_correctness": correctness,
                    "answer_similarity_score": round(answer_similarity, 2),
                })

            return jsonify({
                "status": "success",
                "data": response_data,
                "message": "Query successful"
            }), 200


        # If no match in the database, use the summarized text and AI model
        try:
            with open("summarized_text.txt", "r", encoding="utf-8") as file:
                summarized_text = file.read().strip()
        except FileNotFoundError:
            logging.warning("Summarized text file not found. Falling back to extracted text.")
            try:
                with open("extracted_text.txt", "r", encoding="utf-8") as file:
                    summarized_text = file.read().strip()
            except FileNotFoundError:
                logging.error("Neither summarized nor extracted text files are available.")
                return jsonify({"status": "error", "message": "Context unavailable, no results found"}), 404

        
        # Use AI model to generate an answer
        model_answer = qa_pipeline(question=question, context=summarized_text)
        logging.info(f"Answer generated by AI model for question: {question}")

        end_time = time.time()
        logging.info(f"Processing time for /ask: {end_time - start_time} seconds")
        return jsonify({
                "status": "success",
                "data": {
                    "answer": model_answer['answer'],
                    "score": model_answer['score'],
                    "source": "AI Model",
                    "similarity_score": None
                },
                "message": "Fallback to AI model"
            }), 200
        
    except Exception as e:
        logging.error(f"Error in /ask: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error", "data": None}), 500



#suggest resources based on a topic
@app.route('/recommend_resources', methods=['POST'])
def recommend_resources():
    start_time = time.time()

    try:
        data = request.json
        topic = data.get('topic')

        if not topic:
            return jsonify({
                "status": "error",
                "message": "Topic is required",
                "data": None
            }), 400

        logging.info(f"Received topic for recommendation: {topic}")

        # Normalize and calculate topic embedding
        normalized_topic = normalize_text(topic)
        topic_embedding = embedding_model.encode(normalized_topic, convert_to_tensor=True)
        recommendations = []

        with sqlite3.connect("dataset.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT manual_name, page_number, question, answer FROM qa")
            rows = cursor.fetchall()

        for manual_name, page_number, question, answer in rows:
            normalized_stored_question = normalize_text(question)
            stored_embedding = PRECOMPUTED_EMBEDDINGS.get(normalized_stored_question)

            if stored_embedding is None:
                logging.warning(f"No precomputed embedding for question: {question}")
                continue

            try:
                # Calculate similarity and extract scalar value
                similarity = util.pytorch_cos_sim(topic_embedding, stored_embedding).item()
                logging.info(f"Similarity for '{question}' with topic '{topic}': {similarity}")

                # Include only results with similarity > 0.6
                if similarity > 0.6:
                    recommendations.append({
                        "manual_name": manual_name or "N/A",
                        "page_number": page_number or "N/A",
                        "question": question,
                        "answer": answer,
                        "similarity": similarity
                    })
            except Exception as e:
                logging.error(f"Error calculating similarity for question '{question}': {e}")
                continue

        # Sort recommendations by similarity
        recommendations.sort(key=lambda x: x['similarity'], reverse=True)

        if not recommendations:
            logging.info("No relevant resources found for the given topic.")
            return jsonify({
                "status": "success",
                "message": "No relevant resources found for the given topic.",
                "data": []
            }), 200

        end_time = time.time()
        logging.info(f"Processing time for /recommend_resources: {end_time - start_time} seconds")

        return jsonify({
            "status": "success",
            "message": "Resources recommended successfully",
            "data": recommendations
        }), 200

    except sqlite3.Error as e:
        logging.error(f"Database error in /recommend_resources: {e}")
        return jsonify({
            "status": "error",
            "message": "Database error occurred",
            "data": None
        }), 500
    except Exception as e:
        logging.error(f"Error in /recommend_resources: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal Server Error",
            "data": None
        }), 500


    
    
    
#Let users start a test and specify the number of questions.
@app.route('/test', methods=['POST']) 
def test():
    try:
        data = request.json
        num_questions = data.get('num_questions', 5)

        if not isinstance(num_questions, int) or num_questions <= 0:
            return jsonify({"status": "error", "message": "Invalid num_questions parameter"}), 400

        with sqlite3.connect("dataset.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT question, answer FROM qa ORDER BY RANDOM() LIMIT ?", (num_questions,))
            rows = cursor.fetchall()

        if not rows:
            return jsonify({"status": "error", "message": "No questions available"}), 404

        # Format questions and answers
        questions = [{"question": row[0], "correct_answer": row[1]} for row in rows]

        return jsonify({"status": "success", "data": {"questions": questions}, "message": "Test generated"}), 200
    except Exception as e:
        logging.error(f"Error in /test: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


    
#Fetch questions from the database for review.
@app.route('/review', methods=['GET'])
def review():
    #Pagination to avoid returning too much data
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    try:
        with sqlite3.connect("dataset.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT question, answer FROM qa")
            rows = cursor.fetchall()

        if not rows:
            return jsonify({"status": "error", "message": "No questions available for review", "data": None}), 404

        return jsonify({
            "status": "success",
            "data": [{"question": row[0], "answer": row[1]} for row in rows],
            "message": "Questions fetched"
        }), 200
    except Exception as e:
        logging.error(f"Error in /review: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error", "data": None}), 500



#Global Error Handlers
@app.errorhandler(404)
def not_found(error):
    logging.error("404 Not Found: %s", request.url)
    return jsonify({"error": "Not Found"}), 404
@app.errorhandler(500)
def internal_error(error):
    logging.error("500 Internal Server Error: %s", error)
    return jsonify({"error": "Internal Server Error"}), 500



if __name__ == '__main__':
    app.run(debug=True)

