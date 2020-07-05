@echo off
cd /d "%SINFTOOLS%" && ^
git pull origin master && s-pip install -r requirements.txt