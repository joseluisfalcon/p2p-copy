@echo off
setlocal enabledelayedexpansion

:: ASCII Banner
echo -------------------------------------------------------
echo    ____ ___   ____        ______                      
echo   / __ \\__ \\ / __ \\      / ____/___  ____  __  __ 
echo  / /_/ /_/ // /_/ /_____/ /   / __ \\/ __ \\/ / / / 
echo / ____/ __// ____/_____/ /___/ /_/ / /_/ / /_/ /  
echo /_/   /____/_/          \\____/\\____/ .___/\\__, /   
echo                                  /_/    /____/    
echo    Secure P2P-style file transfer setup (Windows)
echo -------------------------------------------------------

echo.
echo Step 1: Checking system requirements...

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install it from python.org
    exit /b 1
)

:: 2. Create virtual environment
if not exist ".venv" (
    echo Creating virtual environment in .venv/...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        exit /b 1
    )
)

:: 3. Install/Update
echo Step 2: Installing dependencies and p2p-copy...
.venv\\Scripts\\python.exe -m pip install --upgrade pip >nul 2>&1
.venv\\Scripts\\pip.exe install -e . >nul 2>&1

echo.
echo [OK] Installation completed successfully!
echo -------------------------------------------------------
echo To use the program, you can:
echo   1. Activate: .venv\\Scripts\\activate
echo   2. Direct:   .venv\\Scripts\\p2p-copy.exe
echo -------------------------------------------------------
pause
