# Scene Data

## Structure
Each scene is defined in a JSON file with:
- Dialog sequences
- Character interactions
- Language learning content
- Branch points

## Example
```json
{
    "id": "scene001",
    "title": "Welcome to Japan",
    "dialog": [
        {
            "speaker": "alex",
            "text": "Welcome to Japan!",
            "languageVersion": "日本へようこそ！"
        }
    ]
}
```

## Adding New Scenes
1. Create new JSON file in this directory
2. Follow schema in `scene001.json`
3. Add to story progression in `story-structure.md`