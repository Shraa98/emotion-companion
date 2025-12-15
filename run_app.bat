@echo off
echo Starting Emotion Companion...
set PYTHONIOENCODING=utf-8
start "Backend" cmd /k "python -m backend.app"
timeout /t 5
start "Frontend" cmd /k "streamlit run streamlit_app/app.py"
echo App started! Frontend should open in browser.
pause
