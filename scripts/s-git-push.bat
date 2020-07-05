@echo off
cd /d "%SINFTOOLS%" && ^
s-freeze && git add . && git commit -m %1 && git push origin master