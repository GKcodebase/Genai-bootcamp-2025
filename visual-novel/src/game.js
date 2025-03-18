import 'phaser';
import BootScene from './scenes/BootScene';
import MainMenuScene from './scenes/MainMenuScene';
import GameScene from './scenes/GameScene';
import UIScene from './scenes/UIScene';
import AssetLoader from './AssetLoader';

const config = {
    type: Phaser.AUTO,
    parent: 'game-container',
    backgroundColor: '#000000',
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 1280,
        height: 720
    },
    scene: [BootScene,AssetLoader, MainMenuScene, GameScene, UIScene],
    audio: {
        disableWebAudio: false
    }
};

// Create and expose the game instance globally
window.game = new Phaser.Game(config);

// Enhanced debugging helpers with scene management
window.debugGame = {
    inspectDialog: () => {
        const uiScene = window.game.scene.getScene('UIScene');
        if (uiScene && uiScene.dialogBox) {
            const state = {
                visible: uiScene.dialogBox.box.visible,
                currentText: uiScene.dialogBox.dialogText?.text,
                speaker: uiScene.dialogBox.speakerText?.text,
                japaneseText: uiScene.dialogBox.japaneseText?.text,
                position: {
                    x: uiScene.dialogBox.box.x,
                    y: uiScene.dialogBox.box.y
                },
                sceneState: uiScene.scene.isActive('UIScene') ? 'active' : 'inactive'
            };
            console.table(state); // Use table format for better readability
            return state;
        }
        console.warn('UI Scene or Dialog Box not found');
        return null;
    },
    
    testDialog: (text = 'Test dialog', speaker = 'DEBUG', japanese = 'テストダイアログ') => {
        const uiScene = window.game.scene.getScene('UIScene');
        if (uiScene && uiScene.dialogBox) {
            uiScene.dialogBox.showDialog({
                speaker: speaker,
                text: text,
                languageVersion: japanese
            });
            console.log('✅ Test dialog displayed successfully');
            return true;
        }
        console.error('❌ Failed to display test dialog - UI Scene not ready');
        return false;
    },

    getCurrentScene: () => {
        const scenes = window.game.scene.getScenes(true);
        const sceneStates = scenes.map(scene => ({
            name: scene.scene.key,
            active: scene.scene.isActive(),
            visible: scene.scene.isVisible()
        }));
        console.table(sceneStates);
        return sceneStates;
    },

    resetDialog: () => {
        const uiScene = window.game.scene.getScene('UIScene');
        if (uiScene && uiScene.dialogBox) {
            uiScene.dialogBox.clear();
            console.log('🔄 Dialog reset complete');
            return true;
        }
        return false;
    }
};

// Better debug console messages
console.log('%c📱 Visual Novel Debug Tools Ready', 'color: #4CAF50; font-size: 14px; font-weight: bold;');
console.log(`
Available commands:
- debugGame.inspectDialog()     👉 Check dialog state
- debugGame.testDialog("text")  👉 Test custom dialog
- debugGame.getCurrentScene()   👉 List active scenes
- debugGame.resetDialog()       👉 Reset dialog box
`);

export default window.game;