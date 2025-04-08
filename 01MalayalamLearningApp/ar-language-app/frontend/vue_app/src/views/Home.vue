<template>
  <div class="home">
    <h1>Welcome to Your Vue.js App</h1>
    <HelloWorld msg="This is your home page!" />
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}
</style>