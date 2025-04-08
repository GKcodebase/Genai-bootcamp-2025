# API Integration Guide

## Base Configuration
```typescript
const API_BASE = import.meta.env.VITE_API_URL;

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## Endpoints

### Words API
```typescript
// Get all words
GET /api/words

// Get word by ID
GET /api/words/:id

// Create new word
POST /api/words

// Update word
PUT /api/words/:id
```

### Study Sessions API
```typescript
// Get user's study sessions
GET /api/study-sessions

// Create new study session
POST /api/study-sessions

// Update session progress
PUT /api/study-sessions/:id
```

## Error Handling
```typescript
try {
  const response = await apiClient.get('/words');
  return response.data;
} catch (error) {
  handleApiError(error);
}
```