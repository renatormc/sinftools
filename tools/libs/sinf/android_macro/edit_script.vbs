Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "s-idlex macro.py"
oShell.Run strArgs, 0, false