<template>
  <div class="landing-page">
    <h1>Welcome to the AR Language Learning App</h1>
    <button @click="startScanning" class="scan-button">Start Scanning</button>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  methods: {
    startScanning() {
      console.log('Scanning started!')
    }
  }
}
</script>

<style scoped>
.landing-page {
  padding: 20px;
  text-align: center;
}

.scan-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.scan-button:hover {
  background-color: #45a049;
}
</style>