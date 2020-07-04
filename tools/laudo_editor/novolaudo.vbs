Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c " & "C:\ScriptsUFED\Miniconda3\pythonw novo_laudo\novo_laudo.py"
oShell.Run strArgs, 0, false