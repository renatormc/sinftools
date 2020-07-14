@echo off
s-mark sinf-mirror -c %1 -f "%TEMP%\sinf_mirror_input.txt" && ^
s-mirror -f "%TEMP%\sinf_mirror_input.txt"