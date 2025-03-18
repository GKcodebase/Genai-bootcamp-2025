export default class AssetLoader extends Phaser.Scene {
    constructor() {
        super('AssetLoader');
    }

    preload() {
        this.createLoadingText();
        
        // Load audio files
        this.load.audio('bgMusic', 'assets/audio/bg.wav');
        this.load.audio('clickSound', 'assets/audio/click.wav');
        this.load.audio('transitionSound', 'assets/audio/transition.wav');

        // Debug audio loading
        this.load.on('complete', () => {
            console.log('Audio assets loaded:', 
                this.cache.audio.entries.keys()
            );
        });

        // Load other assets
        this.load.setPath('assets/');
        this.loadBackgrounds();
        this.loadCharacters();
    }

    createLoadingText() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        this.loadingText = this.add.text(width/2, height/2, 'Loading...', {
            fontSize: '32px',
            fill: '#ffffff'
        }).setOrigin(0.5);
    }

    loadBackgrounds() {
        this.load.image('apartment', 'assets/images/backgrounds/apartment.jpg');
    }

    loadCharacters() {
        this.load.image('alex', 'assets/images/characters/alex.png');
    }

    create() {
        // Verify audio loaded
        if (this.cache.audio.exists('bgMusic')) {
            console.log('Audio loaded successfully');
        }

        // Test audio before proceeding
        try {
            const testSound = this.sound.add('bgMusic', { volume: 0.1 });
            console.log('Audio system initialized');
        } catch (error) {
            console.error('Audio initialization failed:', error);
        }

        this.state = {
            currentScene: 'scene001',
            currentDialog: 0
        };

        this.loadScene(this.state.currentScene)
            .then(() => {
                console.log('AssetLoader: Assets loaded, transitioning to MainMenu');
                this.scene.start('MainMenuScene');
            });
    }

    async loadScene(sceneId) {
        try {
            const response = await fetch(`scenes/${sceneId}.json`);
            const data = await response.json();
            this.cache.json.add(sceneId, data);
        } catch (error) {
            console.error('Error loading scene:', error);
        }
    }
}