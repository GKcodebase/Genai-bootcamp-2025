export default class DialogManager {
    constructor(scene, dialogData) {
        this.scene = scene;
        this.dialogData = dialogData;
        this.currentDialogIndex = 0;
    }

    start() {
        this.showCurrentDialog();
    }

    showCurrentDialog() {
        if (this.currentDialogIndex < this.dialogData.length) {
            const currentDialog = this.dialogData[this.currentDialogIndex];
            
            // Send dialog to UI scene
            this.scene.scene.get('UIScene').events.emit('updateDialog', currentDialog);

            // Play sound if available
            if (this.scene.sound.get('click')) {
                this.scene.sound.play('click', { volume: 0.3 });
            }
        }
    }

    nextDialog() {
        this.currentDialogIndex++;
        if (this.currentDialogIndex < this.dialogData.length) {
            this.showCurrentDialog();
        }
    }
}