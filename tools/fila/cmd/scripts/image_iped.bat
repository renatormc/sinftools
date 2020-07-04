@echo off
REM deixe o nome da imagem sem extensao na parte de criacao da imagem
s-ftkimager \\.\PHYSICALDRIVE3 "D:\path\to\image\hdd" --e01 --verify && ^
iped -profile fastmode -d "D:\path\to\image\hdd.E01" -o "D:\path\to\results\folder" --nogui --portable