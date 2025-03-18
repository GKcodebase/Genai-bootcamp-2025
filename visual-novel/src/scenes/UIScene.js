import DialogBox from '../components/DialogBox';
import ChoiceMenu from '../components/ChoiceMenu';

export default class UIScene extends Phaser.Scene {
    constructor() {
        super('UIScene');
    }

    create(data) {
        console.log('UIScene: Creating dialog box');
        // Create single dialog box
        this.createDialogBox();
        
        // Listen for dialog updates
        this.events.on('updateDialog', this.updateDialog, this);
        // this.dialogBox = new DialogBox(this, 640, 550);
        // this.choiceMenu = new ChoiceMenu(this, 640, 400);
        
        this.events.on('dialog-start', this.showDialog, this);
        this.events.on('show-choices', this.showChoices, this);
    }

    createDialogBox() {
        // Create semi-transparent background
        const graphics = this.add.graphics();
        graphics.fillStyle(0x000000, 0.7);
        graphics.fillRect(0, 520, 1280, 200);

        // Create text elements
        this.dialogText = this.add.text(40, 540, '', {
            fontSize: '24px',
            fill: '#ffffff',
            wordWrap: { width: 1200 }
        });

        this.japaneseText = this.add.text(40, 580, '', {
            fontSize: '24px',
            fill: '#ffffff',
            wordWrap: { width: 1200 }
        });
    }

    updateDialog(dialogData) {
        if (!dialogData) return;
        console.log('UIScene: Updating dialog with:', dialogData);
        this.dialogText.setText(dialogData.text || '');
        this.japaneseText.setText(dialogData.languageVersion || '');
    }

    showDialog(dialogData) {
        this.dialogBox.showDialog(dialogData);
    }

    showChoices(choices) {
        this.choiceMenu.showChoices(choices);
    }
}