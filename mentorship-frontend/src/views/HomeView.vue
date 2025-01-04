<template>
    <div class="home">
      <!-- Hero Section -->
      <!-- <h1>Welcome to the Virtual Mentorship System</h1>
      <p>Your one-stop solution for learning and mentorship.</p> -->
  
      <!-- Feature Cards -->
      <div class="feature-cards">
        <router-link to="/ask" class="card">
          <h2>Ask a Question</h2>
          <p>Get answers to your queries instantly.</p>
        </router-link>
        <router-link to="/recommend-resources" class="card">
          <h2>Recommend Resources</h2>
          <p>Discover resources tailored to your needs.</p>
        </router-link>
        <router-link to="/test" class="card">
          <h2>Take a Test</h2>
          <p>Evaluate your understanding with curated tests.</p>
        </router-link>
        <router-link to="/review" class="card">
          <h2>Review Questions</h2>
          <p>Look back at the questions and answers.</p>
        </router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {};
  </script>
  
  <style scoped>
  .home {
    text-align: center;
    padding: 20px;
  }
  
  h1 {
    color: #136ec9;
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  p {
    margin-bottom: 2rem;
    font-size: 1.2rem;
    color: #34495e;
  }
  
  .feature-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    justify-items: center;
    margin: 20px 0;
  }
  
  .card {
    text-decoration: none;
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
  }
  
  .card h2 {
    font-size: 1.5rem;
    color: #136ec9;
    margin-bottom: 10px;
  }
  
  .card p {
    font-size: 1rem;
    color: #555;
  }
  </style>
  