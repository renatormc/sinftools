## [inicio]
linha_inicial = 2
import win32com.client as win32
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.ActiveWorkbook
ws = wb.ActiveSheet
## SMS
colunas =[
'#',
'Parte',
'Hora'
'Pasta',
'Status',
'Mensagem',
'Excluido']

## Contatos
colunas =[
'#',
'Nome',
'Entradas'
'Anotações',
'Origem',
'Excluido',
'Link #1']

## Bate-papo
colunas =[
'Identificador',
'Hora de início: Hora',
'Última atividade: Hora'
'Participantes',
'Origem',
'Excluído - Bate-papo',
'De',
'Corpo',
'Marcação de tempo: Hora',
'Anexo #1',
'Anexo #1 - Detalhes']




## [ocultar colunas que nao estão na lista]
lastcol = ws.Cells(linha_inicial, ws.Columns.Count).End(win32.constants.xlToLeft).Column
for col in range(lastcol):
    if not ws.Cells(linha_inicial,col+1).Value in colunas:
        ws.Columns(col+1).Hidden = True

## [Deletar colunas que nao estão na lista]
col =1
for i in range(lastcol):
    if not ws.Cells(linha_inicial,col).Value in colunas:
        ws.Columns(col).Delete()
    else:
        col+=1

## [Criar dicionario de indices]
indice = {}
lastcol = ws.Cells(linha_inicial, ws.Columns.Count).End(win32.constants.xlToLeft).Column
for col in range(lastcol):
    indice[ws.Cells(linha_inicial,col+1).Value] = col +1

## [Copiar anexos para coluna corpo]
lastrow = ws.Cells(ws.Rows.Count, 1).End(win32.constants.xlUp).Row
for row in range(lastrow):
    if ((ws.Cells(row+1,indice['Anexo #1']).Value != "") and (ws.Cells(row+1,indice['Corpo']).Value == "")):
        ws.Cells(row+1,indice['Anexo #1']).Copy(ws.Cells(row+1,indice['Corpo']))
        ws.Cells(row+1,indice['Corpo']).Font.ColorIndex = 3
        ws.Cells(row+1,indice['Corpo']).Font.Bold = True

## [Esconder coluna anexos]
ws.Columns(indice['Anexo #1']).Hidden = True

## [Ajustar alturas das linhas]
excel.ScreenUpdating = False
altura_maxima = 80
lastrow = ws.Cells(ws.Rows.Count, 1).End(win32.constants.xlUp).Row
for row in range(lastrow):
    if (ws.Rows(row+1).Height > altura_maxima):
        ws.Rows(row+1).RowHeight = altura_maxima
excel.ScreenUpdating = True

