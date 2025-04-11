<template>
  <div class="movie-container">
    <div class="search-section">
      <input 
        v-model="movieName" 
        placeholder="Enter movie name..."
        @keyup.enter="searchMovie"
        class="search-input"
      />
      <button @click="searchMovie" :disabled="loading" class="search-button">
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </div>

    <div v-if="movieData" class="result-section">
      <h2 class="movie-title">{{ movieData.movie_name }}</h2>
      
      <div class="plot-container">
        <div class="plot-column">
          <h3>English Plot</h3>
          <div class="plot-text english">
            {{ movieData.english_plot }}
          </div>
        </div>
        
        <div class="plot-column">
          <h3>മലയാളം പ്ലോട്ട്</h3>
          <div class="plot-text malayalam">
            {{ movieData.malayalam_plot }}
          </div>
          <div class="audio-controls">
            <button 
              @click="toggleAudio" 
              class="audio-button"
              :class="{ 'playing': isPlaying }"
            >
              <span class="icon">{{ isPlaying ? '⏹' : '▶' }}</span>
              {{ isPlaying ? 'Stop' : 'Listen in Malayalam' }}
            </button>
            <div v-if="isPlaying" class="audio-progress">
              <div 
                class="progress-bar" 
                :style="{ width: `${audioProgress}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div class="chat-control">
        <button @click="showChat = !showChat" class="chat-toggle">
          {{ showChat ? 'Hide Chat' : 'Chat about the Movie' }}
        </button>
      </div>

      <div v-if="showChat" class="chat-section">
        <div class="chat-messages" ref="chatMessages">
          <div v-for="(msg, index) in chatMessages" 
               :key="index"
               :class="['message', msg.type]">
            <div v-if="msg.type === 'user'" class="user-message">
              {{ msg.text }}
            </div>
            <div v-else-if="msg.type === 'bot'" class="bot-message">
              <div class="response-english">{{ msg.english }}</div>
              <div class="response-malayalam">{{ msg.malayalam }}</div>
            </div>
            <div v-else-if="msg.type === 'error'" class="error-message">
              {{ msg.text }}
            </div>
          </div>
        </div>
        <div class="chat-input">
          <input 
            v-model="currentMessage" 
            placeholder="Chat in Manglish..."
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:8000/api';

export default {
  name: 'MoviePlotScreen',
  data() {
    return {
      movieName: '',
      movieData: null,
      loading: false,
      showChat: false,
      chatMessages: [],
      currentMessage: '',
      audioPlayer: null,
      isPlaying: false,
      audioProgress: 0
    }
  },
  methods: {
    async searchMovie() {
      if (!this.movieName) return;
      
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/movie_plot`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ movie_name: this.movieName })
        });
        
        if (!response.ok) throw new Error('Failed to fetch movie data');
        
        this.movieData = await response.json();
        this.showChat = false;
        this.chatMessages = [];
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to fetch movie data');
      } finally {
        this.loading = false;
      }
    },
    
    toggleAudio() {
      if (this.isPlaying) {
        this.stopAudio();
      } else {
        this.playAudio();
      }
    },
    playAudio() {
      if (!this.movieData?.audio_url) {
        console.error('No audio URL available');
        return;
      }

      // Remove the /api prefix from the URL
      const audioUrl = `http://localhost:8000${this.movieData.audio_url}`;
      console.log('Attempting to play:', audioUrl);

      if (this.audioPlayer) {
        this.stopAudio();
      }

      this.audioPlayer = new Audio(audioUrl);
      
      this.audioPlayer.onerror = (e) => {
        console.error('Audio error:', e);
        alert('Failed to load audio file. Please try searching for the movie again.');
        this.isPlaying = false;
      };

      this.audioPlayer.addEventListener('loadeddata', () => {
        console.log('Audio loaded successfully');
      });

      this.audioPlayer.play()
        .then(() => {
          this.isPlaying = true;
        })
        .catch(error => {
          console.error('Playback failed:', error);
          alert('Failed to play audio. Please try again.');
          this.isPlaying = false;
        });
    },
    stopAudio() {
      if (this.audioPlayer) {
        this.audioPlayer.pause();
        this.audioPlayer.currentTime = 0;
        this.audioPlayer = null;
      }
      this.isPlaying = false;
      this.audioProgress = 0;
    },
    
    async sendMessage() {
      if (!this.currentMessage || !this.movieData) return;
      
      const userMessage = this.currentMessage;
      this.chatMessages.push({ type: 'user', text: userMessage });
      this.currentMessage = '';
      
      try {
        // Remove one /api from the URL
        const response = await fetch(`${API_BASE_URL}/movie_chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            movie_id: this.movieData.movie_id,
            message: userMessage
          })
        });
        
        if (!response.ok) {
          console.error('Chat failed:', response.status);
          throw new Error('Chat failed');
        }
        
        const data = await response.json();
        this.chatMessages.push({ 
          type: 'bot', 
          english: data.english_response,
          malayalam: data.malayalam_response
        });
        
        this.$nextTick(() => {
          const chat = this.$refs.chatMessages;
          chat.scrollTop = chat.scrollHeight;
        });
      } catch (error) {
        console.error('Chat error:', error);
        this.chatMessages.push({
          type: 'error',
          text: 'Failed to get response. Please try again.'
        });
      }
    }
  },
  beforeUnmount() {
    this.stopAudio();
  }
}
</script>

<style scoped>
.movie-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-section {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #4CAF50;
  border-radius: 8px;
}

.movie-title {
  font-size: 2rem;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
}

.plot-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.plot-column {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.plot-column h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.plot-text {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 12px;
  min-height: 300px;
  font-size: 1.1rem;
  line-height: 1.8;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.plot-text.malayalam {
  font-size: 1.2rem;
  line-height: 2;
}

.audio-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.audio-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.audio-button.playing {
  background: #f44336;
}

.audio-button:hover {
  transform: scale(1.05);
}

.audio-progress {
  width: 100%;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #4CAF50;
  transition: width 0.1s linear;
}

.icon {
  font-size: 1.2rem;
}

.chat-control {
  text-align: center;
  margin: 20px 0;
}

.chat-toggle {
  padding: 12px 24px;
  background: #2196F3;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}

.chat-section {
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin: 10px 0;
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 80%;
  font-size: 1rem;
}

.message.user {
  background: #e3f2fd;
  margin-left: auto;
}

.message.bot {
  background: #f5f5f5;
  margin-right: auto;
}

.message.error {
  background: #ffebee;
  color: #b71c1c;
  margin-right: auto;
}

.bot-message {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.response-english {
  font-size: 0.9rem;
  color: #333;
}

.response-malayalam {
  font-size: 1rem;
  color: #1a237e;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 15px;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

button {
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background: #45a049;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .plot-container {
    grid-template-columns: 1fr;
  }
}
</style>