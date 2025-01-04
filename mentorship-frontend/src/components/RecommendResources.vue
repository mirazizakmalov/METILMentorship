<template>
  <div class="recommend-container">
    <h1 class="center-text">Recommend Resources</h1>
    <input
      id="questionInput"
      v-model="topic"
      type="text"
      placeholder="Enter a topic"
      class="input-box"
    />
    <button @click="recommendResources" class="recommend-button">
      Recommend
    </button>
    <div v-if="resources.length" class="resources-container">

      <ul>
        <li
          v-for="(resource, index) in resources"
          :key="index"
          class="resource-item"
        >
          <p><strong>Question:</strong> {{ resource.question }}</p>
          <p><strong>Answer:</strong> {{ resource.answer }}</p>
          <p>
            <strong>Manual:</strong> {{ resource.manual_name }} (Page:
            {{ resource.page_number }})
          </p>
          <p>
            <strong>Similarity:</strong> {{ resource.similarity.toFixed(2) }}
          </p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "../axios";

export default {
  data() {
    return {
      topic: "",
      resources: [],
    };
  },
  methods: {
    async recommendResources() {
      try {
        const res = await axios.post("/recommend_resources", {
          topic: this.topic,
        });
        this.resources = res.data.data; // Ensure backend returns `data` field properly
      } catch (error) {
        console.error("Error fetching resources:", error);
      }
    },
  },
};
</script>

<style>
/* Main container styles */
.recommend-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: 0 auto;
  padding: 20px;
  max-width: 800px;
  background-color: #f9f9f9; /* Optional light background */
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Center text alignment */
.center-text {
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #333;
}

/* Input box styles */
.input-box {
  width: 100%;
  max-width: 600px;
  padding: 10px;
  margin-bottom: 15px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* Button styles */
.recommend-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.recommend-button:hover {
  background-color: #0056b3;
}

/* Resource container styles */
.resources-container {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
}

/* Individual resource item */
.resource-item {
  margin-bottom: 20px;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.resource-item:last-child {
  border-bottom: none;
}
</style>
