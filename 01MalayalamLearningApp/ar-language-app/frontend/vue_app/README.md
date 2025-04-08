# Interactive Malaylam Learning App - Frontend

Vue.js based frontend application for AR language learning.

## Technologies Used

- Vue.js 3.3.0
- Vite 6.2.5
- AR.js 3.4.5
- A-Frame 1.4.2
- Three.js 0.160.0
- Vue Router 4.0.0

## Features

- Real-time AR camera integration
- Object detection interface
- Interactive practice exercises
- History tracking
- Audio playback and recording
- Responsive design

## Project Structure

```
frontend/vue_app/
├── src/
│   ├── components/
│   │   ├── AROverlay.vue
│   │   ├── LandingPage.vue
│   │   └── PracticeScreen.vue
│   ├── router/
│   │   └── index.js
│   ├── assets/
│   │   └── styles.css
│   ├── App.vue
│   └── main.js
├── public/
├── package.json
└── vite.config.js
```

## Setup and Installation

1. Install dependencies:
```bash
npm install
```

2. Create SSL certificates for HTTPS:
```bash
mkdir .cert
openssl req -x509 -newkey rsa:2048 -keyout .cert/key.pem -out .cert/cert.pem -days 365 -nodes
```

3. Start development server:
```bash
npm run dev
```

## Development

- **Port**: 3000
- **HTTPS**: Required for camera access
- **API Proxy**: Configured to forward to backend at port 8000

## Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Dependencies

```json
{
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.0.0",
    "three": "^0.160.0",
    "aframe": "^1.4.2",
    "@ar-js-org/ar.js": "^3.4.5"
  }
}
```

## Browser Support

- Chrome (recommended)
- Safari
- Firefox
- Edge

## License

MIT License

Copyright (c) 2025 GK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software...