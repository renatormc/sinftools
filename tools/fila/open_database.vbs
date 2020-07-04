Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("s-dbb ""%SINFTOOLS%\var\fila\database.db""")  
Set shl = Nothing  
WScript.Quit