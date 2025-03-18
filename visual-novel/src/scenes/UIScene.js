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
    }
}