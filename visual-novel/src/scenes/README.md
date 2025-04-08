# Scenes

## Game Flow
1. BootScene → Loads initial assets
2. MainMenuScene → Game entry point
3. GameScene → Main gameplay
4. UIScene → Overlay interface
5. SettingsScene → Configuration

## Scene Hierarchy
```
Boot → MainMenu → Game + UI
                ↳ Settings
```

## Implementation
Each scene extends Phaser.Scene:
```typescript
export default class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
    }
}
```