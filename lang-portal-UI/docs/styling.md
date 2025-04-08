# Styling Guide

## Theme Configuration

### Colors
```typescript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#E63946',
          dark: '#BF2233',
        },
        secondary: {
          DEFAULT: '#1D3557',
          light: '#457B9D',
        },
      },
    },
  },
}
```

### Typography
- Primary Font: `Noto Sans JP`
- Secondary Font: `CC Wild Words`
- Manga Emphasis: `Bangers`

## Component Styling

### Buttons
```tsx
// Primary Button
<button className="bg-primary hover:bg-primary-dark text-white 
                  font-bold py-2 px-4 rounded-lg">
  Start Learning
</button>

// Secondary Button
<button className="border-2 border-secondary hover:bg-secondary 
                  hover:text-white py-2 px-4 rounded-lg">
  Cancel
</button>
```

### Cards
```tsx
<div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg 
                p-6 hover:shadow-xl transition-shadow">
  {/* Card content */}
</div>
```

## Dark Mode
Use `dark:` variant for dark mode styling:
```tsx
<div className="bg-white dark:bg-gray-800 
                text-gray-900 dark:text-gray-100">
  {/* Content */}
</div>
```