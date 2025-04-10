<template>
  <div class="page-container">
    <!-- <Header /> -->
    <div class="landing-page">
      <h1>Welcome to the Interactive Malayalam Learning App</h1>
      
      <div class="camera-section">
        <AROverlay
          v-if="showAR"
          @exit-ar="handleARExit"
          @object-detected="handleObjectDetected"
        />
        
        <div v-if="showCamera" class="camera-container">
          <video ref="video" autoplay playsinline class="camera-view"></video>
          <div class="controls-container">
            <button @click="captureImage" class="capture-button">Capture</button>
            <button @click="closeCamera" class="close-button">Close Camera</button>
          </div>
        </div>
      </div>
      
      <!-- Rest of your existing template -->
      <div v-show="!showAR" class="main-content">
        <!-- <h1>Welcome to the Interactive Malayalam Learning App</h1> -->
        
        <!-- Scan Options -->
        <div class="scan-options">
          <button @click="startAR" class="scan-button ar">
            Start AR Scan
          </button>
          <button @click="startCamera" class="scan-button">Use Camera</button>
          <button @click="startFileUpload" class="scan-button">
            Upload Image
          </button>
        </div>

        <!-- Results view -->
        <div v-if="scanResult" class="result-container">
          <h2>Scan Result:</h2>
          <div class="result-card">
            <img :src="capturedImage" alt="Scanned object" class="preview-image"/>
            <p class="object-name">English: {{ scanResult.name }}</p>
            <p class="translation">Malayalam: {{ scanResult.malayalam_translation }}</p>
            <div class="action-buttons">
              <button @click="startPractice" class="practice-button">Practice</button>
              <button @click="resetScan" class="reset-button">New Scan</button>
            </div>
          </div>
        </div>
    
        <!-- History Section -->
        <div class="history-section">
          <h2>Scan History</h2>
          <div v-if="scanHistory && scanHistory.length > 0" class="history-list">
            <div v-for="item in scanHistory" :key="item.id || item.object_id" class="history-item">
              <div class="history-content">
                <p><strong>Object:</strong> {{ item.name || item.object_name }}</p>
                <p><strong>Translation:</strong> {{ item.malayalam_translation }}</p>
                <p class="timestamp">{{ new Date(item.timestamp).toLocaleString() }}</p>
              </div>
              <button @click="startPracticeFromHistory(item)" class="practice-button">Practice</button>
            </div>
          </div>
          <p v-else>No scan history available</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AROverlay from './AROverlay.vue'
import Header from './Header.vue'

const DEBUG = true; // Enable/disable debug logging

function log(...args) {
  if (DEBUG) {
    console.log(...args);
  }
}

const fetchHistory = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/history', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching history:', error);
    throw error;
  }
};

