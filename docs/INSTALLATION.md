# Installation Guide

## Python Version Requirements

This project supports **Python 3.8** and **Python 3.9+** (recommended).

### Check Your Python Version

```bash
python3 --version
# or
python --version
```

## Installation Steps

### Option 1: Python 3.8 (Current System)

If you're using Python 3.8 (like your current system):

```bash
# Navigate to backend directory
cd ai-ml-playground-be-fastapi

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python 3.8 compatible requirements
pip install --upgrade pip
pip install -r requirements-py38.txt
```

### Option 2: Python 3.9+ (Recommended)

For better performance and latest features, upgrade to Python 3.9+:

#### On macOS:
```bash
# Install Python 3.9+ using Homebrew
brew install python@3.11

# Or use pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

#### On Linux:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.9 python3.9-venv python3.9-pip

# Create virtual environment with Python 3.9
python3.9 -m venv venv
source venv/bin/activate
```

#### Then install:
```bash
cd ai-ml-playground-be-fastapi
pip install --upgrade pip
pip install -r requirements-py39+.txt
```

### Option 3: Use Flexible Requirements (Auto-detects)

The main `requirements.txt` now uses version ranges that work with both Python 3.8 and 3.9+:

```bash
cd ai-ml-playground-be-fastapi
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Common Installation Issues

### Issue 1: NumPy Version Error

**Error:** `Could not find a version that satisfies the requirement numpy==1.26.3`

**Solution:** 
- Use `requirements-py38.txt` if on Python 3.8
- Or upgrade to Python 3.9+ and use `requirements-py39+.txt`

### Issue 2: TensorFlow Installation Fails

**Error:** TensorFlow requires specific Python versions

**Solution:**
- Python 3.8: Use TensorFlow 2.13.0 (in requirements-py38.txt)
- Python 3.9+: Use TensorFlow 2.15.0 (in requirements-py39+.txt)

### Issue 3: spaCy Model Not Found

**Solution:**
```bash
# After installing requirements
python -m spacy download en_core_web_sm
```

### Issue 4: PostgreSQL Client Libraries

**On macOS:**
```bash
brew install postgresql
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install libpq-dev
```

**On Windows:**
- Install PostgreSQL from https://www.postgresql.org/download/windows/
- Or use `psycopg2-binary` (already in requirements)

## Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test FastAPI import
python -c "import fastapi; print(fastapi.__version__)"

# Test NumPy import
python -c "import numpy; print(numpy.__version__)"
```

## Quick Start After Installation

```bash
# Set up environment variables
cp .env.example .env
# Edit .env with your database URL

# Run the application
python -m app.main
# Or
uvicorn app.main:app --reload
```

## Docker Alternative

If you have Docker installed, you can avoid Python version issues:

```bash
# Build and run with Docker
docker-compose up -d

# View logs
docker-compose logs -f api
```

The Dockerfile uses Python 3.9, so all packages will install correctly.

## Recommended Setup

For production, we recommend:
- **Python 3.9+** (preferably 3.11)
- **Virtual environment** for isolation
- **requirements-py39+.txt** for latest features

## Troubleshooting

### Clear pip cache
```bash
pip cache purge
```

### Reinstall packages
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Check for conflicts
```bash
pip check
```

## Need Help?

If you encounter issues:
1. Check your Python version: `python --version`
2. Use the appropriate requirements file
3. Ensure virtual environment is activated
4. Upgrade pip: `pip install --upgrade pip`
5. Check error messages for specific package issues

