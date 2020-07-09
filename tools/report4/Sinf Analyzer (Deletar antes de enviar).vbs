Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("""%SINFTOOLS%\extras\Python\pythonw.exe"" ""%SINFTOOLS%\tools\report4\reader\gui_server.py""")  
Set shl = Nothing  
WScript.Quit