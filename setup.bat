@echo off
setlocal enabledelayedexpansion

echo ==================================================
echo       File Guessr - Integrated Setup
echo ==================================================
echo.

:: --- Part 0: Check for Administrator Privileges ---
echo [1/4] Checking for Administrator privileges...
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] This script requires Administrator privileges to configure Windows Services.
    echo [!] Attempting to elevate...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
cd /d "%~dp0"

:: --- Part 1: Python Environment Setup ---
echo.
echo [2/4] Setting up Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10+ and add it to PATH.
    pause & exit /b 1
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (echo [ERROR] Dependency installation failed! & pause & exit /b 1)

:: --- Part 2: Elasticsearch Configuration ---
echo.
echo [3/4] Detecting and Configuring Elasticsearch...
set "ES_HOME="
echo Searching for Elasticsearch in common folders...
for %%D in (C:\ D:\ E:\ %USERPROFILE%\Downloads %USERPROFILE%\Desktop) do (
    if exist "%%D" (
        for /f "delims=" %%F in ('dir /s /b "%%Delasticsearch.bat" 2^>nul') do (
            set "POTENTIAL_HOME=%%~dpF\.."
            if exist "!POTENTIAL_HOME!\config\elasticsearch.yml" (
                set "ES_HOME=!POTENTIAL_HOME!"
                goto :ES_FOUND
            )
        )
    )
)

:ES_FOUND
if not defined ES_HOME (
    echo [!] Could not automatically find Elasticsearch.
    echo [!] Search functionality will fallback to SQLite (no fuzzy search).
    goto :SHORTCUT
)

echo Detected Elasticsearch at: !ES_HOME!
set "CONFIG_FILE=!ES_HOME!\config\elasticsearch.yml"
if exist "!CONFIG_FILE!" (
    echo Disabling Elasticsearch security features for local use...
    copy "!CONFIG_FILE!" "!CONFIG_FILE!.bak" >nul 2>&1
    powershell -Command "$c = gc '!CONFIG_FILE!'; $c = $c -replace 'xpack.security.enabled:.*', 'xpack.security.enabled: false'; $c = $c -replace 'enabled: true', 'enabled: false'; [System.IO.File]::WriteAllLines('!CONFIG_FILE!', $c, [System.Text.Encoding]::ASCII)"
)

set "ES_SERVICE_NAME=elasticsearch-service-x64"
sc query "!ES_SERVICE_NAME!" >nul 2>&1
if %errorlevel% neq 0 (
    if exist "!ES_HOME!\bin\elasticsearch-service.bat" (
        echo Installing Elasticsearch Windows service...
        call "!ES_HOME!\bin\elasticsearch-service.bat" install
    )
)
sc config "!ES_SERVICE_NAME!" start= auto >nul 2>&1
sc start "!ES_SERVICE_NAME!" >nul 2>&1

:: --- Part 3: Finalization ---
:SHORTCUT
echo.
echo [4/4] Finalizing setup...
python setup_shortcut.py

echo.
echo ==================================================
echo [SUCCESS] Setup complete! 
echo.
echo IMPORTANT: 
echo 1. If this is a new computer, please click "Settings" in the app 
echo    and re-index your folders.
echo 2. Make sure you have run 'ollama pull gemma3:4b'.
echo ==================================================
pause
