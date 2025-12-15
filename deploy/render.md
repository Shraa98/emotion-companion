# Deployment Guide

This guide covers deploying the Emotion Companion application to production.

## Architecture Overview

- **Backend (FastAPI)**: Deployed to Render or Railway
- **Frontend (Streamlit)**: Deployed to Streamlit Cloud
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage

---

## Part 1: Deploy Backend to Render

### Prerequisites
- GitHub account
- Render account (free tier available at render.com)
- Supabase project set up (see `supabase_setup.md`)

### Step 1: Prepare Repository

1. Create a `Dockerfile.backend` in the project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Download NLTK data
RUN python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('stopwords')"

# Copy application code
COPY backend/ ./backend/
COPY utils/ ./utils/

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Push your code to GitHub

### Step 2: Create Render Web Service

1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `emotion-companion-api`
   - **Environment**: `Docker`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Dockerfile Path**: `Dockerfile.backend`
   - **Instance Type**: Free (or upgrade for better performance)

### Step 3: Set Environment Variables

In Render dashboard, add these environment variables:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=your-production-secret-key-here
ENVIRONMENT=production
USE_HF_MODELS=true
ENABLE_AUDIO=false
CORS_ORIGINS=https://your-streamlit-app.streamlit.app
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your API will be available at: `https://emotion-companion-api.onrender.com`

### Step 5: Test API

```bash
curl https://emotion-companion-api.onrender.com/api/health
```

---

## Part 2: Deploy Frontend to Streamlit Cloud

### Step 1: Prepare Streamlit Configuration

1. Create `.streamlit/config.toml` in your project:

```toml
[theme]
primaryColor = "#4A90E2"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F4F8"
textColor = "#2C3E50"
font = "sans serif"

[server]
headless = true
port = 8501
```

2. Create `requirements-streamlit.txt`:

```
streamlit==1.28.1
requests==2.31.0
pandas==2.1.3
plotly==5.18.0
```

### Step 2: Update API URL

In `streamlit_app/app.py`, update the API URL to use environment variable:

```python
import os
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
```

### Step 3: Deploy to Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/app.py`
   - **App URL**: Choose a custom URL

5. Click "Advanced settings" and add environment variable:
   ```
   API_URL=https://emotion-companion-api.onrender.com/api
   ```

6. Click "Deploy!"

### Step 4: Access Your App

Your app will be available at: `https://your-app-name.streamlit.app`

---

## Part 3: Alternative - Deploy to Railway

Railway is another excellent option for deploying the backend.

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 2: Login and Initialize

```bash
railway login
railway init
```

### Step 3: Deploy

```bash
railway up
```

### Step 4: Set Environment Variables

```bash
railway variables set SUPABASE_URL=https://xxxxx.supabase.co
railway variables set SUPABASE_ANON_KEY=eyJxxx...
railway variables set DATABASE_URL=postgresql://...
# ... add all other variables
```

### Step 5: Get URL

```bash
railway domain
```

---

## Monitoring and Maintenance

### Health Checks

Set up monitoring for your API:
- Render: Built-in health checks at `/api/health`
- Use UptimeRobot or similar service for external monitoring

### Logs

- **Render**: View logs in dashboard under "Logs" tab
- **Streamlit Cloud**: View logs in app settings
- **Railway**: `railway logs`

### Scaling

For production use:
- Upgrade Render instance type for better performance
- Consider adding Redis for caching
- Use CDN for static assets
- Enable database connection pooling

### Security Checklist

- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS (automatic on Render/Streamlit Cloud)
- [ ] Set proper CORS origins
- [ ] Use environment variables for all secrets
- [ ] Enable Supabase Row Level Security
- [ ] Regular security updates for dependencies

---

## Troubleshooting

### Backend won't start
- Check environment variables are set correctly
- Review logs for error messages
- Ensure database migrations have run
- Verify Supabase connection

### Frontend can't connect to backend
- Check CORS settings in backend
- Verify API_URL is correct in Streamlit
- Test API endpoint directly with curl

### Slow performance
- Upgrade instance type
- Enable caching
- Optimize database queries
- Consider using HuggingFace model API instead of local models

---

## Cost Estimates

### Free Tier (Development/Demo)
- Render Free: $0/month (sleeps after inactivity)
- Streamlit Cloud: $0/month
- Supabase Free: $0/month (500MB database, 1GB storage)
- **Total: $0/month**

### Production (Low Traffic)
- Render Starter: $7/month
- Streamlit Cloud: $0/month (or $20/month for private apps)
- Supabase Pro: $25/month
- **Total: ~$32-52/month**

### Production (High Traffic)
- Render Standard: $25/month
- Streamlit Cloud Teams: $250/month
- Supabase Pro: $25/month
- **Total: ~$300/month**
