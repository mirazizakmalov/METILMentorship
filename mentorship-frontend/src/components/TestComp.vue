<template>
  <div class="test-container">
    <h1>Take the Test</h1>

    <!-- Before Test Starts -->
    <div v-if="!started">
      <input
        v-model="numQuestions"
        type="number"
        placeholder="Enter number of questions"
        min="1"
      />
      <button @click="startTest">Start Test</button>
    </div>

    <!-- During Test -->
    <div v-if="started && !finished">
      <h2>Question {{ currentQuestionIndex + 1 }} of {{ numQuestions }}</h2>
      <p>{{ questions[currentQuestionIndex].question }}</p>
      <input v-model="currentAnswer" type="text" placeholder="Your answer" />
      <button @click="submitAnswer">Next</button>
    </div>

    <!-- After Test Ends -->
    <div v-if="finished">
      <h2>Test Results</h2>
      <ul>
        <li v-for="(item, index) in results" :key="index">
          <p><strong>Question:</strong> {{ item.question }}</p>
          <p>
            <strong>Your Answer:</strong>
            {{ item.userAnswer || "No answer given" }}
          </p>
          <p><strong>Correct Answer:</strong> {{ item.correctAnswer }}</p>
          <p>
            <strong>Similarity Score:</strong> {{ item.similarity.toFixed(2) }}
          </p>
          <p>
            <strong>Correctness:</strong>
            <span :class="getCorrectnessClass(item.correctness)">
              {{ item.correctness }}
            </span>
          </p>
        </li>
      </ul>
      <h3>Total Score: {{ totalScore }}/{{ results.length }}</h3>
      <button @click="restartTest">Restart Test</button>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  data() {
    return {
      numQuestions: 5,
      questions: [],
      currentQuestionIndex: 0,
      currentAnswer: "",
      results: [],
      totalScore: 0,
      started: false,
      finished: false,
    };
  },
  methods: {
    async startTest() {
      try {
        const res = await axios.post("/test", {
          num_questions: this.numQuestions,
        });
        this.questions = res.data.data.questions;
        this.started = true;
        this.finished = false;
        this.results = [];
        this.totalScore = 0;
        this.currentQuestionIndex = 0;
        this.currentAnswer = "";
      } catch (error) {
        console.error("Error starting test:", error);
      }
    },
    async submitAnswer() {
      const currentQuestion = this.questions[this.currentQuestionIndex];
      try {
        const res = await axios.post("http://127.0.0.1:5000/ask", {
          question: currentQuestion.question,
          user_answer: this.currentAnswer,
        });

        const backendResponse = res.data.data;

        this.results.push({
          question: backendResponse.question,
          userAnswer: backendResponse.user_answer || "No answer given",
          correctAnswer: backendResponse.answer,
          similarity: backendResponse.answer_similarity_score,
          correctness: backendResponse.answer_correctness,
        });

        if (backendResponse.answer_correctness === "Correct") {
          this.totalScore++;
        }

        this.currentAnswer = "";
        this.currentQuestionIndex++;

        if (this.currentQuestionIndex >= this.questions.length) {
          this.finished = true;
        }
      } catch (error) {
        console.error("Error submitting answer:", error);
      }
    },
    restartTest() {
      this.started = false;
      this.finished = false;
      this.numQuestions = 5;
      this.questions = [];
      this.results = [];
      this.totalScore = 0;
      this.currentQuestionIndex = 0;
      this.currentAnswer = "";
    },
    getCorrectnessClass(correctness) {
      if (correctness === "Correct") return "correct";
      if (correctness === "Partially Correct") return "partial";
      return "incorrect";
    },
  },
};
</script>

<style scoped>
/* Container styling for the test */
.test-container {
  max-width: 800px;
  margin: 30px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Heading styling */
.test-container h1 {
  font-size: 2rem;
  color: #136ec9;
  margin-bottom: 20px;
}

/* Input field for number of questions */
.test-container input[type="number"] {
  width: 60%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 20px;
}

/* Buttons styling */
.test-container button {
  padding: 10px 20px;
  font-size: 1rem;
  color: #ffffff;
  background-color: #136ec9;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.test-container button:hover {
  background-color: #0d4a8c;
}

/* Question display styling */
.test-container h2 {
  font-size: 1.5rem;
  color: #333333;
  margin-bottom: 20px;
}

.test-container p {
  font-size: 1.2rem;
  color: #555555;
}

/* Input field for answers */
.test-container input[type="text"] {
  width: 80%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 20px;
}

/* Results styling */
.test-container ul {
  list-style: none;
  padding: 0;
}

.test-container li {
  text-align: left;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.test-container li p {
  margin: 5px 0;
}

.test-container .correct {
  color: green;
  font-weight: bold;
}

.test-container .partial {
  color: orange;
  font-weight: bold;
}

.test-container .incorrect {
  color: red;
  font-weight: bold;
}

/* Total score */
.test-container h3 {
  font-size: 1.5rem;
  color: #333333;
  margin-top: 30px;
}

.test-container h3 span {
  font-weight: bold;
}

/* Restart button */
.test-container .restart-button {
  margin-top: 20px;
  padding: 10px 25px;
  font-size: 1.1rem;
  background-color: #28a745;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.test-container .restart-button:hover {
  background-color: #218838;
}
</style>
