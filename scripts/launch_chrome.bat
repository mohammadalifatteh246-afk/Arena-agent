@echo off
setlocal

set CHROME_PATH=""

if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
)

if %CHROME_PATH%=="" (
    echo [ERROR] Google Chrome not found in standard paths.
    pause
    exit /b 1
)

echo [INFO] Launching Chrome with Remote Debugging on port 9222...
echo [INFO] Profile stored in D:\Arena-agent\user_data\chrome_profile
echo [INFO] Opening https://arena.ai/direct

start "" %CHROME_PATH% --remote-debugging-port=9222 --user-data-dir="D:\Arena-agent\user_data\chrome_profile" https://arena.ai/direct
exit /b 0
