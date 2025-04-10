<template>
  <header class="app-header">
    <div class="nav-links">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/alphabets" class="nav-link">Learn Alphabets</router-link>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  background-color: #4CAF50;
  padding: 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-links {
  display: flex;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}
</style>