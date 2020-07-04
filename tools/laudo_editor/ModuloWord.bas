Attribute VB_Name = "M�dulo11"

Public Sub word_helper()
    Dim comando As String
    comando = Environ("SINFTOOLS") & "\Miniconda3\pythonw.exe" & " " & Environ("SINFTOOLS") & "\tools\laudo_editor\main\main.pyw " & ActiveDocument.Path
    Call Shell(comando, vbNormalFocus)
End Sub

Public Sub enviar_revisao()
    Dim comando As String
    comando = Environ("SINFTOOLS") & "\Miniconda3\python.exe" & " " & Environ("SINFTOOLS") & "\tools\laudo_editor\enviar_revisao.py " & ActiveDocument.Path & " " & ActiveDocument.Name
    Call Shell(comando, vbNormalFocus)
End Sub


Public Sub openCaseForlder()
    Dim comando As String
    comando = "explorer " & ActiveDocument.Path
    Call Shell(comando, vbNormalFocus)
End Sub

Public Sub laudoRapido()
    Dim comando As String
    comando = Environ("SINFTOOLS") & "\Miniconda3\pythonw.exe" & " " & Environ("SINFTOOLS") & "\tools\laudo_editor" & "\laudo_rapido2\main.py" & " " & ActiveDocument.Path
    Call Shell(comando, vbNormalFocus)
End Sub


