import 'phaser';
import BootScene from './scenes/BootScene';
import AssetLoader from './AssetLoader';
import MainMenuScene from './scenes/MainMenuScene';
import GameScene from './scenes/GameScene';
import UIScene from './scenes/UIScene';

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
  scene: [BootScene, AssetLoader, MainMenuScene, GameScene, UIScene],
  audio: {
    disableWebAudio: false
  }
};

// Add audio context resume on user interaction
window.addEventListener('click', function() {
  if (game.sound.context.state === 'suspended') {
    game.sound.context.resume();
  }
});

window.game = new Phaser.Game(config);

// Add to AudioManager.js playBackgroundMusic method
console.log('Attempting to play background music', {
    exists: !!this.bgMusic,
    isPlaying: this.bgMusic?.isPlaying,
    context: this.scene.sound.context.state
});