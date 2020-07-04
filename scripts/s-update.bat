@echo off
copy "%SINFTOOLS%\tools\updater\dist\update_cmd.exe" "%TEMP%\update_cmd.exe" > NUL && ^
"%TEMP%\update_cmd.exe" update %*