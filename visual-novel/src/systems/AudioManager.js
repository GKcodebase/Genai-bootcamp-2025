export default class AudioManager {
    constructor(scene) {
        this.scene = scene;
        this.bgMusic = null;
        this.clickSound = null;
        this.transitionSound = null;
        this.initialize();
    }

    initialize() {
        // Check if audio exists in cache before creating
        if (this.scene.cache.audio.exists('bgMusic')) {
            this.bgMusic = this.scene.sound.add('bgMusic', { 
                loop: true, 
                volume: 0.5 
            });
            console.log('Background music initialized');
        } else {
            console.warn('Background music not found in cache');
        }

        if (this.scene.cache.audio.exists('clickSound')) {
            this.clickSound = this.scene.sound.add('clickSound', { 
                loop: false, 
                volume: 0.3 
            });
        }

        if (this.scene.cache.audio.exists('transitionSound')) {
            this.transitionSound = this.scene.sound.add('transitionSound', { 
                loop: false, 
                volume: 0.4 
            });
        }
    }

    playBackgroundMusic() {
        if (this.bgMusic && !this.bgMusic.isPlaying) {
            console.log('Attempting to play background music');
            this.bgMusic.play();
        } else {
            console.warn('Background music not initialized or already playing');
        }
    }

    playClickSound() {
        if (this.clickSound) {
            this.clickSound.play();
        }
    }

    playTransitionSound() {
        if (this.transitionSound) {
            this.transitionSound.play();
        }
    }

    stopAll() {
        if (this.bgMusic) this.bgMusic.stop();
        if (this.clickSound) this.clickSound.stop();
        if (this.transitionSound) this.transitionSound.stop();
    }
}