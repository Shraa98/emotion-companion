@echo off
echo Starting Emotion Companion...
set PYTHONIOENCODING=utf-8

:: Check if models exist
if not exist "backend\models\sentiment_model.joblib" (
    echo Models not found. Training initial models...
    python -m backend.train_models
)

start "Backend" cmd /k "python -m backend.app"
timeout /t 5
start "Frontend" cmd /k "streamlit run streamlit_app/app.py"
echo App started! Frontend should open in browser.
pause
