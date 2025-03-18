export default class LoadScene extends Phaser.Scene {
    constructor() {
        super('Load');
    }

    create() {
        // Load game data, save files, or any other initialization
        this.loadGameData();
    }

    loadGameData() {
        // Load any saved game data or initial game state
        
        // Then transition to menu
        this.scene.start('Menu');
    }
}