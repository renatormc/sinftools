Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("soffice .\data\laudo.odt --accept=socket,host=localhost,port=2002;urp")  
Set shl = Nothing  
WScript.Quit