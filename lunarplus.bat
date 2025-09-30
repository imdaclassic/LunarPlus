@echo off
title LunarPlus Bootloader
echo Getting bootloader...

:: Set URL and output file
set "URL=https://raw.githubusercontent.com/imdaclassic/LunarPlus-Plugin/main/src/bootloader.py"
set "BOOT=bootloader.py"

:: Use PowerShell to download the file
powershell -Command ^
  "try {Invoke-WebRequest '%URL%' -OutFile '%BOOT%'} catch {Write-Host 'Oops! An error occurred while trying to get bootloader:'; Write-Host '-----'; Write-Host '<ERRORHERE>'; pause; exit 1}"

if not exist "%BOOT%" (
    echo Bootloader not found after download attempt.
    pause
    exit /b 1
)

echo Bootloader acquired, starting bootloader...
python "%BOOT%"
if errorlevel 1 (
    echo Oops! An error occurred while executing bootloader:
    echo -----
    echo <ERRORHERE>
    pause
    exit /b 1
)

echo Bootloader finished successfully.
pause
