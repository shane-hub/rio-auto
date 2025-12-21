# Rio Auto - Automated Testing Platform (自动化测试平台)

Rio Auto is a unified automated testing platform designed to streamline API, UI, and performance testing. It provides a modern web interface for managing test cases, executing tasks, and viewing detailed reports.

Rio Auto 是一个统一的自动化测试平台，旨在简化 API、UI 和性能测试。它提供了一个现代化的 Web 界面，用于管理测试用例、执行任务和查看详细报告。

## ✨ Key Features (核心功能)

- **Project Management**: Create and manage multiple testing projects.
- **Test Case Management**: 
  - Support for API (HTTP methods, headers, body), UI (Web), and Performance testing types.
  - Flexible test case creation and editing.
- **Task Execution**: 
  - Asynchronous task execution using Celery.
  - Real-time status tracking (Pending, Running, Completed, Failed).
- **Test Reports**: Detailed execution reports with pass/fail statistics and duration.
- **User Management**: 
  - Role-based access control (Admin/User).
  - User registration and login with JWT authentication.
- **Internationalization (i18n)**: Full support for English and Chinese (Simplified).

## 🛠 Tech Stack (技术栈)

### Backend (后端)
- **Framework**: FastAPI (Python 3.9+)
- **Database ORM**: SQLAlchemy (Async)
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL (Production) / SQLite (Local Dev)
- **Authentication**: OAuth2 with Password Bearer (JWT)

### Frontend (前端)
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Language**: TypeScript
- **UI Library**: Element Plus
- **State Management**: Pinia
- **Routing**: Vue Router
- **Internationalization**: Vue I18n

### Infrastructure (基础设施)
- **Containerization**: Docker & Docker Compose
- **Reverse Proxy**: Nginx (Optional in prod)

## 🚀 Quick Start (快速开始)

### Option 1: Docker (Recommended)
Run the entire stack (Backend, Frontend, PostgreSQL, Redis) with a single command.

```bash
# Clone the repository
git clone <repository-url>
cd rio-auto

# Start services
docker-compose up --build
```

- **Frontend**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs

### Option 2: Local Development (本地开发)

#### 1. Backend Setup
The backend defaults to using SQLite and an in-memory task runner for easy local setup without external dependencies (Redis/Postgres).

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```
*API will be available at http://localhost:8000*

#### 2. Frontend Setup
Requires Node.js 18+.

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
*Frontend will be available at http://localhost:5173*

## ⚙️ Configuration (配置)

### Backend Environment Variables (`backend/.env`)
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./rio_auto.db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key` |
| `ALGORITHM` | Encryption algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `CELERY_BROKER_URL` | Redis URL for Celery | `redis://localhost:6379/0` |
| `CELERY_RESULT_BACKEND` | Redis URL for Results | `redis://localhost:6379/0` |

### Frontend Environment Variables (`frontend/.env`)
| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `/api/v1` |

## 📂 Project Structure (目录结构)

```
rio-auto/
├── backend/                # Python FastAPI Backend
│   ├── app/
│   │   ├── core/           # Config, Security, Database
│   │   ├── models/         # SQLAlchemy Models
│   │   ├── routers/        # API Endpoints
│   │   ├── schemas/        # Pydantic Schemas
│   │   ├── services/       # Business Logic & Task Runners
│   │   └── main.py         # Application Entry Point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Vue 3 Frontend
│   ├── src/
│   │   ├── api/            # API Clients
│   │   ├── components/     # Reusable Components
│   │   ├── locales/        # i18n Translation Files
│   │   ├── router/         # Vue Router Config
│   │   ├── views/          # Page Components
│   │   ├── App.vue
│   │   └── main.ts
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml      # Docker Composition
```

## 📝 API Documentation

Once the backend is running, you can access the interactive API documentation (Swagger UI) at:
- **URL**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🤝 Contribution

Contributions are welcome! Please feel free to submit a Pull Request.
