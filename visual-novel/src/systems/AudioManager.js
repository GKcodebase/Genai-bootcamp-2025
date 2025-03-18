export default class AudioManager {
    constructor(scene) {
        this.scene = scene;
        this.setupAudio();
    }

    setupAudio() {
        try {
            // Background music
            if (this.scene.cache.audio.exists('bgMusic')) {
                this.bgMusic = this.scene.sound.add('bgMusic', {
                    loop: true,
                    volume: 0.5
                });
            }

            // Click sound
            if (this.scene.cache.audio.exists('clickSound')) {
                this.clickSound = this.scene.sound.add('clickSound', {
                    loop: false,
                    volume: 0.3
                });
            }

            // Transition sound
            if (this.scene.cache.audio.exists('transitionSound')) {
                this.transitionSound = this.scene.sound.add('transitionSound', {
                    loop: false,
                    volume: 0.4
                });
            }
        } catch (error) {
            console.error('Error setting up audio:', error);
        }
    }

    playMusic() {
        if (this.bgMusic && !this.bgMusic.isPlaying) {
            try {
                this.bgMusic.play();
            } catch (error) {
                console.error('Error playing background music:', error);
            }
        }
    }

    playClickSound() {
        if (this.clickSound) {
            try {
                this.clickSound.play();
            } catch (error) {
                console.error('Error playing click sound:', error);
            }
        }
    }

    playTransitionSound() {
        if (this.transitionSound) {
            try {
                this.transitionSound.play();
            } catch (error) {
                console.error('Error playing transition sound:', error);
            }
        }
    }

    stopAll() {
        if (this.bgMusic && this.bgMusic.isPlaying) {
            this.bgMusic.stop();
        }
        if (this.clickSound && this.clickSound.isPlaying) {
            this.clickSound.stop();
        }
        if (this.transitionSound && this.transitionSound.isPlaying) {
            this.transitionSound.stop();
        }
    }
}