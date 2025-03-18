export default class MainMenuScene extends Phaser.Scene {
    constructor() {
        super('MainMenuScene');
    }

    create() {
        // Title text
        const titleText = this.add.text(640, 200, 'Japanese Visual Novel', {
            fontSize: '64px',
            fill: '#ffffff'
        }).setOrigin(0.5);

        // Create menu buttons
        const buttonStyle = {
            fontSize: '32px',
            fill: '#ffffff',
            backgroundColor: '#333333',
            padding: { x: 20, y: 10 }
        };

        const buttons = [
            { text: 'Start Game', y: 400, handler: () => this.startNewGame() },
            { text: 'Load Game', y: 470, handler: () => this.loadGame() },
            { text: 'Settings', y: 540, handler: () => this.openSettings() }
        ];

        buttons.forEach(button => {
            const buttonText = this.add.text(640, button.y, button.text, buttonStyle)
                .setOrigin(0.5)
                .setInteractive();

            buttonText.on('pointerover', () => buttonText.setStyle({ fill: '#ffff00' }));
            buttonText.on('pointerout', () => buttonText.setStyle({ fill: '#ffffff' }));
            buttonText.on('pointerdown', button.handler);
        });
    }

    startNewGame() {
        this.scene.start('GameScene', { sceneId: 'scene001' });
    }

    loadGame() {
        // Load saved game data from localStorage
        const savedGame = localStorage.getItem('visualNovelSave');
        if (savedGame) {
            const gameData = JSON.parse(savedGame);
            this.scene.start('GameScene', gameData);
        } else {
            this.showMessage('No saved game found');
        }
    }

    openSettings() {
        this.scene.start('SettingsScene');
    }

    showMessage(text) {
        const message = this.add.text(640, 300, text, {
            fontSize: '24px',
            fill: '#ff0000',
            backgroundColor: '#000000',
            padding: { x: 20, y: 10 }
        }).setOrigin(0.5);

        this.time.delayedCall(2000, () => message.destroy());
    }
}