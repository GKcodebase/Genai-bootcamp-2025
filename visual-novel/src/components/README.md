# Components

## Overview
Core UI and interaction components for the visual novel.

### DialogBox
Handles text display and typing effects:
```typescript
import DialogBox from './DialogBox';
const dialog = new DialogBox(scene, x, y);
```

### ChoiceMenu
Manages player decision points:
```typescript
import ChoiceMenu from './ChoiceMenu';
const menu = new ChoiceMenu(scene, x, y);
```

### LanguageTools
Japanese language learning utilities:
```typescript
import { translateText, checkPronunciation } from './LanguageTools';
```