@echo off
setlocal enabledelayedexpansion

echo ==================================================
echo       File Guessr - Easy Setup
echo ==================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

:: 2. Setup Virtual Environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: 3. Install Dependencies
echo [INFO] Installing/Updating dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. Create Desktop Shortcut
echo [INFO] Creating desktop shortcut...
python setup_shortcut.py

echo.
echo ==================================================
echo [SUCCESS] Setup complete! 
echo You can now use the "File Guessr" shortcut on your desktop.
echo ==================================================
pause
