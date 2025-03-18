export default class ChoiceMenu {
    constructor(scene, x, y) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.choices = [];
    }

    showChoices(choices) {
        this.clearChoices();
        
        choices.forEach((choice, index) => {
            const button = this.scene.add.text(this.x, this.y + (index * 50), choice.text, {
                fontSize: '24px',
                fill: '#ffffff',
                backgroundColor: '#333333',
                padding: { x: 10, y: 5 }
            })
            .setOrigin(0.5)
            .setInteractive();

            button.on('pointerdown', () => {
                this.scene.events.emit('choice-selected', choice);
                this.clearChoices();
            });

            this.choices.push(button);
        });
    }

    clearChoices() {
        this.choices.forEach(choice => choice.destroy());
        this.choices = [];
    }
}