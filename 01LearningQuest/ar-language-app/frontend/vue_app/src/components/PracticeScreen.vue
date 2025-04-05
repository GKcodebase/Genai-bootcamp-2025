<template>
  <div class="practice-screen">
    <h1>Practice: {{ name }}</h1>
    
    <!-- Writing Practice -->
    <div class="practice-section">
      <h2>Writing Practice</h2>
      <p>Type the Malayalam word for "{{ name }}":</p>
      <input 
        v-model="writtenAnswer" 
        type="text" 
        class="writing-input"
        :placeholder="'Type here...'"
      />
      <button @click="checkWriting" class="check-button">Check</button>
      <p v-if="writingResult" :class="['result', writingResult.correct ? 'correct' : 'incorrect']">
        {{ writingResult.message }}
      </p>
    </div>

    <!-- Speaking Practice -->
    <div class="practice-section">
      <h2>Speaking Practice</h2>
      <p>Listen and repeat the word:</p>
      <button @click="playAudio" class="audio-button">
        Play Audio
      </button>
      <div class="recording-section">
        <button 
          @click="toggleRecording" 
          :class="['record-button', isRecording ? 'recording' : '']"
        >
          {{ isRecording ? 'Stop Recording' : 'Start Recording' }}
        </button>
        <button 
          v-if="audioBlob" 
          @click="submitSpeaking" 
          class="submit-button"
        >
          Submit
        </button>
      </div>
      <p v-if="speakingResult" :class="['result', speakingResult.correct ? 'correct' : 'incorrect']">
        {{ speakingResult.message }}
      </p>
    </div>

    <!-- Listening Practice -->
    <div class="practice-section">
      <h2>Listening Practice</h2>
      <p>Listen to the phrase and write it down:</p>
      <button @click="playPhrase" class="audio-button">
        Play Phrase
      </button>
      <textarea 
        v-model="phraseAnswer" 
        class="phrase-input"
        :placeholder="'Write the phrase you hear...'"
      ></textarea>
      <button @click="checkPhrase" class="check-button">Check</button>
      <p v-if="phraseResult" :class="['result', phraseResult.correct ? 'correct' : 'incorrect']">
        {{ phraseResult.message }}
      </p>
    </div>

    <div class="navigation-buttons">
      <button @click="goBack" class="back-button">Back to Scan</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PracticeScreen',
  data() {
    return {
      id: null,
      name: '',
      malayalam_translation: '',
      writtenAnswer: '',
      writingResult: null,
      isRecording: false,
      audioBlob: null,
      mediaRecorder: null,
      audioChunks: [],
      speakingResult: null,
      phraseAnswer: '',
      phraseResult: null,
      generatedPhrase: null
    }
  },

  created() {
    // Get data from route query
    const query = this.$route.query;
    console.log('Route query:', query);
    
    // Set the data properties
    this.updateData(query);

    // Generate exercise phrase if we have an ID
    if (this.id) {
      this.generateExercise(this.id);
    }
  },

  watch: {
    '$route.query': {
      immediate: true,
      handler(newQuery) {
        this.updateData(newQuery);
      }
    }
  },

  methods: {
    updateData(query) {
      if (!query) return;
      
      this.id = query.id ? parseInt(query.id) : null;
      this.name = query.name || '';
      this.malayalam_translation = query.malayalam_translation || '';
      
      console.log('Updated component data:', {
        id: this.id,
        name: this.name,
        malayalam_translation: this.malayalam_translation
      });
    },
    async generateExercise(objectId) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/generate_exercise?object_id=${objectId}`);
        if (response.ok) {
          this.generatedPhrase = await response.json();
        }
      } catch (error) {
        console.error('Error generating exercise:', error);
      }
    },

    // Update checkWriting to use correct property name
    async checkWriting() {
      if (this.writtenAnswer === this.malayalam_translation) {
        this.writingResult = {
          correct: true,
          message: 'Correct! Well done!'
        };
      } else {
        this.writingResult = {
          correct: false,
          message: `Incorrect. The correct answer is: ${this.malayalam_translation}`
        };
      }
    },

    // Update playAudio to use correct property name
    async playAudio() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/generate_audio?text=${encodeURIComponent(this.malayalam_translation)}`);
        if (response.ok) {
          const data = await response.json();
          const audio = new Audio(data.audio_url);
          audio.play();
        }
      } catch (error) {
        console.error('Error playing audio:', error);
      }
    },

    async toggleRecording() {
      if (!this.isRecording) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          this.audioChunks = [];
          this.mediaRecorder = new MediaRecorder(stream);
          
          this.mediaRecorder.ondataavailable = (event) => {
            this.audioChunks.push(event.data);
          };

          this.mediaRecorder.onstop = () => {
            this.audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
          };

          this.mediaRecorder.start();
          this.isRecording = true;
        } catch (error) {
          console.error('Error starting recording:', error);
        }
      } else {
        this.mediaRecorder.stop();
        this.isRecording = false;
      }
    },

    async submitSpeaking() {
      if (!this.audioBlob) return;

      const formData = new FormData();
      formData.append('audio', this.audioBlob);

      try {
        const response = await fetch('http://127.0.0.1:8000/api/speaking_test', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const result = await response.json();
          this.speakingResult = {
            correct: result.correct,
            message: result.correct ? 'Correct pronunciation!' : 'Try again'
          };
        }
      } catch (error) {
        console.error('Error submitting speaking test:', error);
      }
    },

    async playPhrase() {
      if (this.generatedPhrase?.audio_url) {
        const audio = new Audio(this.generatedPhrase.audio_url);
        audio.play();
      }
    },

    async checkPhrase() {
      if (this.phraseAnswer === this.generatedPhrase?.phrase) {
        this.phraseResult = {
          correct: true,
          message: 'Correct! Perfect understanding!'
        };
      } else {
        this.phraseResult = {
          correct: false,
          message: `Incorrect. The phrase was: ${this.generatedPhrase?.phrase}`
        };
      }
    },

    goBack() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.practice-screen {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.practice-section {
  margin: 30px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.writing-input, .phrase-input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.audio-button, .check-button, .record-button, .submit-button, .back-button {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.audio-button {
  background-color: #2196F3;
  color: white;
}

.check-button {
  background-color: #4CAF50;
  color: white;
}

.record-button {
  background-color: #f44336;
  color: white;
}

.record-button.recording {
  background-color: #b71c1c;
  animation: pulse 1.5s infinite;
}

.result {
  margin-top: 10px;
  padding: 10px;
  border-radius: 4px;
}

.result.correct {
  background-color: #dff0d8;
  color: #3c763d;
}

.result.incorrect {
  background-color: #f2dede;
  color: #a94442;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.navigation-buttons {
  margin-top: 30px;
  text-align: center;
}

.back-button {
  background-color: #757575;
  color: white;
}
</style>