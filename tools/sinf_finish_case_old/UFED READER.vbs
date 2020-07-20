Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("""..\extracao\UFEDReader.exe""")  
Set shl = Nothing  
WScript.Quit