import DialogBox from '../components/DialogBox';

export default class UIScene extends Phaser.Scene {
    constructor() {
        super('UIScene');
    }

    create() {
        console.log('UIScene: Creating dialog box');
        
        // Create dialog box at the bottom center of the screen
        this.dialogBox = new DialogBox(this, 640, 580);
        
        // Make dialog box accessible globally for debugging
        if (window.game) {
            window.game.debugDialog = this.dialogBox;
        }
        
        // Listen for dialog updates from GameScene
        this.events.on('updateDialog', (dialogData) => {
            console.log('UIScene: Received dialog update:', dialogData);
            if (this.dialogBox && dialogData) {
                // Clear any test dialog first
                this.dialogBox.clear();
                // Show the actual game dialog
                this.dialogBox.showDialog(dialogData);
            }
        });

        // Debug text with better instructions
        // this.debugText = this.add.text(10, 10, 
        //     'Debug: Open console (F12) and type debugGame.inspectDialog() to check dialog state', {
        //     fontSize: '16px',
        //     fill: '#ffffff'
        // });

        // Test dialog to verify box positioning
        this.dialogBox.showDialog({
            speaker: 'System',
            text: 'Welcome to Alex Journey to Japan.',
            languageVersion: 'システム初期化完了'
        });

        // Add control buttons
        this.createControlButtons();
    }

    createControlButtons() {
        const buttonStyle = {
            fontSize: '24px',
            fill: '#ffffff',
            backgroundColor: '#333333',
            padding: { x: 10, y: 5 }
        };

        // Create control buttons in top-right corner
        const controls = [
            { text: 'Save', x: 1100, handler: () => this.saveGame() },
            { text: 'Load', x: 1180, handler: () => this.loadGame() },
            { text: '⚙️', x: 1260, handler: () => this.openSettings() }
        ];

        controls.forEach(control => {
            const button = this.add.text(control.x, 30, control.text, buttonStyle)
                .setOrigin(0.5)
                .setInteractive()
                .setDepth(1000);

            button.on('pointerover', () => button.setStyle({ fill: '#ffff00' }));
            button.on('pointerout', () => button.setStyle({ fill: '#ffffff' }));
            button.on('pointerdown', control.handler);
        });
    }

    saveGame() {
        const gameScene = this.scene.get('GameScene');
        const saveData = {
            sceneId: gameScene.currentScene,
            dialogIndex: gameScene.currentDialog,
            // Add any other state you want to save
            timestamp: new Date().toISOString()
        };
        
        try {
            localStorage.setItem('visualNovelSave', JSON.stringify(saveData));
            this.showMessage('Game Saved Successfully');
        } catch (error) {
            console.error('Save failed:', error);
            this.showMessage('Failed to Save Game');
        }
    }

    loadGame() {
        try {
            const savedGame = localStorage.getItem('visualNovelSave');
            if (!savedGame) {
                this.showMessage('No Save Data Found');
                return;
            }

            const saveData = JSON.parse(savedGame);
            
            // Stop current scene and UI
            this.scene.stop('GameScene');
            this.scene.stop('UIScene');
            
            // Restart with loading screen
            this.scene.start('LoadingScene', saveData);
        } catch (error) {
            console.error('Load failed:', error);
            this.showMessage('Failed to Load Game');
        }
    }

    openSettings() {
        this.scene.pause('GameScene');
        this.scene.launch('SettingsScene');
    }

    showMessage(text) {
        const message = this.add.text(640, 360, text, {
            fontSize: '32px',
            fill: '#ffffff',
            backgroundColor: '#000000',
            padding: { x: 20, y: 10 }
        })
        .setOrigin(0.5)
        .setDepth(2000);

        this.time.delayedCall(2000, () => message.destroy());
    }
}