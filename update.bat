@echo off
setlocal enabledelayedexpansion

REM Determine script directory
set "SCRIPT_DIR=%~dp0"
REM Define variables
set REPO_URL=https://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@github.com/jds4nrdrch/bmpmapswitcher.git
set TEMP_DIR=%TEMP%\repo_temp
set TARGET_DIR=%SCRIPT_DIR%
set FILES_TO_CHECK=configuration.py functions.py main.py settings.toml requirements.txt update.bat
set DEFAULT_SETTINGS_FILE=default_settings.toml
set SETTINGS_FILE=settings.toml
set MAPS_FILE=maps.json

REM Start of the update process
echo 0
echo 10
echo 20
REM Remove maps.json if it exists
if exist "%TARGET_DIR%\%MAPS_FILE%" (
    echo Removing %MAPS_FILE%...
    echo 30
    del /q "%TARGET_DIR%\%MAPS_FILE%"
    echo 40
)
echo 50

REM Clone the repository to a temporary folder
echo Cloning repository to %TEMP_DIR%...
if exist "%TEMP_DIR%" rd /s /q "%TEMP_DIR%"
echo 100
git clone %REPO_URL% "%TEMP_DIR%"
echo 150

if errorlevel 1 (
    echo Error cloning repository.
    exit /b 1
)

echo 200

REM Change to the temporary repository directory
cd /d "%TEMP_DIR%"
echo 250

REM Check and update files
echo Checking and updating files...
for %%f in (%FILES_TO_CHECK%) do (
    if "%%f" == "%SETTINGS_FILE%" (
        echo 300
        if not exist "%TARGET_DIR%\%SETTINGS_FILE%" (
            echo Copying %DEFAULT_SETTINGS_FILE% to %SETTINGS_FILE%...
            copy /y "%DEFAULT_SETTINGS_FILE%" "%TARGET_DIR%\%SETTINGS_FILE%"
            echo 350
        ) else (
            echo Updating %SETTINGS_FILE% from %DEFAULT_SETTINGS_FILE%...
            setlocal enabledelayedexpansion
            for /f "tokens=1,* delims==" %%i in ('type "%DEFAULT_SETTINGS_FILE%"') do (
                set first_part=%%i
                set match_found=false
                for /f "tokens=1,* delims==" %%j in ('type "%TARGET_DIR%\%SETTINGS_FILE%" ^| findstr /b /c:"!first_part!"') do (
                    if "!first_part!=%%k" == "%%j" (
                        set match_found=true
                        rem Check if entire line is different
                        if "!first_part!=%%j" neq "!first_part!=%%k" (
                            echo Updating line: %%i=%%j
                            echo %%i=%%j>>"%TARGET_DIR%\%SETTINGS_FILE%"
                        )
                    )
                )
                if "!match_found!" == "false" (
                    echo Adding line: %%i=%%j
                    echo %%i=%%j>>"%TARGET_DIR%\%SETTINGS_FILE%"
                )
            )
            endlocal
            echo 350
        )
    ) else (
        echo Replacing %%f...
        copy /y "%%f" "%TARGET_DIR%\%%f"
        echo 350
    )
)
echo 450

echo 660

REM Install or upgrade pip packages
if exist "%TARGET_DIR%\requirements.txt" (
    echo Installing or upgrading pip packages from requirements.txt...
    echo 700
    pip install --upgrade -r "%TARGET_DIR%\requirements.txt"
    echo 800
)
echo 850

REM Clean up
echo Cleaning up...
rd /s /q "%TEMP_DIR%"
echo 900

echo Update complete.
echo 1000

exit /b 0
