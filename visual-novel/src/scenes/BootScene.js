export default class BootScene extends Phaser.Scene {
    constructor() {
        super('BootScene');
    }

    preload() {
        // Show loading text
        const loadingText = this.add.text(
            this.cameras.main.width / 2,
            this.cameras.main.height / 2,
            'Loading...',
            {
                fontSize: '32px',
                fill: '#fff'
            }
        ).setOrigin(0.5);

        // Load UI assets
        this.load.image('logo', 'assets/images/ui/logo.png');
        this.load.image('loading-bar', 'assets/images/ui/loading-bar.png');
        
        // Load all backgrounds
        const backgrounds = [
            'apartment',
            'cafe',
            'classroom',
            'post-office',
            'store'
        ];
        
        backgrounds.forEach(bg => {
            this.load.image(bg, `assets/images/backgrounds/${bg}.jpg`);
        });
        
        // Load all character images
        const characters = [
            'akiko',
            'alex',
            'carlos',
            'hiroshi',
            'kenji',
            'minji',
            'yuki',
            'yamamoto'
        ];
        
        characters.forEach(char => {
            this.load.image(`${char}`, `assets/images/charachter/${char}.png`);
        });

        // Add loading bar
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        const progressBar = this.add.graphics();
        const progressBox = this.add.graphics();
        progressBox.fillStyle(0x222222, 0.8);
        progressBox.fillRect(width/4, height/2, width/2, 50);
        
        // Loading progress events
        this.load.on('progress', (value) => {
            progressBar.clear();
            progressBar.fillStyle(0xffffff, 1);
            progressBar.fillRect(width/4 + 10, height/2 + 10, (width/2 - 20) * value, 30);
        });
        
        this.load.on('complete', () => {
            progressBar.destroy();
            progressBox.destroy();
            loadingText.destroy();
            this.scene.start('MainMenuScene');
        });
    }

    create() {
        console.log('BootScene: Starting AssetLoader');
        this.scene.start('AssetLoader');
    }
}