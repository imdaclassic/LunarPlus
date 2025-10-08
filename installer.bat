@echo off
setlocal

title LunarPlus Manager

echo Checking for local LunarPlus installation...
echo.

:: Check for permissions
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

:: If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

IF EXIST "lib\lunarplus" (
    echo Found local LunarPlus library.
    echo Executing local version...
    echo ----------------------------------------
    python "lib\lunarplus"
) ELSE (
    echo Local library not found.
    echo Preparing to fetch and run the bootloader...
    echo ----------------------------------------

    echo Installing/updating Python requirements...
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "Invoke-WebRequest -Uri 'https://github.com/imdaclassic/LunarPlus/raw/refs/heads/main/src/req.txt' -OutFile '%temp%\lp_requirements.txt'"

    IF %ERRORLEVEL% NEQ 0 (
        echo [FATAL] Could not download requirements file.
        pause
        exit /b %ERRORLEVEL%
    )

    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install -r "%temp%\lp_requirements.txt"
    IF %ERRORLEVEL% NEQ 0 (
        echo [FATAL] Failed to install Python requirements.
        pause
        exit /b %ERRORLEVEL%
    )

    echo.
    echo Requirements installed successfully.
    echo Launching bootloader...
    echo ----------------------------------------

    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "(Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/imdaclassic/LunarPlus/main/src/bootloader.py').Content | python -"

    IF %ERRORLEVEL% NEQ 0 (
        echo.
        echo [FATAL] An error occurred while trying to fetch or run the bootloader.
        pause
        exit /b %ERRORLEVEL%
    )
)

echo.
echo ----------------------------------------
echo Script execution finished.

IF /I NOT "%~n0"=="LP-Manager" (
    echo.
    echo Renaming this launcher to LP-Manager.bat for future use...
    ren "%~f0" "LP-Manager.bat"
)

endlocal
