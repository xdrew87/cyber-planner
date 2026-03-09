@echo off
REM Build Script for Cyber Planner EXE
REM This script creates a standalone executable using PyInstaller

echo ========================================
echo   CYBER PLANNER - EXE BUILD SCRIPT
echo ========================================
echo.

REM Check if PyInstaller is installed
python3 -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    python3 -m pip install pyinstaller -q
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully!
    echo.
)

REM Build the executable
echo Building executable...
echo.

REM Clean old build first
if exist dist rmdir /s /q dist
if exist Cyber*.spec del /q Cyber*.spec

python3 -m PyInstaller ^
    --onefile ^
    --windowed ^
    --icon=cyber_planner2.ico ^
    --name="Cyber Planner" ^
    --distpath=dist ^
    --workpath=build ^
    --specpath=. ^
    --add-data "backgrounds;backgrounds" ^
    --add-data "cyber_planner2.ico;." ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD SUCCESSFUL!
echo ========================================
echo.
echo Your executable is ready at:
echo   dist\Cyber Planner.exe
echo.
echo You can now:
echo   1. Run the EXE directly from the dist folder
echo   2. Copy it to other computers (Windows 10+)
echo   3. Create a shortcut to place on your desktop
echo.
pause
