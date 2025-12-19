# FastAPI Backend Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.9+
- PostgreSQL 12+
- pip

### 2. Installation

```bash
# Navigate to backend directory
cd ai-ml-playground-be-fastapi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install spaCy model
python -m spacy download en_core_web_sm
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb ai_ml_playground

# Or using psql
psql -U postgres
CREATE DATABASE ai_ml_playground;
```

### 4. Environment Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# Update DATABASE_URL, SECRET_KEY, etc.
```

### 5. Run Application

```bash
# Development mode
python -m app.main

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

### 6. Verify Installation

- API: http://localhost:5000
- Docs: http://localhost:5000/docs
- Health: http://localhost:5000/health

## Docker Setup (Alternative)

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f api
```

## Database Migrations

When Alembic is fully configured:

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Testing Endpoints

### Example: NLP Search
```bash
curl -X POST "http://localhost:5000/api/v1/nlp/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "red running shoes",
    "limit": 10
  }'
```

### Example: Fraud Detection
```bash
curl -X POST "http://localhost:5000/api/v1/fraud/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "txn_123",
    "amount": 50000,
    "user_id": "user_123"
  }'
```

## Project Structure

```
ai-ml-playground-be-fastapi/
├── app/
│   ├── main.py              # Application entry
│   ├── core/                # Core configuration
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # AI/ML services
│   └── api/v1/              # API routes
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Key Features

✅ **90+ API Endpoints** across 9 industries
✅ **AI/ML Services** - NLP, Vision, Forecasting, ML
✅ **Database Models** - User, Product, Order, Customer, Analytics
✅ **Production Ready** - CORS, error handling, logging
✅ **Auto Documentation** - Swagger UI and ReDoc

## Next Steps

1. Configure database connection in `.env`
2. Run database migrations
3. Test API endpoints
4. Connect frontend to backend
5. Deploy to production

## Troubleshooting

**Import errors:**
- Ensure virtual environment is activated
- Install all requirements: `pip install -r requirements.txt`

**Database connection errors:**
- Check PostgreSQL is running
- Verify DATABASE_URL in `.env`
- Ensure database exists

**Model loading errors:**
- Run: `python -m spacy download en_core_web_sm`
- Check MODELS_DIR path in `.env`

## Support

For issues, check:
- API documentation at `/docs`
- Logs in console
- Database connection status