export default {
  name: 'LandingPage',
  components: {
    AROverlay,
    Header
  },
  data() {
    return {
      showCamera: false,
      stream: null,
      scanResult: null,
      capturedImage: null,
      scanHistory: [],
      showAR: false
    }
  },
  
  async mounted() {
    console.log('Component mounted'); // Debug log
    await this.loadHistory();
  },

  methods: {
    async startCamera() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: 'environment' } 
        });
        this.showCamera = true;
        this.$nextTick(() => {
          this.$refs.video.srcObject = this.stream;
        });
      } catch (error) {
        console.error('Camera error:', error);
        alert('Could not access camera. Please check permissions.');
      }
    },

    async captureImage() {
      const video = this.$refs.video;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const context = canvas.getContext('2d');
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // Convert canvas to blob
      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');
        
        try {
          const response = await fetch('http://127.0.0.1:8000/api/recognize_object', {
            method: 'POST',
            body: formData,
            mode: 'cors',
            headers: {
              'Accept': 'application/json',
            },
          });

          if (!response.ok) {
            throw new Error(`Failed to recognize object: ${response.status}`);
          }

          this.scanResult = await response.json();
          this.capturedImage = canvas.toDataURL('image/jpeg');
          this.closeCamera();
        } catch (error) {
          console.error('Recognition error:', error);
          alert('Failed to process image. Please try again.');
        }
      }, 'image/jpeg');
    },

    closeCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
        this.stream = null;
      }
      this.showCamera = false;
    },

    async startFileUpload() {
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = 'image/*';
      
      fileInput.onchange = async (event) => {
        const file = event.target.files[0];
        if (file) {
          const formData = new FormData();
          formData.append('image', file);

          try {
            const response = await fetch('http://127.0.0.1:8000/api/recognize_object', {
              method: 'POST',
              body: formData,
              mode: 'cors',
              headers: {
                'Accept': 'application/json',
              },
            });

            if (!response.ok) {
              throw new Error(`Failed to recognize object: ${response.status}`);
            }

            const result = await response.json();
            this.scanResult = result;
            this.capturedImage = URL.createObjectURL(file);
            
            // Reload history after successful scan
            await this.loadHistory();
          } catch (error) {
            console.error('Scanning error:', error);
            alert('Failed to process image. Please try again.');
          }
        }
      };

      fileInput.click();
    },

    // Add history loading method
    async loadHistory() {
      try {
        log('Loading history...');
        const data = await fetchHistory();
        log('History data received:', data);

        if (!data || (!Array.isArray(data) && !Array.isArray(data.items))) {
          throw new Error('Invalid history data format');
        }

        this.scanHistory = Array.isArray(data) ? data : data.items;
        log('History updated:', this.scanHistory);
      } catch (error) {
        console.error('Error loading history:', error);
        this.scanHistory = [];
      }
    },

    startPractice() {
      if (this.scanResult) {
        console.log('Navigating with:', this.scanResult);
        this.$router.push({
          name: 'Practice',
          query: {
            id: this.scanResult.id,
            name: this.scanResult.name,
            malayalam_translation: this.scanResult.malayalam_translation
          }
        });
      }
    },

    resetScan() {
      this.scanResult = null;
      this.capturedImage = null;
    },

    // Add method to handle practice from history
    startPracticeFromHistory(item) {
      console.log('Navigating from history:', item); // Debug log
      this.$router.push({
        name: 'Practice',
        query: {
          id: item.id,
          name: item.name,
          malayalam_translation: item.malayalam_translation
        }
      });
    },

    // Add new AR methods
    async startAR() {
      try {
        // Check for AR and camera support
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          throw new Error('AR requires camera access');
        }
        
        // Request camera permissions
        await navigator.mediaDevices.getUserMedia({ 
          video: { 
            facingMode: 'environment'
          } 
        });
        
        this.showAR = true;
        
      } catch (error) {
        console.error('AR initialization error:', error);
        alert('Could not start AR. Please check camera permissions.');
      }
    },
    
    handleARExit() {
      this.showAR = false;
      this.scanResult = null;
      this.loadHistory(); // Refresh history after AR session
    },

    handleObjectDetected(result) {
      this.scanResult = result;
      this.showAR = false; // Exit AR after successful detection
      this.loadHistory(); // Refresh history
    }
  }
}
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.landing-page {
  flex: 1;
  padding: 20px;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.camera-section {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  flex-shrink: 0; /* Prevent camera section from shrinking */
}

.camera-container {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 4/3;
}

.camera-view {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.controls-container {
  position: absolute;
  bottom: 10px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 10px;
}

/* Update button positioning */
.capture-button, 
.close-button {
  position: relative; /* Change from absolute to relative */
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 5px;
  z-index: 2;
}

.scan-options {
  margin-top: 20px;
}

.scan-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 5px;
}

.scan-button:hover {
  background-color: #45a049;
}

.scan-button.ar {
  background-color: #2196F3;
}

.scan-button.ar:hover {
  background-color: #1976D2;
}

.result-container {
  margin-top: 20px;
}

.result-card {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 20px;
  text-align: left;
  max-width: 400px;
  margin: 0 auto;
}

.preview-image {
  width: 100%;
  border-radius: 4px;
}

.object-name, .translation {
  font-size: 18px;
  margin: 10px 0;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}

.practice-button, .reset-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 5px;
}

.practice-button:hover, .reset-button:hover {
  background-color: #45a049;
}

.history-section {
  margin-top: 40px;
  padding: 20px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.history-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
}

.history-content {
  flex-grow: 1;
}

.history-content p {
  margin: 5px 0;
}

.timestamp {
  color: #666;
  font-size: 0.9em;
}

.practice-button {
  min-width: 100px;
}

/* Add to your existing styles */
.camera-section {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
}

/* ... rest of your existing styles ... */
</style>