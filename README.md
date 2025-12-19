# AI/ML Playground Backend - FastAPI

Comprehensive FastAPI backend for the AI/ML Playground platform, covering 9 industries with 90+ use cases.

## 🚀 Features

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM with PostgreSQL support
- **AI/ML Services** - NLP, Computer Vision, Forecasting, ML models
- **90+ API Endpoints** - Covering all industries and use cases
- **Comprehensive Database Schemas** - User, Product, Order, Customer, Analytics models
- **Production Ready** - CORS, error handling, logging

## 📋 Requirements

- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)

## 🛠️ Installation

1. **Clone and navigate to the backend directory:**
```bash
cd ai-ml-playground-be-fastapi
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install spaCy language model:**
```bash
python -m spacy download en_core_web_sm
```

5. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

6. **Set up database:**
```bash
# Create PostgreSQL database
createdb ai_ml_playground

# Run migrations (when Alembic is configured)
alembic upgrade head
```

## 🏃 Running the Application

**Development mode:**
```bash
python -m app.main
# Or
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

**Production mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4
```

The API will be available at:
- API: `http://localhost:5000`
- Docs: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## 📁 Project Structure

```
ai-ml-playground-be-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   └── database.py         # Database setup
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── customer.py
│   │   └── ...
│   ├── schemas/                # Pydantic schemas
│   │   └── common.py
│   ├── services/               # AI/ML services
│   │   ├── nlp_service.py
│   │   ├── vision_service.py
│   │   ├── forecasting_service.py
│   │   └── ml_service.py
│   └── api/
│       └── v1/                  # API routes
│           ├── ecommerce.py     # 27 endpoints
│           ├── healthcare.py
│           ├── fintech.py
│           ├── travel.py
│           └── ...
├── requirements.txt
├── .env.example
└── README.md
```

## 🔌 API Endpoints

### E-commerce (27 endpoints)
- `/api/v1/nlp/search` - Semantic product search
- `/api/v1/vss/upload` - Visual similarity search
- `/api/v1/bundle/recommend` - Bundle recommendations
- `/api/v1/eta/predict` - ETA prediction
- `/api/v1/pricing/recommend` - Dynamic pricing
- `/api/v1/fraud/predict` - Fraud detection
- `/api/v1/churn/predict` - Churn prediction
- ... and 20 more

### Other Industries
- Healthcare (6 endpoints)
- Fintech (6 endpoints)
- Travel (6 endpoints)
- Hospitality (6 endpoints)
- Entertainment (6 endpoints)
- Manufacturing (6 endpoints)
- Real Estate (6 endpoints)
- Retail (6 endpoints)

See `API_SPECIFICATION.md` in the frontend directory for complete API documentation.

## 🤖 AI/ML Services

### NLP Service
- Semantic search using sentence transformers
- Sentiment analysis
- Named entity recognition
- Text embeddings

### Vision Service
- Image similarity search
- Object detection
- Feature extraction
- CLIP-based embeddings

### Forecasting Service
- Time series forecasting
- ETA prediction
- Demand forecasting
- Sales forecasting

### ML Service
- Fraud detection
- Churn prediction
- Customer segmentation
- Price recommendation

## 🗄️ Database Models

- **User** - User authentication and preferences
- **Industry** - Industry definitions
- **UseCase** - Use case catalog
- **Product** - Product catalog with embeddings
- **ProductVariant** - Product variants
- **Order** - Order management
- **Customer** - Customer data and segmentation
- **Transaction** - Transaction and fraud data
- **Inventory** - Inventory management
- **Analytics** - Analytics events and A/B tests

## 🔧 Configuration

Key configuration options in `.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `CORS_ORIGINS` - Allowed CORS origins
- `SECRET_KEY` - Secret key for JWT/sessions
- `MODELS_DIR` - Directory for trained ML models
- `OPENAI_API_KEY` - OpenAI API key (optional)
- `HUGGINGFACE_API_KEY` - HuggingFace API key (optional)

## 📦 Dependencies

Key packages:
- `fastapi` - Web framework
- `sqlalchemy` - ORM
- `sentence-transformers` - NLP embeddings
- `scikit-learn` - ML algorithms
- `pandas` - Data processing
- `numpy` - Numerical computing
- `pillow` - Image processing
- `opencv-python` - Computer vision

See `requirements.txt` for complete list.

## 🧪 Testing

```bash
pytest
```

## 📝 API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`

## 🚀 Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Environment Variables

Set all required environment variables in production:
- Database credentials
- Secret keys
- API keys
- CORS origins

## 🔐 Security

- CORS middleware configured
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy
- File upload size limits
- Error handling without exposing internals

## 📊 Monitoring

- Health check endpoint: `/health`
- Structured logging ready
- Error tracking ready

## 🤝 Contributing

1. Follow FastAPI best practices
2. Add type hints to all functions
3. Write docstrings for all endpoints
4. Update API documentation

## 📄 License

Proprietary - RBM Software

## 🆘 Support

For issues and questions, contact the development team.

---

**Built with FastAPI, SQLAlchemy, and modern AI/ML libraries**

