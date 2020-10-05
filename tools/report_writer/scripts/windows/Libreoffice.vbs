Dim shl  
Set shl = CreateObject("Wscript.Shell")  
Call shl.Run("soffice socket,host=0.0.0.0,port=2002;urp;StarOffice.Service")  
Set shl = Nothing  
WScript.Quit