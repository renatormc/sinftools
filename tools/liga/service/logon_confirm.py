import PySimpleGUI as sg
from sinf.servers import user_manage
import sys

connection_type = user_manage.get_connection_type()
if connection_type != "local" and not (len(sys.argv) > 1 and sys.argv[1] == 'test'):
    sys.exit()


sg.theme('DarkAmber')  
layout = [  [sg.Text('Por gentileza informe seu nome para ficar registrado quem é que está usando o computador \npara que quando alguém for tentar se conectar usando s-ts lhe seja informado \nque é você que está usando a máquina.')],
            [sg.Text('SEU NOME'), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancelar')] ]

window = sg.Window('Informe seu nome', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break
    elif event == 'Ok' and values[0].strip():
        name = values[0].strip()
        last_logon = user_manage.get_last_logon_time()
        if last_logon:
            user_manage.post_connect_intent(name, last_logon)
        break
    
window.close()