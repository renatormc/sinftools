@echo off
"%SINFTOOLS%\extras\Python\python.exe" -m pip freeze > "%SINFTOOLS%\requirements.txt" && type "%SINFTOOLS%\requirements.txt"