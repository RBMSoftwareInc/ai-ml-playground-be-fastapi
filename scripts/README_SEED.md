# Content Seeding Script

This script migrates hardcoded industry and use case data from the frontend into the database.

## Prerequisites

1. Database migrations must be run first:
   ```bash
   cd ai-ml-playground-be-fastapi
   alembic upgrade head
   ```

2. Ensure your database connection is configured in `.env`:
   ```
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rbm_ai_ml_playground
   ```

## Running the Seed Script

```bash
cd ai-ml-playground-be-fastapi
python scripts/seed_content.py
```

The script will:
- Create industries (Healthcare, Manufacturing, Real Estate)
- Create categories for each industry
- Create use cases with their details
- Create themes with color configurations
- Create content blocks for descriptions and taglines

## What Gets Created

### Industries
- Healthcare AI
- Manufacturing AI  
- Real Estate AI

### For Each Industry:
- **Industry record** with name, description, icon
- **Theme** with primary/secondary colors
- **Content blocks** for description and tagline
- **Categories** (e.g., "Clinical Intelligence", "Equipment", "Valuation")
- **Use cases** with:
  - Display name and descriptions
  - Metadata (duration, difficulty, benefits, tech stack)
  - Content blocks for short description and "how it works"

## Verification

After running the script, verify the data:

1. Check API endpoint:
   ```bash
   curl http://localhost:5000/api/v1/public/industries
   ```

2. Check admin panel:
   - Navigate to `/admin/industries`
   - You should see all industries listed

3. Check frontend:
   - Navigate to `/industries/healthcare` (or other industry)
   - Content should load from database

## Adding More Industries

To add more industries, edit `scripts/seed_content.py` and add to the `INDUSTRIES_DATA` dictionary. The script is idempotent - running it multiple times will update existing records rather than create duplicates.

## Notes

- The script uses `industry_id` as the unique identifier
- Use case keys must be unique across all industries
- Icons are stored as strings (e.g., "LocalHospital") which are mapped to React components in the frontend
- The script will update existing records if they already exist

