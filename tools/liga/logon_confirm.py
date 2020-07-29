import PySimpleGUI as sg
from helpers.user_manage import get_last_logon_time, post_connect_intent, get_connection_type
import sys

connection_type = get_connection_type()
if connection_type != "local" and not (len(sys.argv) > 1 and sys.argv[1] == 'manual'):
    sys.exit()


sg.theme('DarkAmber')  
layout = [  [sg.Text('Por gentileza informe seu nome. Deixe os demais peritos cientes de que é você que está usando o computador.')],
            [sg.Text('SEU NOME'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancelar')] ]

window = sg.Window('Informe seu nome', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break
    elif event == 'Ok' and values[0].strip():
        name = values[0].strip()
        last_logon = get_last_logon_time()
        if last_logon:
            post_connect_intent(name, last_logon)
        break
    
window.close()