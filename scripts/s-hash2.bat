@echo off
(set PYTHONPATH=%SINFTOOLS%\tools\libs && "%SINFTOOLS%\extras\Python\python.exe" "%SINFTOOLS%\tools\sinf_finish_case2\main.py" %*) || pause