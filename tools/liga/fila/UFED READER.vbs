Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("C:\Windows\System32\cmd.exe /c set PYTHONPATH=""%SINFTOOLS%\tools\libs"" && ""%SINFTOOLS%\extras\Python\pythonw.exe"" ""%SINFTOOLS%\tools\liga\fila_main.py"" standalone")  
Set shl = Nothing  
WScript.Quit