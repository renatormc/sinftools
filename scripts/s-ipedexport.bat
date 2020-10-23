@echo off
SET PATH=%PATH%;%SINFTOOLS%\extras\iped\iped-3.17-snapshot\tools\tsk\x64
SET PYTHONPATH=%SINFTOOLS%\tools\libs && ^
"%SINFTOOLS%\extras\Python\python.exe" "%SINFTOOLS%\tools\iped_export\main.py" %*
