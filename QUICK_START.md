# 🚀 Quick Start Guide - Test Mode (No Database Required)

The Emotion Companion is now ready to run in **TEST MODE** without requiring database setup!

## ✅ What's Already Done

- ✅ All Python packages installed
- ✅ NLP models downloaded (sentiment, emotion, themes)
- ✅ Test mode backend created (no database needed)
- ✅ Simplified frontend created

---

## 🎯 Run the Application (2 Steps)

### Step 1: Start Backend (Terminal 1)

Open PowerShell and run:

```powershell
cd "c:\Users\Dell\OneDrive\Desktop\Emotions Companion AI\emotion-companion"
python -m backend.app_no_db
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Starting Emotion Companion API (Test Mode - No Database)
⚠️  Database connection disabled for testing
```

### Step 2: Start Frontend (Terminal 2)

Open a **NEW** PowerShell window and run:

```powershell
cd "c:\Users\Dell\OneDrive\Desktop\Emotions Companion AI\emotion-companion"
streamlit run streamlit_app/app_simple.py
```

**Browser will open automatically at:** http://localhost:8501

---

## 🎨 How to Use

1. **Write a journal entry** in the text area (e.g., "I feel anxious about my presentation tomorrow")
2. **Click "Analyze Entry"**
3. **See results:**
   - Emotion detection (with emoji)
   - Mood score (0-10)
   - Sentiment (positive/negative/neutral)
   - Themes extracted
   - Personalized coping suggestions

---

## 📝 Test Mode vs Full Mode

### Test Mode (Current - No Database)
- ✅ All NLP analysis works
- ✅ No setup required
- ❌ Entries are NOT saved
- ❌ No dashboard/history
- ❌ No audio upload

### Full Mode (Requires Database)
- ✅ All features
- ✅ Entries saved to database
- ✅ Dashboard with mood trends
- ✅ Audio upload support
- ⚠️ Requires Supabase setup

---

## 🔧 Database Connectivity Issue

Your Supabase database hostname cannot be reached from your network. This could be due to:

1. **Network/Firewall**: Your network might be blocking Supabase
2. **VPN Required**: Some networks require VPN to access cloud databases
3. **DNS Issue**: Your DNS cannot resolve the Supabase hostname

### Solutions:

**Option A: Use Mobile Hotspot**
- Connect your computer to mobile hotspot
- Try running the full backend again

**Option B: Use VPN**
- Connect to a VPN
- Try accessing Supabase

**Option C: Continue in Test Mode**
- Use the test mode for now
- Set up database later when on a different network

---

## 🎉 What You Can Do Now

**Immediate:**
1. Test the NLP analysis with different journal entries
2. See how emotions are detected
3. Get personalized coping suggestions
4. Understand how the system works

**Later (When Database Works):**
1. Run migrations in Supabase
2. Use full backend (`python -m backend.app`)
3. Use full frontend (`streamlit run streamlit_app/app.py`)
4. Get dashboard with mood trends
5. Save and track journal entries over time

---

## 📞 Need Help?

If you have questions or issues, check:
- Backend logs in Terminal 1
- Frontend errors in Terminal 2
- API docs: http://localhost:8000/api/docs (when backend is running)

---

**Ready to test? Run the two commands above!** 🚀
