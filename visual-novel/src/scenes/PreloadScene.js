export default class PreloadScene extends Phaser.Scene {
    constructor() {
        super('Preload');
    }

    preload() {
        // Create loading bar
        this.createLoadingBar();

        // Load game assets
        this.loadAssets();
    }

    createLoadingBar() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(width/4, height/2, width/2, 50);
        
        this.load.on('progress', (value) => {
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(width/4 + 10, height/2 + 10, (width/2 - 20) * value, 30);
        });
    }

    loadAssets() {
        // Load your game assets here
    }

    create() {
        this.scene.start('Load');
    }
}