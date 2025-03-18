export default class LoadingScene extends Phaser.Scene {
    constructor() {
        super('LoadingScene');
    }

    init(saveData) {
        this.saveData = saveData;
    }

    create() {
        // Show loading text
        const loadingText = this.add.text(640, 360, 'Loading...', {
            fontSize: '32px',
            fill: '#ffffff'
        }).setOrigin(0.5);

        // Load required assets
        this.loadAssets();
    }

    loadAssets() {
        // Load or verify all required assets
        const requiredAssets = {
            images: ['apartment', 'alex'],
            audio: ['bgMusic', 'clickSound', 'transitionSound']
        };

        let assetsLoaded = true;

        // Check images
        requiredAssets.images.forEach(key => {
            if (!this.textures.exists(key)) {
                assetsLoaded = false;
                this.load.image(key, `assets/images/${key}.png`);
            }
        });

        // Check audio
        requiredAssets.audio.forEach(key => {
            if (!this.cache.audio.exists(key)) {
                assetsLoaded = false;
                this.load.audio(key, `assets/audio/${key}.wav`);
            }
        });

        if (assetsLoaded) {
            this.startGame();
        } else {
            this.load.once('complete', this.startGame, this);
            this.load.start();
        }
    }

    startGame() {
        // Start GameScene with saved data
        this.scene.start('GameScene', this.saveData);
    }
}