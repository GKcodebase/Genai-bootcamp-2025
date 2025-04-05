<template>
  <div>
    <h1>Practice</h1>
    <div>
      <h2>Writing</h2>
      <input v-model="userInput" placeholder="Type the Malayalam word" />
      <button @click="checkWriting">Submit</button>
    </div>
    <div>
      <h2>Speaking</h2>
      <button @click="startSpeakingTest">Start Speaking Test</button>
    </div>
    <div>
      <h2>Listening</h2>
      <button @click="playAudio">Play Audio</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: "",
    };
  },
  methods: {
    checkWriting() {
      // Validate user input
      console.log("User input:", this.userInput);
    },
    startSpeakingTest() {
      // Trigger speaking test
      console.log("Speaking test started");
    },
    playAudio() {
      // Play audio for listening exercise
      console.log("Playing audio");
    },
  },
};
</script>