@echo off
REM deixe o nome da imagem sem extensao na parte de criacao da imagem.
s-check-disk "\\.\PHYSICALDRIVE3 - Kingston DataTraveler 3.0 USB Device [15GB USB]" && ^
s-ftkimager \\.\PHYSICALDRIVE3 "C:\Users\renato\Downloads\teste_pen" --e01 --verify