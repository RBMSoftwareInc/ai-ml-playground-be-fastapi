FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Create directories
RUN mkdir -p uploads trained_models

# Expose port
EXPOSE 5000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]

