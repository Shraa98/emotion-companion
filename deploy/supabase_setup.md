# Supabase Setup Guide

This guide will walk you through setting up Supabase for the Emotion Companion application.

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub or create an account
4. Click "New Project"
5. Fill in project details:
   - **Name**: emotion-companion
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free tier is sufficient for development

6. Click "Create new project" and wait 2-3 minutes for setup

## Step 2: Get API Keys

1. In your project dashboard, click "Settings" (gear icon) in the sidebar
2. Click "API" under Project Settings
3. Copy the following values:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: Long string starting with `eyJ...`
   - **service_role key**: Another long string (keep this secret!)

4. Add these to your `.env` file:
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...
```

## Step 3: Get Database Connection String

1. In Settings → Database
2. Scroll to "Connection string"
3. Select "URI" tab
4. Copy the connection string
5. Replace `[YOUR-PASSWORD]` with your database password
6. Add to `.env`:
```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

## Step 4: Run Database Migrations

### Option A: Using Supabase SQL Editor (Recommended)

1. In your Supabase dashboard, click "SQL Editor" in the sidebar
2. Click "New query"
3. Copy and paste the contents of `migrations/001_create_users.sql`
4. Click "Run" (or press Ctrl+Enter)
5. Repeat for `002_create_journal_entries.sql` and `003_create_audio_entries.sql`

### Option B: Using psql Command Line

```bash
# Install PostgreSQL client if not already installed
# Windows: Download from postgresql.org
# Mac: brew install postgresql
# Linux: sudo apt-get install postgresql-client

# Run migrations
psql "postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres" -f migrations/001_create_users.sql
psql "postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres" -f migrations/002_create_journal_entries.sql
psql "postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres" -f migrations/003_create_audio_entries.sql
```

## Step 5: Create Storage Bucket (For Audio Files)

1. In Supabase dashboard, click "Storage" in the sidebar
2. Click "Create a new bucket"
3. Bucket details:
   - **Name**: `audio-files`
   - **Public bucket**: No (keep private)
4. Click "Create bucket"

## Step 6: Set Up Storage Policies (Optional)

If you want users to upload audio files, you need to set up Row Level Security policies:

1. Click on the `audio-files` bucket
2. Click "Policies" tab
3. Click "New Policy"
4. Create a policy for INSERT:
   ```sql
   CREATE POLICY "Users can upload their own audio"
   ON storage.objects FOR INSERT
   TO authenticated
   WITH CHECK (bucket_id = 'audio-files' AND auth.uid()::text = (storage.foldername(name))[1]);
   ```

## Step 7: Verify Setup

Test your connection:

```python
from supabase import create_client

url = "https://xxxxx.supabase.co"
key = "eyJxxx..."

supabase = create_client(url, key)

# Test query
result = supabase.table("users").select("*").execute()
print("Connection successful!", result)
```

## Troubleshooting

### Cannot connect to database
- Check that your IP is allowed (Supabase allows all IPs by default)
- Verify your password is correct
- Ensure you're using the correct connection string

### Migrations fail
- Make sure you're running them in order (001, 002, 003)
- Check for syntax errors in the SQL files
- Verify you have the correct permissions

### Storage upload fails
- Ensure the bucket exists
- Check that storage policies are set up correctly
- Verify your service_role key is correct

## Next Steps

Once Supabase is set up:
1. Update your `.env` file with all the credentials
2. Start the backend: `python -m backend.app`
3. Start the frontend: `streamlit run streamlit_app/app.py`
4. Test creating a journal entry!
