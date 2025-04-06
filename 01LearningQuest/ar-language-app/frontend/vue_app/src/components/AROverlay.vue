<template>
  <div class="ar-container">
    <!-- Camera Section -->
    <div class="camera-section">
      <div v-if="isLoading" class="loading-overlay">
        <p>Initializing AR Camera...</p>
      </div>

      <div class="camera-container">
        <video 
          ref="videoFeed" 
          class="camera-view" 
          autoplay 
          playsinline
          @loadedmetadata="onVideoLoad"
        ></video>

        <!-- AR Translation Overlay -->
        <div v-if="detectedObject" class="ar-overlay">
          <div class="translation-box">
            <p class="malayalam-text">{{ detectedObject.malayalam_translation }}</p>
            <p class="english-text">{{ detectedObject.name }}</p>
          </div>
        </div>

        <!-- Detection Frame -->
        <div class="detection-frame" :class="{ active: isDetecting }">
          <div class="corner top-left"></div>
          <div class="corner top-right"></div>
          <div class="corner bottom-left"></div>
          <div class="corner bottom-right"></div>
        </div>
      </div>

      <!-- Simple Translation Display -->
      <div v-if="detectedObject" class="translation-display">
        <div class="translation-content">
          <div class="word-pair">
            <span class="english-word">{{ detectedObject.name }}</span>
            <span class="arrow">→</span>
            <span class="malayalam-word">{{ detectedObject.malayalam_translation }}</span>
          </div>
          <button @click="startPractice" class="practice-button">
            <span class="practice-icon">✏️</span>
            Practice Now
          </button>
        </div>
      </div>
    </div>

    <!-- Controls Section -->
    <div class="controls-section">
      <button 
        @click="toggleDetection" 
        class="control-button primary"
        :disabled="isCapturing"
      >
        {{ isCapturing ? 'Capturing...' : 'Detect Object' }}
      </button>
      <button @click="exitAR" class="control-button secondary">
        Exit AR
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AROverlay',
  data() {
    return {
      isLoading: true,
      isDetecting: false,
      isCapturing: false,
      detectedObject: null,
      mediaStream: null
    }
  },
  methods: {
    async initializeCamera() {
      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: 'environment',
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        });
        
        const videoElement = this.$refs.videoFeed;
        videoElement.srcObject = this.mediaStream;
      } catch (error) {
        console.error('Camera initialization error:', error);
        alert('Could not access camera. Please check permissions.');
        this.exitAR();
      }
    },

    onVideoLoad() {
      this.isLoading = false;
    },

    async toggleDetection() {
      if (this.isCapturing) return;
      
      try {
        this.isCapturing = true;
        this.isDetecting = true;
        
        const result = await this.captureAndDetect();
        console.log('Detection result:', result);
        
        if (result && result.name) {
          // Just update the local state, don't emit event
          this.detectedObject = {
            object_id: result.id,
            name: result.name,
            malayalam_translation: result.malayalam_translation
          };
          // Remove this line that was causing redirection
          // this.$emit('object-detected', this.detectedObject);
        } else {
          alert('No object detected. Please try again.');
        }
      } catch (error) {
        console.error('Detection error:', error);
        alert('Failed to detect object. Please try again.');
      } finally {
        this.isDetecting = false;
        this.isCapturing = false;
      }
    },

    async captureAndDetect() {
      const canvas = document.createElement('canvas');
      const video = this.$refs.videoFeed;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
      const formData = new FormData();
      formData.append('image', blob, 'detect.jpg');

      const response = await fetch('http://127.0.0.1:8000/api/recognize_object', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Detection failed');
      
      const result = await response.json();
      console.log('API Response:', result); // Debug log
      return result;
    },

    resetDetection() {
      this.detectedObject = null;
      this.isDetecting = false;
      this.isCapturing = false;
    },

    // Update startPractice to use router.push with state
    startPractice() {
      if (!this.detectedObject) return;
      
      this.$router.push({
        name: 'Practice',
        query: {
          id: this.detectedObject.object_id,
          name: this.detectedObject.name,
          malayalam_translation: this.detectedObject.malayalam_translation
        }
      });
    },

    async exitAR() {
      try {
        // Stop detection if running
        this.stopDetection();
        
        // Clean up camera resources
        if (this.mediaStream) {
          const tracks = this.mediaStream.getTracks();
          tracks.forEach(track => {
            track.stop();
            this.mediaStream.removeTrack(track);
          });
          this.mediaStream = null;
        }

        // Clear video element
        const videoElement = this.$refs.videoFeed;
        if (videoElement) {
          videoElement.srcObject = null;
        }

        // Reset all states
        this.detectedObject = null;
        this.isDetecting = false;
        this.isCapturing = false;
        
        // Emit exit event to parent
        this.$emit('exit-ar');
      } catch (error) {
        console.error('Error cleaning up AR:', error);
      }
    },

    stopDetection() {
      this.isDetecting = false;
      this.isCapturing = false;
    }
  },
  async mounted() {
    await this.initializeCamera();
  },
  beforeUnmount() {
    this.exitAR();
  }
}
</script>

<style scoped>
.ar-container {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.camera-section {
  position: relative;
  width: 100%;
}

.camera-container {
  position: relative;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  background: #000;
  aspect-ratio: 4/3;
}

.camera-view {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.ar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  pointer-events: none;
}

.translation-box {
  background: rgba(0, 0, 0, 0.8);
  padding: 12px 24px;
  border-radius: 12px;
  border: 2px solid rgba(76, 175, 80, 0.8);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.malayalam-text {
  color: #4CAF50;
  font-size: 32px;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.english-text {
  color: white;
  font-size: 16px;
  margin: 4px 0 0 0;
  opacity: 0.8;
}

.detection-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 60%;
  border: 2px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  z-index: 5;
}

.detection-frame.active {
  border-color: rgba(76, 175, 80, 0.8);
  box-shadow: 0 0 20px rgba(76, 175, 80, 0.3);
}

.corner {
  position: absolute;
  width: 24px;
  height: 24px;
  border: 3px solid #4CAF50;
}

.top-left {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.top-right {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

.bottom-left {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}

.bottom-right {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.controls-section {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.control-button {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
}

.control-button.primary {
  background-color: #4CAF50;
  color: white;
}

.control-button.secondary {
  background-color: #f44336;
  color: white;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  z-index: 3;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.translation-display {
  margin-top: 16px;
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.translation-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.word-pair {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
}

.english-word {
  color: #333;
  font-weight: 500;
}

.arrow {
  color: #666;
}

.malayalam-word {
  color: #4CAF50;
  font-size: 24px;
  font-weight: 500;
}

.practice-button {
  background-color: #2196F3;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.practice-button:hover {
  background-color: #1976D2;
  transform: translateY(-1px);
}

.practice-icon {
  font-size: 18px;
}
</style>