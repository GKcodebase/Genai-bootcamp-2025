import DialogManager from '../systems/DialogManager';
import AudioManager from '../systems/AudioManager';

export default class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
    }

    init(data) {
        console.log('GameScene: Initializing');
        this.currentScene = data.sceneId;
        this.currentDialog = 0;
    }

    async create() {
        console.log('GameScene: Creating');
        console.log('Audio cache:', this.cache.audio.entries);

        // Wait for audio to be available
        if (!this.cache.audio.exists('bgMusic')) {
            console.warn('Audio not loaded, waiting...');
            this.time.delayedCall(100, () => this.create());
            return;
        }

        // Load scene data first
        await this.loadSceneData();
        
        // Create game elements
        this.createBackground();
        this.createCharacter();
        
        // Launch UI scene
        this.scene.launch('UIScene');
        
        // Start dialog
        this.showCurrentDialog();

        // Initialize audio after confirming assets are loaded
        this.audioManager = new AudioManager(this);
        this.audioManager.playBackgroundMusic();

        // Add click handler for next dialog with sound
        this.input.on('pointerdown', () => {
            this.audioManager.playClickSound();
            this.nextDialog();
        });
    }

    async loadSceneData() {
        try {
            const response = await fetch(`/scenes/${this.currentScene}.json`);
            this.sceneData = await response.json();
        } catch (error) {
            console.error('Error loading scene data:', error);
        }
    }

    createBackground() {
        this.background = this.add.image(640, 360, 'apartment');
        this.background.setDisplaySize(1280, 720);
    }

    createCharacter() {
        if (this.sceneData.character) {
            this.character = this.add.image(640, 360, 'alex');
            this.character.setScale(0.8);
        }
    }

    showCurrentDialog() {
        if (this.sceneData.dialog && this.sceneData.dialog[this.currentDialog]) {
            const dialogData = this.sceneData.dialog[this.currentDialog];
            this.scene.get('UIScene').events.emit('updateDialog', dialogData);
        }
    }

    nextDialog() {
        this.currentDialog++;
        if (this.sceneData.dialog && this.currentDialog < this.sceneData.dialog.length) {
            this.showCurrentDialog();
        } else {
            // Play transition sound when dialog ends
            this.audioManager.playTransitionSound();
        }
    }
}