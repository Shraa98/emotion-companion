# Emotion Companion - Environment Setup Instructions

## Your Supabase Credentials (from screenshot):

**Project URL**: https://xbaohqivkendyamjataz.supabase.co
**API Key (anon)**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiYW9ocWl2a2VuZHlhbWphdGF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5NTAxMjYsImV4cCI6MjA0ODUyNjEyNn0.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiYW9ocWl2a2VuZHlhbWphdGF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5NTAxMjYsImV4cCI6MjA0ODUyNjEyNn0

---

## Step 1: Get Your Database Password

1. In Supabase dashboard, go to **Settings** → **Database**
2. Find the **Connection string** section
3. Select **URI** tab
4. Copy the connection string
5. Note your database password (you set this when creating the project)

---

## Step 2: Create .env File

Run this command in PowerShell:

```powershell
cd "c:\Users\Dell\OneDrive\Desktop\Emotions Companion AI\emotion-companion"

# Create .env file
@"
# Supabase Configuration
SUPABASE_URL=https://xbaohqivkendyamjataz.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiYW9ocWl2a2VuZHlhbWphdGF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5NTAxMjYsImV4cCI6MjA0ODUyNjEyNn0.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhiYW9ocWl2a2VuZHlhbWphdGF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5NTAxMjYsImV4cCI6MjA0ODUyNjEyNn0
SUPABASE_SERVICE_KEY=your-service-key-here

# Database Configuration (REPLACE [YOUR-PASSWORD] with your actual password!)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xbaohqivkendyamjataz.supabase.co:5432/postgres

# Application Configuration
SECRET_KEY=emotion-companion-secret-key-12345
ENVIRONMENT=development

# NLP Model Configuration
USE_HF_MODELS=true
HF_CACHE_DIR=./model_cache

# Audio Configuration
ENABLE_AUDIO=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
"@ | Out-File -FilePath .env -Encoding UTF8
```

**IMPORTANT**: After creating the file, edit `.env` and replace `[YOUR-PASSWORD]` with your actual database password!

---

## Step 3: Run Database Migrations

1. Go to your Supabase dashboard
2. Click **SQL Editor** in the left sidebar
3. Click **"New query"**
4. Copy and paste the content from `migrations/001_create_users.sql`
5. Click **Run** (or press Ctrl+Enter)
6. Repeat for `migrations/002_create_journal_entries.sql`
7. Repeat for `migrations/003_create_audio_entries.sql`

---

## Step 4: Run the Application

Open TWO PowerShell windows:

**Window 1 - Backend:**
```powershell
cd "c:\Users\Dell\OneDrive\Desktop\Emotions Companion AI\emotion-companion"
python -m backend.app
```

**Window 2 - Frontend:**
```powershell
cd "c:\Users\Dell\OneDrive\Desktop\Emotions Companion AI\emotion-companion"
streamlit run streamlit_app/app.py
```

---

## Quick Test (Without Database)

If you want to test the NLP analysis without setting up the database first:

```powershell
cd "c:\Users\Dell\OneDrive\Desktop\Emotions Companion AI\emotion-companion"
python -c "from backend.nlp import analyze_text; import json; result = analyze_text('I feel amazing today!'); print(json.dumps(result, indent=2, default=str))"
```

---

## Need Help?

If you get stuck, let me know at which step!
