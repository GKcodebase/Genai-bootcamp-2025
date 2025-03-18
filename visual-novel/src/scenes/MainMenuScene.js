export default class MainMenuScene extends Phaser.Scene {
    constructor() {
        super('MainMenuScene');
    }

    create() {
        // Add title text instead of logo image
        const titleText = this.add.text(640, 260, 'Japanese Visual Novel', {
            fontSize: '64px',
            fill: '#ffffff'
        }).setOrigin(0.5);

        const startButton = this.add.text(640, 500, 'Start Game', {
            fontSize: '32px',
            fill: '#ffffff',
            backgroundColor: '#333333',
            padding: { x: 20, y: 10 }
        })
        .setOrigin(0.5)
        .setInteractive();

        // Add hover effect
        startButton.on('pointerover', () => startButton.setStyle({ fill: '#ffff00' }));
        startButton.on('pointerout', () => startButton.setStyle({ fill: '#ffffff' }));
        startButton.on('pointerdown', () => {
            this.scene.start('GameScene', { sceneId: 'scene001' });
        });
    }
}