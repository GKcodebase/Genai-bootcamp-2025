<template>
  <div class="alphabet-container">
    <h1>Malayalam Alphabet Learning</h1>
    <div class="alphabet-grid">
      <div 
        v-for="alphabet in alphabets" 
        :key="alphabet.id" 
        class="alphabet-card"
        @click="selectAlphabet(alphabet)"
      >
        <h2>{{ alphabet.malayalam_char }}</h2>
        <p>{{ alphabet.english_transliteration }}</p>
        <button 
          @click.stop="playAudio(alphabet.audio_url)" 
          class="play-button"
        >
          <span class="play-icon">▶</span>
        </button>
      </div>
    </div>

    <div v-if="selectedAlphabet" class="alphabet-detail">
      <div class="selected-header">
        <h3>{{ selectedAlphabet.malayalam_char }}</h3>
        <div class="pronunciation-section">
          <p class="transliteration"> pronounced as - {{ selectedAlphabet.english_transliteration }}</p>
          <button 
            @click="playAudio(selectedAlphabet.audio_url)"
            class="audio-button"
          >
            Listen to Pronunciation
          </button>
        </div>
      </div>
      
      <div class="word-list">
        <div v-for="(word, index) in generatedWords" :key="index" class="word-item">
          <div class="word-details">
            <span class="malayalam-word">{{ word.word }}</span>
            <span class="pronunciation">{{ word.pronunciation }}</span>
            <span class="translation">"{{ word.english_translation }}"</span>
          </div>
        </div>
      </div>
      
      <button @click="generateNewWords" class="generate-button">
        Generate New Words
      </button>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:8000';

export default {
  name: 'AlphabetScreen',
  data() {
    return {
      alphabets: [],
      selectedAlphabet: null,
      generatedWords: []
    }
  },
  async created() {
    try {
      const response = await fetch('/api/alphabets')
      this.alphabets = await response.json()
    } catch (error) {
      console.error('Failed to fetch alphabets:', error)
    }
  },
  methods: {
    async selectAlphabet(alphabet) {
      this.selectedAlphabet = alphabet
      await this.generateNewWords()
    },
    async generateNewWords() {
      if (!this.selectedAlphabet) return;
      try {
        const response = await fetch(`${API_BASE_URL}/api/generate_words?alphabet_id=${this.selectedAlphabet.id}`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        this.generatedWords = data.words;
      } catch (error) {
        console.error('Failed to generate words:', error);
      }
    },
    playAudio(audioUrl) {
      if (!audioUrl) return;
      const fullUrl = `${API_BASE_URL}${audioUrl}`;
      const audio = new Audio(fullUrl);
      
      audio.onerror = (e) => {
        console.error('Audio playback error:', e);
      };
      
      audio.play().catch(e => {
        console.error('Playback failed:', e);
      });
    }
  }
}
</script>

<style scoped>
.alphabet-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.alphabet-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.alphabet-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  text-align: center;
  cursor: pointer;
  transition: transform 0.2s;
  margin: 10px;
}

.alphabet-card:hover {
  transform: scale(1.05);
  background-color: #f5f5f5;
}

.alphabet-detail {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 20px;
}

.word-list {
  margin: 20px 0;
}

.word-item {
  margin: 1rem 0;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.word-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.malayalam-word {
  font-size: 1.5rem;
  font-weight: bold;
}

.pronunciation {
  color: #666;
  font-style: italic;
}

.translation {
  color: #2c3e50;
}

.transliteration {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.audio-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.audio-button:hover {
  background-color: #45a049;
}

.generate-button {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}

.play-button {
  background: transparent;
  border: none;
  color: #4CAF50;
  cursor: pointer;
  padding: 5px;
  margin-top: 5px;
  border-radius: 50%;
  transition: all 0.2s;
}

.play-button:hover {
  background: #4CAF50;
  color: white;
}

.play-icon {
  font-size: 1.2rem;
}

.pronunciation-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
}

.selected-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
}
</style>