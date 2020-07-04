@echo off
s-py -m pipenv install --python "%SINFTOOLS%\extras\Python\python.exe && s-py -m pipenv --venv > tmpFile && SET /p myvar= < tmpFile && s-py "%~dp0\install.py" "%myvar%"
