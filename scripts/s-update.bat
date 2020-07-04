@echo off
set PYTHONPATH=%SINFTOOLS%\tools\libs && ^
"%SINFTOOLS%\extras\Python\python.exe" "%SINFTOOLS%\tools\updater\gen_update_file.py" %*