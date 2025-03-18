export default class SettingsScene extends Phaser.Scene {
    constructor() {
        super('SettingsScene');
        this.settings = {
            textSpeed: parseInt(localStorage.getItem('textSpeed')) || 30,
            musicVolume: parseFloat(localStorage.getItem('musicVolume')) || 0.5,
            soundVolume: parseFloat(localStorage.getItem('soundVolume')) || 0.7,
            autoSave: localStorage.getItem('autoSave') === 'true' || false
        };
    }

    create() {
        // Title
        this.add.text(640, 100, 'Settings', {
            fontSize: '48px',
            fill: '#ffffff'
        }).setOrigin(0.5);

        // Create settings controls
        this.createSlider('Text Speed', 200, this.settings.textSpeed, 10, 50, value => {
            this.settings.textSpeed = value;
            localStorage.setItem('textSpeed', value);
        });

        this.createSlider('Music Volume', 270, this.settings.musicVolume, 0, 1, value => {
            this.settings.musicVolume = value;
            localStorage.setItem('musicVolume', value);
            // Update active music volume
            const gameScene = this.scene.get('GameScene');
            if (gameScene.audioManager) {
                gameScene.audioManager.setMusicVolume(value);
            }
        });

        this.createSlider('Sound Effects', 340, this.settings.soundVolume, 0, 1, value => {
            this.settings.soundVolume = value;
            localStorage.setItem('soundVolume', value);
            // Update sound effects volume
            const gameScene = this.scene.get('GameScene');
            if (gameScene.audioManager) {
                gameScene.audioManager.setSoundVolume(value);
            }
        });

        // Auto-save toggle
        this.createToggle('Auto-Save', 410, this.settings.autoSave, value => {
            this.settings.autoSave = value;
            localStorage.setItem('autoSave', value);
        });

        // Back button
        const backButton = this.add.text(640, 500, 'Back', {
            fontSize: '32px',
            fill: '#ffffff',
            backgroundColor: '#333333',
            padding: { x: 20, y: 10 }
        })
        .setOrigin(0.5)
        .setInteractive();

        backButton.on('pointerover', () => backButton.setStyle({ fill: '#ffff00' }));
        backButton.on('pointerout', () => backButton.setStyle({ fill: '#ffffff' }));
        backButton.on('pointerdown', () => {
            this.saveSettings();
            this.scene.start('MainMenuScene');
        });
    }

    createSlider(label, y, initialValue, min, max, onChange) {
        // Label
        this.add.text(440, y, label, {
            fontSize: '32px',
            fill: '#ffffff'
        }).setOrigin(1, 0.5);

        // Slider background
        const sliderWidth = 200;
        const sliderBg = this.add.rectangle(640, y, sliderWidth, 10, 0x666666);

        // Slider handle
        const handle = this.add.rectangle(
            640 + ((initialValue - min) / (max - min) - 0.5) * sliderWidth,
            y,
            20,
            30,
            0xffffff
        ).setInteractive();

        // Value text
        const valueText = this.add.text(740, y, initialValue.toFixed(1), {
            fontSize: '24px',
            fill: '#ffffff'
        }).setOrigin(0, 0.5);

        // Make handle draggable
        this.input.setDraggable(handle);

        handle.on('drag', (pointer, dragX) => {
            const minX = 640 - sliderWidth/2;
            const maxX = 640 + sliderWidth/2;
            const newX = Phaser.Math.Clamp(dragX, minX, maxX);
            handle.x = newX;

            const value = min + (handle.x - minX) / sliderWidth * (max - min);
            valueText.setText(value.toFixed(1));
            onChange(value);
        });
    }

    createToggle(label, y, initialValue, onChange) {
        // Label
        this.add.text(440, y, label, {
            fontSize: '32px',
            fill: '#ffffff'
        }).setOrigin(1, 0.5);

        // Toggle button
        const toggle = this.add.rectangle(640, y, 60, 30, initialValue ? 0x00ff00 : 0xff0000)
            .setInteractive();

        const toggleText = this.add.text(640, y, initialValue ? 'ON' : 'OFF', {
            fontSize: '24px',
            fill: '#ffffff'
        }).setOrigin(0.5);

        toggle.on('pointerdown', () => {
            const newValue = !this.settings.autoSave;
            toggle.setFillStyle(newValue ? 0x00ff00 : 0xff0000);
            toggleText.setText(newValue ? 'ON' : 'OFF');
            onChange(newValue);
        });
    }

    saveSettings() {
        // Save all settings to localStorage
        Object.entries(this.settings).forEach(([key, value]) => {
            localStorage.setItem(key, value);
        });
    }
}