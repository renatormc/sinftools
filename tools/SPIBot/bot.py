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


class Bot:
    def __init__(self):
        self.MENU_MAIS = "Mais"
        self.EXPORTAR = "Exportar conversa"
        self.INCLUIR_MIDIA = "INCLUIR ARQUIVOS DE MÍDIA"
        self.APP_NAME = "Extrator 0.4"
        self.SALVAR = "SALVAR"
        self.VOLTAR = "KEYCODE_BACK"
        self.ROLAR_N_VEZES = 5
       

    def extract(self):
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
                            vc.findViewWithTextOrRaise(self.MENU_MAIS).touch()
                            vc.dump(window=-1)
                            try:
                                vc.findViewWithTextOrRaise(self.EXPORTAR).touch()
                                vc.sleep(1)
                                vc.dump(window=-1)
                                try:
                                    vc.findViewWithTextOrRaise(self.INCLUIR_MIDIA).touch()
                                    vc.sleep(3)
                                except:
                                    print("Contato sem mídias ")
                                try:
                                    vc.dump(window=-1)
                                    vc.findViewWithTextOrRaise(self.APP_NAME).touch()
                                except:
                                    # A exportação pode ser demorada
                                    vc.sleep(15)
                                    vc.dump(window=-1)
                                    vc.findViewWithTextOrRaise(self.APP_NAME).touch()
                                    print("Exportação demorando mais que o normal ")
                                vc.sleep(1)
                                vc.dump(window=-1)
                                vc.findViewWithTextOrRaise(self.SALVAR).touch()
                                vc.sleep(2)
                                device.press(self.VOLTAR)
                                vc.sleep(1)
                                device.press(self.VOLTAR)
                            except Exception as e:
                                print("Opção de enviar por e-mail não encontrada! ")
                                device.press(self.VOLTAR)
                                vc.sleep(1)
                                device.press(self.VOLTAR)
                                print(e)
                        except Exception as e:
                            print_safe(f"View não encontrada: {contato}")
                            print(e)
            if not listaAtualizada:
                repeticoes = repeticoes + 1
            for i in range(self.ROLAR_N_VEZES):
                device.press('KEYCODE_DPAD_DOWN')
        
        for contato in listContatos:
            print(contato)


