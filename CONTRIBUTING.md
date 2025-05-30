# Contributing to Generative AI Bootcamp Projects 2025

Thank you for your interest in contributing to our Generative AI Bootcamp Projects! 🎉 

This repository contains a diverse collection of AI-powered language learning applications and educational tools. We welcome contributions from developers of all skill levels who are passionate about AI, education, and language learning.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:
- **Node.js** (v16 or higher)
- **Python** (v3.7 or higher)
- **Go** (v1.19 or higher) - for Go-based projects
- **Git**

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/your-username/Genai-bootcamp-2025.git
cd Genai-bootcamp-2025
```

3. Add the original repository as upstream:
```bash
git remote add upstream https://github.com/GKcodebase/free-genai-bootcamp-2025.git
```

## 🛠️ How to Contribute

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Fixes
- Fix existing bugs in any project
- Improve error handling
- Performance optimizations

#### ✨ New Features
- Add new language learning exercises
- Implement new AI integrations
- Create new learning modalities

#### 📚 Documentation
- Improve README files
- Add API documentation
- Create tutorials and guides
- Fix typos and grammar

#### 🧪 Testing
- Add unit tests
- Improve test coverage
- Create integration tests

#### 🎨 UI/UX Improvements
- Enhance user interfaces
- Improve accessibility
- Add responsive design features

### Project-Specific Contributions

#### AR Language Learning App
- Improve object detection accuracy
- Add new languages
- Enhance AR overlay features

#### Visual Novel
- Create new story branches
- Add interactive elements
- Improve audio integration

#### Language Portal
- Add new vocabulary features
- Implement advanced search
- Create new study activities

#### Writing Practice App
- Improve OCR accuracy
- Add new writing exercises
- Enhance grading algorithms

## 💻 Development Setup

### General Setup

1. **Install dependencies** for the project you want to work on:

```bash
# For Node.js projects
cd project-directory
npm install

# For Python projects
cd project-directory
pip install -r requirements.txt

# For Go projects
cd project-directory
go mod download
```

2. **Environment Variables**: Copy `.env.example` to `.env` and fill in required values

3. **Database Setup**: Follow project-specific database setup instructions

### Project-Specific Setup

Each project has its own setup requirements. Please refer to the individual project README files for detailed setup instructions.

## 📝 Coding Standards

### General Guidelines

- Write clean, readable, and maintainable code
- Follow the existing code style in each project
- Add comments for complex logic
- Use meaningful variable and function names

### Language-Specific Standards

#### JavaScript/TypeScript
- Use ES6+ features
- Follow ESLint configurations
- Use TypeScript for type safety
- Prefer arrow functions for callbacks

#### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Use virtual environments

#### Go
- Follow Go formatting standards (`go fmt`)
- Use proper error handling
- Write clear variable names
- Include tests for new functions

### File Naming Conventions

- Use kebab-case for directories: `my-project-name`
- Use camelCase for JavaScript/TypeScript files: `myComponent.js`
- Use snake_case for Python files: `my_module.py`
- Use PascalCase for component files: `MyComponent.vue`

## 📝 Commit Guidelines

### Commit Message Format

Use the conventional commits format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Examples
```bash
feat(ar-app): add Malayalam object detection
fix(visual-novel): resolve audio loading issue
docs(readme): update installation instructions
test(lang-portal): add vocabulary API tests
```

### Commit Best Practices

- Make atomic commits (one feature/fix per commit)
- Write clear, descriptive commit messages
- Include issue numbers when applicable: `fixes #123`

## 🔍 Pull Request Process

### Before Submitting

1. **Create a feature branch**:
```bash
git checkout -b feature/amazing-feature
```

2. **Make your changes** following the coding standards

3. **Test your changes**:
```bash
# Run tests for the specific project
npm test  # or pytest, or go test
```

4. **Update documentation** if needed

5. **Commit your changes** using conventional commit format

### Submitting the Pull Request

1. **Push your branch**:
```bash
git push origin feature/amazing-feature
```

2. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Screenshots for UI changes
   - Link to related issues

3. **Fill out the PR template** completely

### PR Review Process

- All PRs require at least one review
- Address review feedback promptly
- Keep PRs focused and reasonably sized
- Ensure CI/CD checks pass

## 🏗️ Project Structure

Each project follows a consistent structure:

```
project-name/
├── README.md           # Project-specific documentation
├── package.json        # Dependencies (Node.js projects)
├── requirements.txt    # Dependencies (Python projects)
├── src/               # Source code
├── tests/             # Test files
├── docs/              # Additional documentation
└── .env.example       # Environment variables template
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for new features and bug fixes
- Aim for good test coverage (>80%)
- Use descriptive test names
- Test both happy path and edge cases

### Running Tests

```bash
# JavaScript/TypeScript projects
npm test
npm run test:coverage

# Python projects
pytest
pytest --cov

# Go projects
go test ./...
go test -cover ./...
```

### Test Types

- **Unit Tests**: Test individual functions/components
- **Integration Tests**: Test interactions between components
- **E2E Tests**: Test complete user workflows

## 📖 Documentation

### README Files

Each project should have:
- Clear description
- Installation instructions
- Usage examples
- API documentation (if applicable)
- Contributing guidelines

### Code Documentation

- Add JSDoc comments for JavaScript functions
- Use docstrings for Python functions
- Add Go doc comments for exported functions
- Document complex algorithms and business logic

### API Documentation

- Use OpenAPI/Swagger for REST APIs
- Include request/response examples
- Document error responses
- Keep documentation up to date

## 👥 Community

### Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Contact**: Reach out to maintainers directly for urgent matters

### Stay Updated

- Watch the repository for updates
- Follow the project roadmap
- Participate in discussions

## 🏷️ Issue Labels

We use the following labels to categorize issues:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements or additions to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 🎯 Contribution Ideas

Looking for ways to contribute? Here are some ideas:

### Beginner-Friendly
- Fix typos in documentation
- Add missing tests
- Improve error messages
- Update dependencies

### Intermediate
- Add new language support
- Implement new learning exercises
- Improve UI components
- Optimize performance

### Advanced
- Implement new AI models
- Add complex features
- Architect new projects
- Optimize algorithms

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Project documentation
- Release notes for significant contributions

---

Thank you for contributing to the Generative AI Bootcamp Projects! Your contributions help make language learning more accessible and engaging for everyone. 🌟

For questions about contributing, please open an issue or reach out to the maintainers. 