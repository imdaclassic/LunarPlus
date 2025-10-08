@echo off
setlocal

title LunarPlus Manager

echo Checking for local LunarPlus installation...
echo.

:: Check if the local library file exists in a 'lib' subdirectory
IF EXIST "lib\lunarplus" (
    echo Found local LunarPlus library.
    echo Executing local version...
    echo ----------------------------------------
    REM Assumes 'python' is in the system's PATH environment variable.
    python "lib\lunarplus"
) ELSE (
    echo Local library not found.
    echo Fetching the latest bootloader from GitHub...
    echo ----------------------------------------
    
    REM Use PowerShell to download the script's raw text and pipe it to the Python interpreter.
    REM This method runs the script without saving it to the disk.
    REM -NoProfile: Speeds up PowerShell startup.
    REM -ExecutionPolicy Bypass: Ensures the command runs regardless of the system's execution policy.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "try { (Invoke-RestMethod -Uri 'https://raw.githubusercontent.com/imdaclassic/LunarPlus/main/src/bootloader.py') | python - } catch { Write-Host '[ERROR] Failed to fetch script. Check internet connection.'; exit 1 }"
    
    REM Check if the PowerShell command failed (e.g., no internet, 404 error).
    IF %ERRORLEVEL% NEQ 0 (
        echo.
        echo [FATAL] An error occurred while trying to fetch or run the bootloader.
        echo Please ensure you have a stable internet connection and that Python is
        echo correctly installed and added to your system's PATH.
        pause
        exit /b %ERRORLEVEL%
    )
)

echo.
echo ----------------------------------------
echo Script execution finished.

:: After execution, check the current filename. If it's not "LP-Manager.bat",
:: rename it. This makes it a one-time operation.
:: %~n0 is the filename of the current script without the extension.
:: The /I switch makes the string comparison case-insensitive.
IF /I NOT "%~n0"=="LP-Manager" (
    echo.
    echo Renaming this launcher to LP-Manager.bat for future use...
    REM %~f0 is the full path to the current batch file.
    ren "%~f0" "LP-Manager.bat"
)

endlocal

:: Optional: If your Python script exits immediately, the console window will
:: close. You can uncomment the line below to keep it open until a key is pressed.
:: pause
