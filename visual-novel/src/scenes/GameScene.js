import DialogManager from '../systems/DialogManager';
import AudioManager from '../systems/AudioManager';

export default class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
        this.currentDialog = 0;
    }

    init(data) {
        console.log('GameScene: Initializing with data:', data);
        this.currentScene = data.sceneId || 'scene001';
    }

    async create() {
        console.log('GameScene: Creating scene');
        
        // Load scene data first
        await this.loadSceneData();
        console.log('Scene data loaded:', this.sceneData);
        
        // Create game elements
        this.createBackground();
        this.createCharacter();
        
        // Launch UI scene
        this.scene.launch('UIScene');
        
        // Listen for dialog progression
        this.scene.get('UIScene').events.on('dialogNext', () => {
            this.nextDialog();
        });

        // Show first dialog
        this.showCurrentDialog();

        // Initialize audio after scene is ready
        this.time.delayedCall(100, () => {
            this.initializeAudio();
        });

        // Listen for choice events
        this.events.on('dialogChoice', this.handleDialogChoice, this);
    }

    async loadSceneData() {
        try {
            const response = await fetch(`scenes/${this.currentScene}.json`);
            if (!response.ok) {
                throw new Error(`Failed to load scene: ${this.currentScene}`);
            }
            this.sceneData = await response.json();
            console.log('Loaded scene data:', this.sceneData);
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
        if (!this.sceneData?.dialog?.[this.currentDialog]) return;

        const dialogData = this.sceneData.dialog[this.currentDialog];
        console.log('Emitting dialog:', dialogData);

        // Ensure UIScene exists and is active
        if (!this.scene.isActive('UIScene')) {
            this.scene.launch('UIScene');
        }

        // Emit dialog update event
        this.scene.get('UIScene').events.emit('updateDialog', {
            speaker: dialogData.speaker,
            text: dialogData.text,
            languageVersion: dialogData.languageVersion,
            options: dialogData.options
        });
    }

    nextDialog() {
        console.log('Moving to next dialog');
        this.currentDialog++;
        if (this.sceneData && this.sceneData.dialog && this.currentDialog < this.sceneData.dialog.length) {
            this.showCurrentDialog();
            if (this.audioManager) {
                this.audioManager.playClickSound();
            }
        } else {
            console.log('Reached end of dialog');
            if (this.audioManager) {
                this.audioManager.playTransitionSound();
            }
        }
    }

    initializeAudio() {
        try {
            this.audioManager = new AudioManager(this);
            this.audioManager.playMusic();
        } catch (error) {
            console.error('Failed to initialize audio:', error);
        }
    }

    handleDialogChoice(data) {
        console.log('Choice selected:', data);
        // Handle choice consequences here
        this.nextDialog();
    }
}