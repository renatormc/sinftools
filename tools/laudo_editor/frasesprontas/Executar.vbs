Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c pythonw MainWindow.py"
oShell.Run strArgs, 0, false