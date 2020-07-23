@echo off
"%SINFTOOLS%\extras\Python\python.exe" -m pip freeze > "%SINFTOOLS%\requirements_windows.txt" && type "%SINFTOOLS%\requirements_windows.txt"