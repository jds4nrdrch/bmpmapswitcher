@echo off
setlocal enabledelayedexpansion

REM Define variables
set REPO_URL=https://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@github.com/jds4nrdrch/bmpmapswitcher.git
set TEMP_DIR=%TEMP%\repo_temp
set TARGET_DIR=%CD%
set FILES_TO_CHECK=configuration.py functions.py main.py settings.toml requirements.txt
set DEFAULT_SETTINGS_FILE=default_settings.toml
set SETTINGS_FILE=settings.toml
set MAPS_FILE=maps.json

REM Start of the update process
echo 0

REM Clone the repository to a temporary folder
echo Cloning repository to %TEMP_DIR%...
if exist %TEMP_DIR% rd /s /q %TEMP_DIR%
git clone %REPO_URL% %TEMP_DIR%
if errorlevel 1 (
    echo Error cloning repository.
    echo 100
    exit /b 1
)
echo 30

REM Change to the temporary repository directory
cd /d %TEMP_DIR%

REM Check and update files
echo Checking and updating files...
for %%f in (%FILES_TO_CHECK%) do (
    if "%%f" == "%SETTINGS_FILE%" (
        if not exist "%TARGET_DIR%\%SETTINGS_FILE%" (
            echo Copying %DEFAULT_SETTINGS_FILE% to %SETTINGS_FILE%...
            copy /y %DEFAULT_SETTINGS_FILE% "%TARGET_DIR%\%SETTINGS_FILE%"
        )
    ) else (
        echo Replacing %%f...
        copy /y %%f "%TARGET_DIR%\%%f"
    )
)
echo 60

REM Remove maps.json if it exists
if exist "%TARGET_DIR%\%MAPS_FILE%" (
    echo Removing %MAPS_FILE%...
    del /q "%TARGET_DIR%\%MAPS_FILE%"
)
echo 80

REM Install or upgrade pip packages
if exist "%TARGET_DIR%\requirements.txt" (
    echo Installing or upgrading pip packages from requirements.txt...
    pip install --upgrade -r "%TARGET_DIR%\requirements.txt"
)
echo 90

REM Clean up
echo Cleaning up...
rd /s /q %TEMP_DIR%

echo 100
echo Update complete.
exit /b 0