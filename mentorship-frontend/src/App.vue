<template>
  <div id="app">
    <!-- Header Section -->
    <header class="header">
      <img src="@/assets/Rad.png" alt="Rad" class="header-image left" />
      <NavbarComp />
      <img
        src="@/assets/element.png"
        alt="Element"
        class="header-image right"
      />
    </header>

    <!-- Hero Section -->
    <div class="hero">
      <h1>Welcome to the Virtual Mentorship System</h1>
      <p>Your one-stop solution for learning and mentorship.</p>
    </div>

    <!-- Dynamic content based on routes -->
    <router-view />

    <!-- Footer with DOE logo -->
    <footer class="footer">
      <img src="@/assets/DOE.png" alt="DOE Logo" class="footer-logo" />
    </footer>
  </div>
</template>

<script>
import NavbarComp from "./components/NavbarComp.vue";

export default {
  components: {
    NavbarComp,
  },
};
</script>

<style>
/* General styles */
body {
  margin: 0;
  padding: 0;
  font-family: "Lexend", sans-serif;
  font-weight: 300;
  /* Set the default font to Lexend Light */
  background-color: #f9f9f9; /* Ensure the overall page background is white */
}

#app {
  min-height: 100vh; /* Ensure the app covers the full height */
  display: flex;
  flex-direction: column;
}

/* Header styles */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #07d531; /* Blue background for the header */
  padding: 10px 20px;
  color: white; /* White text for contrast */
}

.header-image {
  width: 100px; /* Adjust width of the images */
  height: auto; /* Maintain aspect ratio */
}

.header-image.left {
  margin-right: auto; /* Align the left image to the start */
}

.header-image.right {
  margin-left: auto; /* Align the right image to the end */
}

/* Hero section styles */
.hero {
  text-align: center;
  margin: 20px 0; /* Add some spacing around the hero section */
  padding: 20px;
  background-color: #f9f9f9; /* Optional: Light background to make it stand out */
  border-radius: 8px; /* Optional: Add some rounded corners */
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333; /* Darker color for contrast */
}

.hero p {
  font-size: 1.25rem;
  color: #555; /* Slightly lighter color for the description */
}

/* Footer styles */
#app {
  min-height: 100vh; /* Ensure the app covers the full height */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Ensures the footer is pushed to the bottom */
}

.footer {
  margin-top: auto; /* Pushes the footer to the bottom */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 0; /* Reduce padding to bring the logo closer to the bottom */
  background-color: #f9f9fb; /* Explicitly set footer background to white */
  border-top: 1px solid #ddd; /* Optional: Add a border to separate the footer */
}

.footer-logo {
  width: 40%; /* Stretch image to fit horizontally */
  max-width: 1200px; /* Add a max width to prevent excessive stretching */
  height: auto; /* Maintain aspect ratio */
  margin: 0; /* Remove any additional margins */
}

</style>
