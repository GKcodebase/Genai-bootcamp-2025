export default class DialogBox {
    constructor(scene, x, y) {
        this.scene = scene;
        
        // Create dialog box background
        this.box = scene.add.rectangle(x, y, 1000, 200, 0x000000, 0.7);
        
        // Create text objects
        this.text = scene.add.text(x - 480, y - 80, '', {
            fontSize: '24px',
            fill: '#ffffff',
            wordWrap: { width: 960 }
        });
        
        this.japaneseText = scene.add.text(x - 480, y + 20, '', {
            fontSize: '24px',
            fill: '#ffffff',
            wordWrap: { width: 960 }
        });
    }

    // showDialog(dialogData) {
    //     this.text.setText(dialogData.text);
    //     this.japaneseText.setText(dialogData.languageVersion || '');
    // }
}