export default class AssetLoader extends Phaser.Scene {
    constructor() {
        super('AssetLoader');
    }

    preload() {
        this.createLoadingText();
        
        // Load audio assets first
        this.load.setPath('assets/audio/');
        this.load.audio('bgMusic', ['bg.wav']);
        this.load.audio('clickSound', ['click.wav']);
        this.load.audio('transitionSound', ['transition.wav']);

        // Add audio loading debug
        this.load.on('filecomplete-audio-bgMusic', () => {
            console.log('Background music loaded successfully');
        });

        this.load.on('loaderror', (file) => {
            console.error('Error loading:', file.key, file.src);
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

    loadAudio() {
        // Load audio with correct paths
        this.load.audio('bgMusic', 'assets/audio/bg.wav');
        this.load.audio('clickSound', 'assets/audio/click.wav');
        this.load.audio('transitionSound', 'assets/audio/transition.wav');
        
        // Add loading progress callback
        this.load.on('complete', () => {
            console.log('Audio loaded successfully');
        });
        
        this.load.on('loaderror', (fileObj) => {
            console.error('Error loading audio:', fileObj.src);
        });
    }

    create() {
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