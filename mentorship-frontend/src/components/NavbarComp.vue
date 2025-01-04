<template>
    <nav class="navbar">
      <ul class="navbar-list">
        <li class="navbar-item">
          <router-link to="/">Home</router-link>
        </li>
        <li class="navbar-item">
          <router-link to="/ask">Ask a Question</router-link>
        </li>
        <li class="navbar-item">
          <router-link to="/recommend-resources">Recommend Resources</router-link>
        </li>
        <li class="navbar-item">
          <router-link to="/test">Test</router-link>
        </li>
        <li class="navbar-item">
          <router-link to="/review">Review</router-link>
        </li>
      </ul>
    </nav>
  </template>
  
  <script>
  export default {};
  </script>
  
  <style>
  .navbar {
    display: flex;
    justify-content: center;
    background-color: #07d531; /* Green background */
    padding: 10px;
  }
  
  .navbar-list {
    display: flex;
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .navbar-item {
    margin: 0 15px;
  }
  
 .navbar-item a {
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 1.5rem; /* Adjust the font size here (smaller value) */
  transition: color 0.3s;
}

.navbar-item a:hover {
  color: #d1ffd7; /* Light green hover color */
}

.navbar-item .router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
  </style>
  