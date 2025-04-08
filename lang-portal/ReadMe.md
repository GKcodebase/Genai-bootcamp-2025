# Language Learning Portal

A comprehensive language learning platform that serves as a vocabulary inventory, learning record store (LRS), and unified launch pad for various learning applications.

## 🎯 Project Overview

This project implements a multi-backend architecture showcasing different implementation approaches:
- FastAPI (Python)
- Go/Gin
- Flask

The platform allows users to:
- Manage vocabulary lists
- Track learning progress
- Launch different learning activities
- Monitor study sessions
- View detailed statistics

## 🏗️ Architecture

```
lang-portal/
├── backend-fastapi/      # FastAPI implementation
├── backend_go/          # Go/Gin implementation
├── backend-flask/       # Flask implementation
├── frontend-react/      # React/Next.js frontend
└── TechSpec/           # Technical specifications
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**
  - SQLAlchemy ORM
  - Alembic migrations
  - Pydantic models
- **Go/Gin**
  - modernc.org/sqlite
  - Mage task runner
- **Common Database**: SQLite3

### Frontend
- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Query

## 📦 Installation & Setup

### FastAPI Backend
```bash
cd backend-fastapi
python -m venv venv
source venv/bin/activate  # For Unix
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Go Backend
```bash
cd backend_go
go mod download
mage migrate
mage run
```

### Frontend
```bash
cd frontend-react
npm install
npm run dev
```

## 🗄️ Database Schema

```sql
-- Core Tables
Words(id, japanese, romaji, english, parts)
Groups(id, name)
WordGroups(word_id, group_id)
StudyActivities(id, name, thumbnail_url)
StudySessions(id, activity_id, group_id, created_at)
WordReviewItems(id, word_id, study_session_id, correct, created_at)
```

## 📚 API Documentation

### Dashboard Endpoints
- `GET /api/dashboard/last_study_session`
- `GET /api/dashboard/study_progress`
- `GET /api/dashboard/quick-stats`

### Study Activities
- `GET /api/study_activities`
- `GET /api/study_activities/:id`
- `POST /api/study_activities`

### Words & Groups
- `GET /api/words`
- `GET /api/words/:id`
- `GET /api/groups`
- `GET /api/groups/:id/words`

### Study Sessions
- `GET /api/study_sessions`
- `GET /api/study_sessions/:id`
- `GET /api/study_sessions/:id/words`

## 🧪 Testing

### FastAPI
```bash
cd backend-fastapi
pytest
```

### Go
```bash
cd backend_go
go test ./...
```

### Frontend
```bash
cd frontend-react
npm test
```

## 📂 Subdirectory READMEs

- [FastAPI Backend](backend-fastapi/README.md)
- [Go Backend](backend_go/README.md)
- [Frontend](frontend-react/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Keywords

language learning, vocabulary management, study tracking, fastapi, go, gin, nextjs, typescript, sqlite, learning record store

