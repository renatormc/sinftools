Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("""start ..\extracao\Relatório simplificado.html""")  
Set shl = Nothing  
WScript.Quit