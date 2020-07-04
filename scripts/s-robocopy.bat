@echo off
robocopy %1 %2  /mir /copyall /eta /R:10 /W:3 /MT:10
if %ERRORLEVEL% EQU 8 EXIT /B 1 ELSE EXIT /B 0