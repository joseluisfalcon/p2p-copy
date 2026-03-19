@echo off
setlocal enabledelayedexpansion

:: Configuration
set "INSTALL_DIR=%USERPROFILE%\.p2pc-secure"
set "SCRIPTS_DIR=%INSTALL_DIR%\.venv\Scripts"

echo -------------------------------------------------------
echo   p2pc-secure: Windows Installer
echo -------------------------------------------------------
echo   ____ ___   ____        ______
echo  / __ \__ \ / __ \      / ____/___  ____  __  __
echo / /_/ /_/ // /_/ /_____/ /   / __ \/ __ \/ / / /
echo / ____/ __// ____/_____/ /___/ /_/ / /_/ / /_/ /   
echo /_/   /____/_/          \____/\____/ .___/\__, /    
echo                                  /_/    /____/     

:: 1. Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [31mError: Python not found. Please install it from python.org[0m
    pause
    exit /b 1
)

:: 2. Create permanent home
echo Step 1: Preparing home in %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 3. Copy files (excluding envs)
echo Step 2: Copying source files...
xcopy /s /e /y /q . "%INSTALL_DIR%\" >nul 2>&1

:: 4. Setup Environment
echo Step 3: Setting up internal environment (this may take a minute)...
cd /d "%INSTALL_DIR%"
python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -e . >nul 2>&1

:: 5. Add to PATH automatically using PowerShell
echo Step 4: Registering p2pc-secure in your system PATH...
powershell -Command "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($oldPath -notlike '*%SCRIPTS_DIR%*') { [Environment]::SetEnvironmentVariable('Path', $oldPath + ';%SCRIPTS_DIR%', 'User') }" >nul 2>&1

echo.
echo [32m[1m✔ Installation complete![0m
echo -------------------------------------------------------
echo IMPORTANT: 
echo 1. Close this terminal and OPEN A NEW ONE to refresh the PATH.
echo 2. Then, just type: p2pc-secure
echo -------------------------------------------------------
pause
