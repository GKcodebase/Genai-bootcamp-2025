export default class DialogBox {
    constructor(scene, x, y) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.boxWidth = 1000;
        this.boxHeight = 220; // Increased height to accommodate Japanese text
        this.padding = 20;
        
        this.createDialogBox();
        this.createTextElements();
        this.createNextButton();
        
        // Initialize typing effect
        this.typingSpeed = parseInt(localStorage.getItem('textSpeed')) || 30;
        this.isTyping = false;
        this.textToType = '';
        this.japaneseTextToType = '';
    }

    createDialogBox() {
        this.box = this.scene.add.graphics();
        this.box.lineStyle(2, 0xffffff);
        this.box.fillStyle(0x000000, 0.8);
        this.box.fillRect(
            this.x - this.boxWidth/2, 
            this.y - this.boxHeight/2, 
            this.boxWidth, 
            this.boxHeight
        );
        this.box.strokeRect(
            this.x - this.boxWidth/2, 
            this.y - this.boxHeight/2, 
            this.boxWidth, 
            this.boxHeight
        );
        this.box.setDepth(999);
    }

    createTextElements() {
        // Speaker name at the top
        this.speakerText = this.scene.add.text(
            this.x - this.boxWidth/2 + this.padding, 
            this.y - this.boxHeight/2 + this.padding, 
            '', {
                fontSize: '24px',
                fill: '#ffff00',
                fontStyle: 'bold'
            }
        ).setDepth(1000);

        // English text in the middle
        this.dialogText = this.scene.add.text(
            this.x - this.boxWidth/2 + this.padding, 
            this.y - this.boxHeight/4, 
            '', {
                fontSize: '24px',
                fill: '#ffffff',
                wordWrap: { 
                    width: this.boxWidth - (this.padding * 2),
                    useAdvancedWrap: true 
                },
                lineSpacing: 6
            }
        ).setDepth(1000);

        // Japanese text at the bottom with more space
        this.japaneseText = this.scene.add.text(
            this.x - this.boxWidth/2 + this.padding, 
            this.y + 10, 
            '', {
                fontSize: '22px', // Slightly smaller font for Japanese
                fill: '#99ff99',
                wordWrap: { 
                    width: this.boxWidth - (this.padding * 2),
                    useAdvancedWrap: true 
                },
                lineSpacing: 8
            }
        ).setDepth(1000);
    }

    createNextButton() {
        this.nextButton = this.scene.add.text(
            this.x + this.boxWidth/2 - this.padding*2, 
            this.y + this.boxHeight/2 - this.padding*2, 
            '▶', {
                fontSize: '32px',
                fill: '#ffffff',
                backgroundColor: '#333333',
                padding: { x: 10, y: 5 }
            }
        )
        .setDepth(1000)
        .setInteractive()
        .setAlpha(0); // Start hidden

        this.nextButton.on('pointerover', () => this.nextButton.setStyle({ fill: '#ffff00' }));
        this.nextButton.on('pointerout', () => this.nextButton.setStyle({ fill: '#ffffff' }));
        this.nextButton.on('pointerdown', () => {
            if (this.isTyping) {
                this.showFullText();
            } else {
                this.scene.events.emit('dialogNext');
            }
        });
    }

    showDialog(dialogData) {
        if (!dialogData) return;

        // Set speaker name
        this.speakerText.setText(dialogData.speaker ? dialogData.speaker.toUpperCase() : '');

        // Store full text for typing effect
        this.textToType = dialogData.text || '';
        this.japaneseTextToType = dialogData.languageVersion || '';

        // Clear current text
        this.dialogText.setText('');
        this.japaneseText.setText('');

        // Start typing effect
        this.startTypingEffect();
    }

    startTypingEffect() {
        this.isTyping = true;
        this.nextButton.setAlpha(0);
        
        let currentChar = 0;
        let currentJapChar = 0;

        if (this.typingTimer) {
            this.typingTimer.remove();
        }

        this.typingTimer = this.scene.time.addEvent({
            delay: this.typingSpeed,
            callback: () => {
                if (currentChar < this.textToType.length) {
                    this.dialogText.text += this.textToType[currentChar];
                    currentChar++;
                }

                if (currentJapChar < this.japaneseTextToType.length) {
                    this.japaneseText.text += this.japaneseTextToType[currentJapChar];
                    currentJapChar++;
                }

                if (currentChar >= this.textToType.length && 
                    currentJapChar >= this.japaneseTextToType.length) {
                    this.typingComplete();
                }
            },
            repeat: this.textToType.length + this.japaneseTextToType.length - 1
        });
    }

    showFullText() {
        if (this.typingTimer) {
            this.typingTimer.remove();
        }
        this.dialogText.setText(this.textToType);
        this.japaneseText.setText(this.japaneseTextToType);
        this.typingComplete();
    }

    typingComplete() {
        this.isTyping = false;
        this.nextButton.setAlpha(1);
    }

    clear() {
        this.speakerText.setText('');
        this.dialogText.setText('');
        this.japaneseText.setText('');
        this.nextButton.setAlpha(0);
    }

    setVisible(visible) {
        this.box.setVisible(visible);
        this.speakerText.setVisible(visible);
        this.dialogText.setVisible(visible);
        this.japaneseText.setVisible(visible);
    }
}