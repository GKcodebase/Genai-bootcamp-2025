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
        :placeholder="'Type Malayalam word...'"
      />
      <button @click="checkWriting" class="check-button">Check</button>
      <p v-if="writingResult" :class="['result', writingResult.correct ? 'correct' : 'incorrect']">
        {{ writingResult.message }}
      </p>
    </div>

    <!-- Speaking Practice -->
    <div class="practice-section">
      <h2>Speaking Practice</h2>
      <div class="practice-steps">
        <div class="step">
          <p>1. Listen to the word:</p>
          <button 
            @click="playWordAudio" 
            class="audio-button"
            :disabled="isPlaying"
          >
            <span class="icon">{{ isPlaying ? '🔊' : '▶' }}</span>
            Play "{{ malayalam_translation }}"
          </button>
          <p v-if="audioError" class="error-message">{{ audioError }}</p>
        </div>
        
        <div class="step">
          <p>2. Record your pronunciation:</p>
          <div class="recording-controls">
            <button 
              @click="toggleRecording" 
              :class="['record-button', isRecording ? 'recording' : '']"
              :disabled="isVerifying"
            >
              {{ isRecording ? 'Stop Recording' : 'Start Recording' }}
            </button>
            <span v-if="isRecording" class="recording-indicator">Recording...</span>
          </div>
          
          <!-- Update the preview controls in the template -->
          <div v-if="audioBlob" class="preview-controls">
            <div class="audio-preview">
              <button 
                @click="togglePreviewPlayback" 
                class="preview-button"
                :class="{ 'playing': isPreviewPlaying }"
                :disabled="isVerifying"
              >
                <span class="icon">
                  {{ isPreviewPlaying ? '⏸' : '▶' }}
                </span>
                {{ isPreviewPlaying ? 'Pause' : 'Play Recording' }}
              </button>
              <div class="audio-wave" v-if="isPreviewPlaying">
                <div class="wave-bar" v-for="n in 5" :key="n"></div>
              </div>
            </div>
            <button 
              @click="submitSpeaking" 
              class="submit-button"
              :disabled="isVerifying"
            >
              {{ isVerifying ? 'Verifying...' : 'Submit Recording' }}
            </button>
          </div>
          
          <!-- Add loading spinner -->
          <div v-if="isVerifying" class="spinner-container">
            <div class="spinner"></div>
            <p>Verifying pronunciation...</p>
          </div>

          <!-- Add verification results display -->
          <div v-if="speakingResult" class="verification-results">
            <h3>Verification Results</h3>
            <div class="result-grid">
              <div class="result-item">
                <span class="label">Your Pronunciation:</span>
                <span class="value">{{ speakingResult.recognized_text }}</span>
                <span class="transliteration">({{ speakingResult.transliterated_recognized }})</span>
              </div>
              <div class="result-item">
                <span class="label">Expected:</span>
                <span class="value">{{ malayalam_translation }}</span>
                <span class="transliteration">({{ speakingResult.transliterated_expected }})</span>
              </div>
              <div class="confidence-meter">
                <div class="confidence-label">Accuracy:</div>
                <div class="confidence-bar">
                  <div 
                    class="confidence-fill" 
                    :style="{ width: `${speakingResult.confidence * 100}%` }"
                    :class="{ 
                      high: speakingResult.confidence >= 0.8,
                      medium: speakingResult.confidence >= 0.6 && speakingResult.confidence < 0.8,
                      low: speakingResult.confidence < 0.6 
                    }"
                  ></div>
                </div>
                <div class="confidence-value">{{ Math.round(speakingResult.confidence * 100) }}%</div>
              </div>
            </div>
            <p :class="['result-message', speakingResult.correct ? 'correct' : 'incorrect']">
              {{ speakingResult.correct ? 'Good job!' : 'Try again!' }}
            </p>
          </div>
        </div>
      </div>
      <div v-if="speakingResult" class="result-container">
        <p :class="['result', speakingResult.correct ? 'correct' : 'incorrect']">
          {{ speakingResult.message }}
        </p>
        <div class="confidence-meter">
          <div class="confidence-label">Confidence Score:</div>
          <div class="confidence-bar">
            <div 
              class="confidence-fill" 
              :style="{ width: `${speakingResult.confidence * 100}%` }"
              :class="{ 
                high: speakingResult.confidence >= 0.8,
                medium: speakingResult.confidence >= 0.5 && speakingResult.confidence < 0.8,
                low: speakingResult.confidence < 0.5 
              }"
            ></div>
          </div>
          <div class="confidence-value">{{ Math.round(speakingResult.confidence * 100) }}%</div>
        </div>
      </div>
    </div>

    <!-- Listening Practice -->
    <div class="practice-section">
      <h2>Listening Practice</h2>
      <div class="practice-steps">
        <div class="step">
          <h3>1. Listen to the phrase:</h3>
          <div class="phrase-container">
            <p class="malayalam-text">{{ generatedExercise.phrase }}</p>
            <p class="english-text">"{{ generatedExercise.english_translation }}"</p>
            <button 
              @click="playPhraseAudio" 
              class="audio-button"
              :disabled="isPhrasePlayback"
            >
              <span class="icon">{{ isPhrasePlayback ? '🔊' : '▶' }}</span>
              {{ isPhrasePlayback ? 'Playing...' : 'Play Phrase' }}
            </button>
            <p v-if="phraseError" class="error-message">{{ phraseError }}</p>
          </div>
        </div>
        
        <div class="step">
          <p>2. Write what you hear in Malayalam:</p>
          <textarea 
            v-model="phraseAnswer" 
            class="phrase-input"
            :placeholder="'Write the Malayalam phrase...'"
          ></textarea>
          <button 
            @click="checkPhrase" 
            class="check-button"
            :disabled="!phraseAnswer"
          >
            Check Answer
          </button>
        </div>
      </div>
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
      generatedExercise: {
        phrase: '',
        english_translation: '',
        audio_url: ''
      },
      recordingPreview: null,
      audioError: null,
      lastGeneratedAudioUrl: null,
      isVerifying: false,
      isPreviewPlaying: false,
      audioPlayer: null,
      audioCache: new Map(), // Cache for audio URLs
      isPlaying: false,
      isPhrasePlayback: false,
      phrasePlayer: null,
      phraseError: null
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
        if (!response.ok) {
          throw new Error('Failed to generate exercise');
        }
        
        const data = await response.json();
        this.generatedExercise = {
          phrase: data.phrase,
          english_translation: data.english_translation,
          audio_url: data.audio_url
        };
        
        console.log('Generated exercise:', this.generatedExercise);
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
      if (this.isPlaying) {
        // Stop current playback if playing
        if (this.audioPlayer) {
          this.audioPlayer.pause();
          this.audioPlayer.currentTime = 0;
          this.isPlaying = false;
          return;
        }
      }

      try {
        this.audioError = null;
        const text = this.malayalam_translation;
        
        // Check cache first
        let audioUrl = this.audioCache.get(text);
        
        if (!audioUrl) {
          // Generate new audio only if not in cache
          const response = await fetch(
            `http://127.0.0.1:8000/api/generate_audio?text=${encodeURIComponent(text)}`,
            { cache: 'force-cache' } // Use browser caching
          );
          
          if (!response.ok) {
            throw new Error('Failed to generate audio');
          }
          
          const data = await response.json();
          if (!data.audio_url) {
            throw new Error('No audio URL received');
          }
          
          audioUrl = data.audio_url;
          this.audioCache.set(text, audioUrl); // Cache the URL
        }

        // Create new audio player if needed
        if (!this.audioPlayer) {
          this.audioPlayer = new Audio();
          
          this.audioPlayer.onerror = (e) => {
            console.error('Audio playback error:', e);
            this.audioError = 'Failed to play audio. Please try again.';
            this.isPlaying = false;
          };
          
          this.audioPlayer.onended = () => {
            this.isPlaying = false;
          };
        }

        // Set new source and play
        this.audioPlayer.src = audioUrl;
        this.isPlaying = true;
        await this.audioPlayer.play();

      } catch (error) {
        console.error('Error playing audio:', error);
        this.audioError = error.message;
        this.isPlaying = false;
      }
    },

    async toggleRecording() {
      if (!this.isRecording) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
              sampleRate: 16000,  // Required for Whisper
              channelCount: 1,    // Mono audio
              echoCancellation: true,
              noiseSuppression: true
            }
          });
          
          this.audioChunks = [];
          this.mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'  // Use opus codec for better quality
          });
          
          this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
              this.audioChunks.push(event.data);
            }
          };

          this.mediaRecorder.onstop = () => {
            this.audioBlob = new Blob(this.audioChunks, { 
              type: 'audio/webm' 
            });
            if (this.recordingPreviewURL) {
              URL.revokeObjectURL(this.recordingPreviewURL);
            }
            this.recordingPreviewURL = URL.createObjectURL(this.audioBlob);
            this.recordingPreview = new Audio(this.recordingPreviewURL);
          };

          this.mediaRecorder.start();
          this.isRecording = true;
        } catch (error) {
          console.error('Error accessing microphone:', error);
          alert('Failed to access microphone. Please check permissions.');
        }
      } else {
        this.mediaRecorder.stop();
        this.isRecording = false;
        this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
      }
    },

    // Update the submitSpeaking method
    async submitSpeaking() {
      if (!this.audioBlob) {
        alert('Please record audio first');
        return;
      }

      this.isVerifying = true;
      try {
        const formData = new FormData();
        formData.append('audio', this.audioBlob, 'recording.webm');
        formData.append('expected_text', this.malayalam_translation);

        console.log('Submitting audio for verification...');
        console.log('Expected text:', this.malayalam_translation);

        const response = await fetch('http://127.0.0.1:8000/api/speaking_test', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Failed to verify speech');
        }

        const result = await response.json();
        console.log('Speech verification result:', result);

        // Map all properties from the API response
        this.speakingResult = {
          recognized_text: result.recognized_text,
          transliterated_recognized: result.transliterated_recognized,
          transliterated_expected: result.transliterated_expected,
          correct: result.correct,
          confidence: result.confidence,
          message: result.correct 
            ? `Correct! Your pronunciation matches (${Math.round(result.confidence * 100)}% confidence)` 
            : `Try again. Your pronunciation needs improvement (${Math.round(result.confidence * 100)}% confidence)`
        };

      } catch (error) {
        console.error('Error submitting speaking test:', error);
        this.speakingResult = {
          recognized_text: '',
          transliterated_recognized: '',
          transliterated_expected: '',
          correct: false,
          confidence: 0,
          message: `Error: ${error.message}`
        };
      } finally {
        this.isVerifying = false;
      }
    },

    async playPhrase() {
      if (this.generatedExercise?.audio_url) {
        const audio = new Audio(this.generatedExercise.audio_url);
        await audio.play();
      }
    },

    async checkPhrase() {
      if (!this.phraseAnswer || !this.generatedExercise?.phrase) return;
      
      if (this.phraseAnswer === this.generatedExercise.phrase) {
        this.phraseResult = {
          correct: true,
          message: 'Correct! Perfect understanding!'
        };
      } else {
        this.phraseResult = {
          correct: false,
          message: `Incorrect. The phrase was: ${this.generatedExercise.phrase}`
        };
      }
    },

    goBack() {
      this.$router.push('/');
    },

    // Add new method for preview playback
    togglePreviewPlayback() {
      if (!this.recordingPreview) return;
      
      if (this.isPreviewPlaying) {
        this.recordingPreview.pause();
        this.recordingPreview.currentTime = 0;
        this.isPreviewPlaying = false;
      } else {
        this.recordingPreview.play();
        this.isPreviewPlaying = true;
        
        // Handle playback completion
        this.recordingPreview.onended = () => {
          this.isPreviewPlaying = false;
        };
      }
    },

    // For playing single word pronunciation
    async playWordAudio() {
      if (this.isPlaying) {
        if (this.audioPlayer) {
          this.audioPlayer.pause();
          this.audioPlayer.currentTime = 0;
          this.isPlaying = false;
          return;
        }
      }

      try {
        this.audioError = null;
        const text = this.malayalam_translation;
        
        let audioUrl = this.audioCache.get(text);
        
        if (!audioUrl) {
          const response = await fetch(
            `http://127.0.0.1:8000/api/generate_audio?text=${encodeURIComponent(text)}`,
            { cache: 'force-cache' }
          );
          
          if (!response.ok) {
            throw new Error('Failed to generate audio');
          }
          
          const data = await response.json();
          if (!data.audio_url) {
            throw new Error('No audio URL received');
          }
          
          audioUrl = data.audio_url;
          this.audioCache.set(text, audioUrl);
        }

        if (!this.audioPlayer) {
          this.audioPlayer = new Audio();
          this.audioPlayer.onended = () => {
            this.isPlaying = false;
          };
        }

        this.audioPlayer.src = audioUrl;
        this.isPlaying = true;
        await this.audioPlayer.play();

      } catch (error) {
        console.error('Error playing word audio:', error);
        this.audioError = error.message;
        this.isPlaying = false;
      }
    },

    // For playing practice phrase
    async playPhraseAudio() {
      if (this.isPhrasePlayback) {
        if (this.phrasePlayer) {
          this.phrasePlayer.pause();
          this.phrasePlayer.currentTime = 0;
          this.isPhrasePlayback = false;
          return;
        }
      }

      try {
        if (!this.generatedExercise?.audio_url) {
          throw new Error('No phrase audio available');
        }

        if (!this.phrasePlayer) {
          this.phrasePlayer = new Audio();
          this.phrasePlayer.onended = () => {
            this.isPhrasePlayback = false;
          };
        }

        this.phrasePlayer.src = this.generatedExercise.audio_url;
        this.isPhrasePlayback = true;
        await this.phrasePlayer.play();

      } catch (error) {
        console.error('Error playing phrase audio:', error);
        this.phraseError = error.message;
        this.isPhrasePlayback = false;
      }
    },

    // Clean up audio resources when component is destroyed
    beforeDestroy() {
      if (this.audioPlayer) {
        this.audioPlayer.pause();
        this.audioPlayer = null;
      }
      if (this.phrasePlayer) {
        this.phrasePlayer.pause();
        this.phrasePlayer = null;
      }
      this.audioCache.clear();
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

.practice-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step {
  padding: 15px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.writing-input, .phrase-input {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.writing-input:focus, .phrase-input:focus {
  border-color: #2196F3;
  outline: none;
}

.recording-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.recording-indicator {
  color: #f44336;
  font-weight: bold;
  animation: blink 1s infinite;
}

@keyframes blink {
  50% { opacity: 0; }
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

.result-container {
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  background-color: #f5f5f5;
}

.confidence-meter {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.confidence-label {
  font-size: 14px;
  color: #666;
  min-width: 120px;
}

.confidence-bar {
  flex-grow: 1;
  height: 12px;
  background-color: #eee;
  border-radius: 6px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.confidence-fill.high {
  background-color: #4CAF50;
}

.confidence-fill.medium {
  background-color: #FFC107;
}

.confidence-fill.low {
  background-color: #F44336;
}

.confidence-value {
  min-width: 50px;
  text-align: right;
  font-weight: bold;
  color: #333;
}

.correct {
  color: #4CAF50;
}

.incorrect {
  color: #F44336;
}

.spinner-container {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 4px solid #ddd;
  border-top: 4px solid #2196F3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.audio-preview {
  display: flex;
  align-items: center;
  gap: 15px;
  background: #f0f0f0;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.preview-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-button:hover {
  background-color: #45a049;
}

.preview-button.playing {
  background-color: #ff9800;
}

.preview-button .icon {
  font-size: 20px;
}

.audio-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 30px;
}

.wave-bar {
  width: 3px;
  background-color: #2196F3;
  animation: wave 0.5s ease infinite;
}

.wave-bar:nth-child(2) { animation-delay: 0.1s; }
.wave-bar:nth-child(3) { animation-delay: 0.2s; }
.wave-bar:nth-child(4) { animation-delay: 0.3s; }
.wave-bar:nth-child(5) { animation-delay: 0.4s; }

@keyframes wave {
  0%, 100% { height: 8px; }
  50% { height: 25px; }
}

.audio-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.audio-button:hover {
  background-color: #1976D2;
}

.audio-button:disabled {
  background-color: #BDBDBD;
  cursor: not-allowed;
}

.audio-button::before {
  content: '🔊';
  font-size: 20px;
}

.verification-results {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.result-grid {
  display: grid;
  gap: 15px;
  margin: 15px 0;
}

.result-item {
  display: grid;
  gap: 5px;
}

.label {
  color: #6c757d;
  font-size: 0.9em;
}

.value {
  font-size: 1.2em;
  font-weight: 500;
}

.transliteration {
  color: #6c757d;
  font-style: italic;
}

.confidence-meter {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.confidence-bar {
  flex-grow: 1;
  height: 12px;
  background: #e9ecef;
  border-radius: 6px;
  overflow: hidden;
}

.confidence-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.confidence-fill.high {
  background-color: #28a745;
}

.confidence-fill.medium {
  background-color: #ffc107;
}

.confidence-fill.low {
  background-color: #dc3545;
}

.result-message {
  margin-top: 15px;
  text-align: center;
  font-weight: 500;
}

.result-message.correct {
  color: #28a745;
}

.result-message.incorrect {
  color: #dc3545;
}

.confidence-label {
  min-width: 70px;
  color: #6c757d;
}

.confidence-value {
  min-width: 50px;
  text-align: right;
  font-weight: 500;
}

.phrase-container {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.malayalam-text {
  font-size: 1.5em;
  margin-bottom: 8px;
  color: #2c3e50;
}

.english-text {
  font-size: 1em;
  color: #6c757d;
  font-style: italic;
  margin-bottom: 15px;
}

.audio-button {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.audio-button:hover {
  background-color: #45a049;
}

.audio-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.icon {
  font-size: 1.2em;
}
</style>