Attribute VB_Name = "M�dulo11"
Public Sub escrever()
    Dim comando As String
    comando = "cmd /c cd /d """ & ActiveDocument.Path & """ && s-wh write"
    Call Shell(comando, vbNormalFocus)
End Sub

Public Sub escanearFotos()
    Dim comando As String
    comando = "cmd /c cd /d """ & ActiveDocument.Path & """ && s-wh pics"
    Call Shell(comando, vbNormalFocus)
End Sub

