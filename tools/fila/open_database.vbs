Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("s-dbb ""%SINFTOOLS%\var\databases\fila.db""")  
Set shl = Nothing  
WScript.Quit