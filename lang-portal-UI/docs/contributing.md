# Contributing Guide

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/lang-portal-UI.git
cd lang-portal-UI
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local`:
```env
VITE_API_URL=http://localhost:3000
```

## Development Workflow

1. Create a new branch:
```bash
git checkout -b feature/your-feature
```

2. Start development server:
```bash
npm run dev
```

3. Format code before committing:
```bash
npm run format
```

## Commit Guidelines

Use semantic commit messages:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code restructuring
- `test:` adding tests

## Pull Request Process

1. Update documentation
2. Add tests if needed
3. Ensure all tests pass
4. Request review from maintainers

## Code Style

- Use TypeScript
- Follow ESLint configuration
- Use Prettier for formatting
- Add JSDoc comments for complex functions