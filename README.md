# 📰 Belsons News - Full-Stack News Aggregation Platform

A modern, full-stack news aggregation application built with Django REST Framework and Angular 21. Fetch, filter, and browse news articles from multiple sources across different categories, languages, and countries.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [API Documentation](#api-documentation)
- [Database Setup](#database-setup)

---

## 🎯 Overview

Belsons News is a comprehensive news aggregation platform that:

- **Fetches news articles** from multiple news sources via NewsAPI
- **Stores news data** in PostgreSQL with optimized indexing
- **Provides a REST API** for querying and filtering news articles
- **Offers a modern UI** built with Angular 21 and Tailwind CSS
- **Supports background tasks** using Celery and Redis for scheduled news fetching

**Perfect for:** Building news aggregation websites, news reader applications, or integrating real-time news data into your platform.

---

## 🛠️ Tech Stack

### Backend

- **Framework:** Django 5.2.10
- **API:** Django REST Framework 3.16.1
- **Database:** PostgreSQL 15+ (with psycopg3)
- **Task Queue:** Celery 5.6.2 with Redis 7.1.0
- **News Source:** NewsAPI (newsapi-python 0.2.7)
- **Filtering:** django-filter 25.2
- **CORS:** django-cors-headers 4.9.0

### Frontend

- **Framework:** Angular 21.1.0
- **Styling:** Tailwind CSS 4.1.18
- **HTTP Client:** RxJS 7.8.0
- **Build Tool:** Angular CLI 21.1.2

### Infrastructure

- **Containerization:** Docker & Docker Compose
- **Python Version:** 3.10+
- **Node.js Version:** 18+

---

## 📁 Project Structure

```
belsons_test/
├── README.md                          # This file
├── API_DOCUMENTATION.md               # Detailed API documentation
│
├── backend/                           # Django Backend
│   ├── manage.py                      # Django management script
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile                     # Backend Docker image
│   ├── docker-compose.yaml            # Docker Compose configuration
│   │
│   ├── config/                        # Django Configuration
│   │   ├── settings.py                # Main settings file
│   │   ├── urls.py                    # URL routing
│   │   ├── celery.py                  # Celery configuration
│   │   └── asgi.py, wsgi.py           # Server configurations
│   │
│   └── apps/news/                     # News Application
│       ├── models.py                  # Database models
│       ├── views.py                   # API views
│       ├── serializers.py             # DRF serializers
│       ├── urls.py                    # URL patterns
│       ├── filters.py                 # Custom filters
│       ├── pagination.py              # Pagination class
│       ├── tasks.py                   # Celery tasks
│       └── migrations/                # Database migrations
│
└── frontend/                          # Angular Frontend
    ├── package.json                   # NPM dependencies
    ├── angular.json                   # Angular CLI configuration
    │
    └── src/
        ├── main.ts                    # Angular bootstrap
        ├── index.html                 # HTML entry point
        ├── styles.css                 # Global styles
        │
        └── app/
            ├── components/            # Angular Components
            ├── services/              # Angular Services
            └── models/                # TypeScript interfaces
```

---

## ✨ Features

### Backend Features

- ✅ **RESTful API** with comprehensive endpoint coverage
- ✅ **Advanced Filtering** by category, country, source, and language
- ✅ **Full-Text Search** on article titles
- ✅ **Sorting & Ordering** by publication date, creation date, and title
- ✅ **Pagination** with customizable page size
- ✅ **Automated News Fetching** via Celery scheduled tasks
- ✅ **Database Optimization** with strategic indexing
- ✅ **CORS Support** for cross-origin requests

### Frontend Features

- ✅ **Modern Angular 21 UI** with responsive design
- ✅ **Real-time News Display** with dynamic filtering
- ✅ **Advanced Search** capabilities
- ✅ **Category & Country Filters** for personalized news
- ✅ **Pagination Support** for browsing articles
- ✅ **Clean, Intuitive Interface** with Tailwind CSS

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Docker** (20.10+) and **Docker Compose** (1.29+)
  - [Install Docker](https://docs.docker.com/get-docker/)
- **Git** (for cloning the repository)
- **Node.js** 18+ and **npm** 10+ (for local frontend development)

### Clone the Repository

```bash
git clone https://github.com/ahmed123456787/belsons_test
cd belsons_test
```

### Create Environment File

Create a `.env` file in the project root directory:

```bash
cat > .env << EOF
# Django Settings
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-in-production

# PostgreSQL Database
POSTGRES_DB=news_db
POSTGRES_USER=news_user
POSTGRES_PASSWORD=secure_password_here
POSTGRES_HOST=db

# NewsAPI
NEWS_API_KEY=your_newsapi_key_here

# Redis
REDIS_URL=redis://redis:6379/0

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
EOF
```

**Get your NewsAPI Key:**

1. Visit [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key and paste it in the `.env` file

---

## 📦 Running the Backend

### Option 1: Backend with Docker Compose (Recommended)

This is the easiest way to run the backend with all dependencies (PostgreSQL, Redis).

#### Step 1: Navigate to Backend Directory

```bash
cd backend
```

#### Step 2: Start Docker Compose

```bash
docker-compose up -d
```

This will:

- Start PostgreSQL database
- Start Redis cache
- Build and start Django backend
- Run database migrations automatically

#### Step 3: Access the Backend

- **API Base URL:** http://localhost:8000
- **API Endpoints:** http://localhost:8000/apis/v1/
- **Django Admin:** http://localhost:8000/admin/
  - Default credentials: `admin` / `admin`

#### Step 4: View Logs

```bash
docker-compose logs -f web
```

#### Step 5: Stop Backend

```bash
docker-compose down
```

---

### Option 2: Backend without Docker (Local Development)

If you prefer to run the backend locally without Docker:

#### Step 1: Navigate to Backend Directory

```bash
cd backend
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Run Migrations

```bash
python manage.py migrate
```

#### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

#### Step 6: Start Development Server

```bash
python manage.py runserver
```

Backend will be available at: http://localhost:8000

#### Step 7: Start Celery Worker (Optional)

In a new terminal:

```bash
celery -A config worker -l info
```

#### Step 8: Start Celery Beat (Optional)

In another terminal:

```bash
celery -A config beat -l info
```

---

## 🎨 Running the Frontend

### Option 1: Frontend Local Development

#### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

#### Step 2: Install Dependencies

```bash
npm install
```

#### Step 3: Start Development Server

```bash
npm start
```

Frontend will be available at: http://localhost:4200

#### Step 4: Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

---

## 📖 API Documentation

The API is fully documented with detailed endpoint specifications, parameters, and examples.

### Quick API Reference

| Method | Endpoint               | Description                                          |
| ------ | ---------------------- | ---------------------------------------------------- |
| GET    | `/apis/v1/news/`       | List all news articles (with filtering & pagination) |
| GET    | `/apis/v1/news/<id>/`  | Get single article details                           |
| GET    | `/apis/v1/sources/`    | List all news sources                                |
| GET    | `/apis/v1/categories/` | List all categories                                  |
| GET    | `/apis/v1/languages/`  | List all supported languages                         |
| GET    | `/apis/v1/countries/`  | List all supported countries                         |

### Example API Calls

**Get latest technology news:**

```bash
curl "http://localhost:8000/apis/v1/news/?category=1&ordering=-published_at"
```

**Search for "AI" articles:**

```bash
curl "http://localhost:8000/apis/v1/news/?title=AI"
```

**Get news from United States:**

```bash
curl "http://localhost:8000/apis/v1/news/?country=1"
```

**Get paginated results (20 articles per page):**

```bash
curl "http://localhost:8000/apis/v1/news/?page=1&page_size=20"
```

### For Complete API Documentation

See the detailed [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) file for:

- All available endpoints
- Complete parameter specifications
- Request/response examples
- Error handling information
- Pagination details
- Filtering and searching capabilities

---

## 🗄️ Database Setup

### Database Schema

The project uses PostgreSQL with the following main models:

```
Category
├── id (Primary Key)
├── name (Business, Entertainment, General, Health, Science, Sports, Technology)

Language
├── id (Primary Key)
├── code (en, fr, ar)
├── name (Display Name)

Country
├── id (Primary Key)
├── code (us, fr, eg, ca)
├── name (Display Name)

Source (News Source)
├── id (Primary Key)
├── source_id (Unique, from NewsAPI)
├── name
├── description
├── url
├── category_id (Foreign Key → Category)
├── language_id (Foreign Key → Language)
├── country_id (Foreign Key → Country)

NewsArticle
├── id (Primary Key)
├── title
├── description
├── url (Unique)
├── content
├── image_url
├── published_at (DateTime)
├── created_at (Auto)
├── source_id (Foreign Key → Source)
├── category_id (Foreign Key → Category)
├── language_id (Foreign Key → Language)
├── country_id (Foreign Key → Country)
```

### Auto-Migrations

Database migrations run automatically when using Docker Compose. For local development:

```bash
python manage.py migrate
```

### Seed Data

Reference data (categories, languages, countries) is seeded automatically during migrations.

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
# Django Configuration
DEBUG=True                              # Set to False in production
SECRET_KEY=change-me-in-production     # Generate a secure key

# Database Configuration
POSTGRES_DB=news_db
POSTGRES_USER=news_user
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=postgres                 # 'postgres' for Docker, 'localhost' for local

# NewsAPI Configuration
NEWSAPI_KEY=your_api_key_from_newsapi  # Get from https://newsapi.org/

# Redis Configuration
REDIS_URL=redis://redis:6379/0         # 'redis' for Docker, 'localhost' for local

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

## 📝 Additional Documentation

- **Detailed API Endpoints** → [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Django Configuration** → `backend/config/settings.py`
- **Frontend Components** → `frontend/src/app/components/`
- **Database Models** → `backend/apps/news/models.py`

---

## 🤝 Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 📞 Support

For issues or questions:

1. Review the [API Documentation](./API_DOCUMENTATION.md)
2. Check Docker/application logs:
   ```bash
   docker-compose logs -f [service-name]
   ```
3. Verify environment variables in `.env` file

---

**Happy Coding! 🚀**
