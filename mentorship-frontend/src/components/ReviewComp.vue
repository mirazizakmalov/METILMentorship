<template>
    <div class="review-questions">
      <h1>Review Questions</h1>
      <button @click="fetchQuestions">Load Questions</button>
      <div v-if="questions.length" class="questions-list">
        <ul>
          <li v-for="(question, index) in questions" :key="index" class="question-item">
            <strong>{{ question.question }}</strong>
            <br />
            <span>{{ question.answer }}</span>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "@/axios";
  
  export default {
    data() {
      return {
        questions: [],
      };
    },
    methods: {
      async fetchQuestions() {
        try {
          const response = await axios.get("/review");
          this.questions = response.data.data || [];
        } catch (error) {
          console.error("Error fetching questions:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .review-questions {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 20px auto;
    padding: 20px;
    max-width: 800px; /* Limit the section width */
  }
  
  button {
    margin: 10px 0;
    padding: 10px 20px;
    background-color: #07d531;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #059424;
  }
  
  .questions-list {
    width: 100%;
  }
  
  .questions-list ul {
    list-style: none; /* Remove bullet points */
    padding: 0;
  }
  
  .question-item {
    text-align: center; /* Center the text */
    margin-bottom: 20px; /* Add spacing between items */
  }
  
  .question-item strong {
    font-size: 1.2rem; /* Slightly larger font for questions */
  }
  
  .question-item span {
    display: block;
    margin-top: 10px;
    color: #555; /* Add a subtle color to differentiate answers */
  }
  </style>
  