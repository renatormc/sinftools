import re
import sys
import os
import string
from uteis.idlex import print_safe
try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass
from com.dtmilano.android.viewclient import ViewClient

### DEFINIÇÔES ----------------------------------------------
MENU_MAIS = "Mais"
EXPORTAR = "Exportar conversa"
INCLUIR_MIDIA = "INCLUIR ARQUIVOS DE MÍDIA"
APP_NAME = "Extrator 0.4"
SALVAR = "SALVAR"

### ------------------------------------------------------


def dropDownMenu(device,numberOfTimes):
    for i in range(0,numberOfTimes):
        device.press('KEYCODE_DPAD_DOWN')

device, serialno = ViewClient.connectToDeviceOrExit()
ViewClient.sleep(2)
vc = ViewClient(device, serialno)

listContatos = []
repeticoes = 0

while repeticoes < 10:
    vc.dump(window=-1)
    textViews = vc.findViewsWithAttribute("class", "android.widget.TextView")
    listaAtualizada = False
    for texView in textViews:
        if(texView.getId() == 'com.whatsapp:id/conversations_row_contact_name'):
            contato = texView.getText()
            if contato not in listContatos:
                listContatos.append(texView.getText())
                print_safe(f"Exportando dados do contato: {contato}")
                listaAtualizada = True
                try:
                    vc.sleep(1)
                    texView.touch()
                    vc.sleep(1)
                    vc.dump(window=-1)
                    vc.findViewWithContentDescriptionOrRaise(u'''Mais opções''').touch()
                    vc.dump(window=-1)
                    vc.findViewWithTextOrRaise(MENU_MAIS).touch()
                    vc.dump(window=-1)
                    try:
                        vc.findViewWithTextOrRaise(EXPORTAR).touch()
                        vc.sleep(1)
                        vc.dump(window=-1)
                        try:
                            vc.findViewWithTextOrRaise(INCLUIR_MIDIA).touch()
                            vc.sleep(3)
                        except:
                            print("Contato sem mídias ")
                        try:
                            vc.dump(window=-1)
                            vc.findViewWithTextOrRaise(APP_NAME).touch()
                        except:
                            # A exportação pode ser demorada
                            vc.sleep(15)
                            vc.dump(window=-1)
                            vc.findViewWithTextOrRaise(APP_NAME).touch()
                            print("Exportação demorando mais que o normal ")
                        vc.sleep(1)
                        vc.dump(window=-1)
                        vc.findViewWithTextOrRaise(SALVAR).touch()
                        vc.sleep(2)
                        #device.press('KEYCODE_ESCAPE')
                        device.press('KEYCODE_BACK')
                        vc.sleep(1)
                        #device.press('KEYCODE_ESCAPE')
                        device.press('KEYCODE_BACK')
                    except Exception as e:
                        print("Opção de enviar por e-mail não encontrada! ")
                        #device.press('KEYCODE_ESCAPE')
                        device.press('KEYCODE_BACK')
                        vc.sleep(1)
                        #device.press('KEYCODE_ESCAPE')
                        device.press('KEYCODE_BACK')
                        print(e)
                except Exception as e:
                    print_safe(f"View não encontrada: {contato}")
                    print(e)
    if not listaAtualizada:
        repeticoes = repeticoes + 1
    dropDownMenu(device,5)

for contato in listContatos:
    print (contato.encode('utf-8'))


