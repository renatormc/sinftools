Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("soffice .\data\data.ods --accept=socket,host=localhost,port=2002;urp")  
Set shl = Nothing  
WScript.Quit