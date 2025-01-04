<template>
  <div class="ask-question-container">
    <!-- Centered Header -->
    <h1 class="header">Ask a Question</h1>

    <!-- Form Group -->
    <div class="form-group">
      <!-- Question Input -->
      <input
        v-model="question"
        type="text"
        placeholder="Enter your question..."
        class="question-input"
      />
      <!-- Submit Button -->
      <button @click="submitQuestion" class="submit-button">Submit</button>
    </div>

    <!-- Response Box -->
    <div v-if="response" class="response-box">
      <h2>Response:</h2>
      <p><strong>Question:</strong> {{ response.question }}</p>
      <p><strong>Answer:</strong> {{ response.answer }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      question: "", // User's question
      response: null, // API response
    };
  },
  methods: {
    async submitQuestion() {
      try {
        // Reset the response for a new query
        this.response = null;

        // Make API call
        const res = await axios.post("http://127.0.0.1:5000/ask", {
          question: this.question,
        });

        // Log and store the API response
        console.log("API Response:", res.data.data);
        this.response = res.data.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style>
/* Container for the entire component */
.ask-question-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto; /* Centers the container horizontally */
}

/* Centered Header */
.header {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: white; /* Keep the text white */
}

/* Form Group */
.form-group {
  display: flex;
  align-items: center;
  gap: 10px; /* Add spacing between input and button */
}

/* Question Input */
.question-input {
  flex-grow: 1; /* Allows the input to stretch horizontally */
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 100%; /* Ensures it stretches across the screen */
  max-width: none; /* Removes any limitations on width */
  box-sizing: border-box; /* Prevents padding from exceeding width */
}

/* Submit Button */
.submit-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #0056b3;
}

/* Response Box */
.response-box {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}
</style>
