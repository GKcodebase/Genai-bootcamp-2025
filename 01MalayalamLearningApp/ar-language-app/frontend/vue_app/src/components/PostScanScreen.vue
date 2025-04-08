<!-- filepath: /Users/gokulg.k/Documents/GitHub/free-genai-bootcamp-2025/01LearningQuest/frontend/vue_app/src/components/PostScanScreen.vue -->
<template>
  <div>
    <h1>Scan Result</h1>
    <div v-if="scanResult">
      <p><strong>Object:</strong> {{ scanResult.object_name }}</p>
      <p><strong>Translation:</strong> {{ scanResult.malayalam_translation }}</p>
      <button @click="goToPractice">Practice</button>
      <button @click="cancel">Cancel</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      scanResult: null,
    };
  },
  methods: {
    goToPractice() {
      this.$router.push("/practice");
    },
    cancel() {
      this.$router.push("/");
    },
  },
  mounted() {
    // Simulate scanning and fetch result
    fetch("/api/recognize_object", { method: "POST" })
      .then((response) => response.json())
      .then((data) => {
        this.scanResult = data;
      });
  },
};
</script>