@echo off
echo ==========================================
echo   Emotion Companion - Git Setup Helper
echo ==========================================
echo.
echo This script will initialize a local git repository 
echo and commit all your current files.
echo.
echo 1. Initializing git...
git init

echo.
echo 2. Adding all files...
git add .

echo.
echo 3. Creating initial commit...
git commit -m "Initial commit of Emotion Companion AI"

echo.
echo ==========================================
echo   Local Setup Complete!
echo ==========================================
echo.
echo Now, go to https://github.com/new and create a repository.
echo Then, copy the commands under "...or push an existing repository"
echo and paste them below (or in a new terminal).
echo.
echo Example:
echo   git remote add origin https://github.com/YOUR_USER/REPO.git
echo   git branch -M main
echo   git push -u origin main
echo.
cmd /k
