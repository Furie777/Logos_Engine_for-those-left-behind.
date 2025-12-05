@echo off
REM ============================================================================
REM LOGOS ENGINE - Quick Setup Script for Windows
REM 
REM This script will:
REM 1. Check if Python 3 is installed
REM 2. Install networkx (required)
REM 3. Build the graph database
REM 4. Test the installation
REM
REM Usage: Double-click this file or run from Command Prompt:
REM   setup.bat
REM ============================================================================

echo ================================================================================
echo                     LOGOS ENGINE - Quick Setup
echo ================================================================================
echo.

REM Step 1: Check Python
echo Step 1: Checking for Python 3...
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python found
    set PYTHON_CMD=python
) else (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.x
    echo 3. Run installer
    echo 4. IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo.

REM Step 2: Check pip
echo Step 2: Checking for pip...
pip --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] pip found
    set PIP_CMD=pip
) else (
    echo [ERROR] pip not found
    echo pip should come with Python. Please reinstall Python.
    pause
    exit /b 1
)
echo.

REM Step 3: Install networkx
echo Step 3: Installing required dependencies...
echo Installing networkx (this may take a moment)...
%PIP_CMD% install networkx
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install networkx
    echo Please try manually: pip install networkx
    pause
    exit /b 1
)
echo [OK] networkx installed successfully
echo.

REM Step 4: Build the graph
echo Step 4: Building LOGOS graph database...
echo This will create the network graph from Bible data...
%PYTHON_CMD% logos.py build
echo.

REM Step 5: Test the installation
echo Step 5: Testing LOGOS ENGINE...
echo Looking up John 3:16...
echo.
%PYTHON_CMD% logos.py verse "John 3:16"
if %errorlevel% neq 0 (
    echo [ERROR] Test failed
    pause
    exit /b 1
)
echo.

REM Success!
echo ================================================================================
echo [SUCCESS] LOGOS ENGINE is ready!
echo ================================================================================
echo.
echo Try these commands:
echo   python logos.py help                 # Show all commands
echo   python logos.py verse "Genesis 1:1"  # Look up a verse
echo   python logos.py search "grace"       # Search for a word
echo   python logos.py strongs H430         # Hebrew/Greek study
echo   python logos.py stats                # Network statistics
echo.
echo Read START_HERE.txt for introduction
echo Read WHY.txt to understand the Gospel
echo Read docs\INSTALL.md for complete documentation
echo.
echo ================================================================================
echo "In the beginning was the Word, and the Word was with God,"
echo " and the Word was God." - John 1:1
echo ================================================================================
echo.
pause
