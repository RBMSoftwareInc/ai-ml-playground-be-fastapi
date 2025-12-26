# Database Setup Guide

## Problem

When running `alembic upgrade head`, you may encounter:
```
psycopg2.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: fe_sendauth: no password supplied
```

This means your `.env` file has a placeholder DATABASE_URL that needs to be configured with actual PostgreSQL credentials.

## Solution

### Step 1: Check PostgreSQL Status

```bash
pg_isready
# Should show: /var/run/postgresql:5432 - accepting connections
```

### Step 2: Create Database and User

You have several options:

#### Option A: Use Default Postgres User (Recommended for Development)

1. **Connect as postgres superuser:**
   ```bash
   sudo -u postgres psql
   ```

2. **Create the database:**
   ```sql
   CREATE DATABASE rbm_ai_ml_playground;
   ```

3. **Create a user (optional, if you want a dedicated user):**
   ```sql
   CREATE USER rbm WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE rbm_ai_ml_playground TO rbm;
   ```

4. **Exit psql:**
   ```sql
   \q
   ```

5. **Update `.env` file:**
   ```bash
   # For postgres user (no password if using peer authentication)
   DATABASE_URL=postgresql://postgres@localhost:5432/rbm_ai_ml_playground
   
   # OR with password
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rbm_ai_ml_playground
   
   # OR for custom user
   DATABASE_URL=postgresql://rbm:your_secure_password@localhost:5432/rbm_ai_ml_playground
   ```

#### Option B: Use Peer Authentication (No Password)

If your PostgreSQL is configured for peer authentication (common on Linux):

1. **Create database as postgres user:**
   ```bash
   sudo -u postgres createdb rbm_ai_ml_playground
   ```

2. **Update `.env` file:**
   ```bash
   DATABASE_URL=postgresql://postgres@localhost:5432/rbm_ai_ml_playground
   ```

#### Option C: Use Existing Database

If you already have a PostgreSQL database:

1. **Update `.env` file with your credentials:**
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   ```

### Step 3: Test Connection

```bash
# Test with psql
psql -U postgres -d rbm_ai_ml_playground -c "SELECT version();"

# Or test with Python
source venv/bin/activate
python -c "from app.core.config import settings; from sqlalchemy import create_engine; engine = create_engine(settings.DATABASE_URL); conn = engine.connect(); print('Connection successful!'); conn.close()"
```

### Step 4: Run Migrations

Once the database is configured:

```bash
source venv/bin/activate
alembic upgrade head
```

## Common Issues

### Issue 1: "role does not exist"

**Error:** `FATAL: role "username" does not exist`

**Solution:** Create the PostgreSQL user:
```bash
sudo -u postgres psql
CREATE USER username WITH PASSWORD 'password';
```

### Issue 2: "database does not exist"

**Error:** `FATAL: database "rbm_ai_ml_playground" does not exist`

**Solution:** Create the database:
```bash
sudo -u postgres createdb rbm_ai_ml_playground
```

### Issue 3: "password authentication failed"

**Error:** `FATAL: password authentication failed for user "username"`

**Solution:** 
1. Check your password in `.env`
2. Or reset the password:
   ```bash
   sudo -u postgres psql
   ALTER USER username WITH PASSWORD 'new_password';
   ```

### Issue 4: "Peer authentication failed"

**Error:** `FATAL: Peer authentication failed for user "postgres"`

**Solution:** Use password authentication or connect as the postgres system user:
```bash
sudo -u postgres psql
```

## Quick Setup Script

You can use this script to set up the database quickly:

```bash
#!/bin/bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE rbm_ai_ml_playground;
CREATE USER rbm WITH PASSWORD 'changeme';
GRANT ALL PRIVILEGES ON DATABASE rbm_ai_ml_playground TO rbm;
\q
EOF

# Update .env (you'll need to do this manually)
echo "Update your .env file with:"
echo "DATABASE_URL=postgresql://rbm:changeme@localhost:5432/rbm_ai_ml_playground"
```

## Environment File Format

Your `.env` file should have:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/rbm_ai_ml_playground
```

**Format breakdown:**
- `postgresql://` - Protocol
- `username` - PostgreSQL username
- `password` - PostgreSQL password (can be omitted for peer auth)
- `@localhost:5432` - Host and port
- `/rbm_ai_ml_playground` - Database name

## Security Notes

1. **Never commit `.env` to version control** - It's already in `.gitignore`
2. **Use strong passwords** in production
3. **Consider using environment variables** instead of `.env` file in production
4. **Use connection pooling** for production deployments

## Next Steps

After setting up the database:

1. ✅ Database created
2. ✅ `.env` file updated with correct DATABASE_URL
3. ✅ Test connection works
4. ✅ Run `alembic upgrade head` to create tables
5. ✅ Start the application: `python -m app.main`

