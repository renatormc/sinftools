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
from pathlib import Path
from database import *


class Bot:
    def __init__(self):
        self.MENU_MAIS = "Mais"
        self.EXPORTAR = "Exportar conversa"
        self.INCLUIR_MIDIA = "INCLUIR ARQUIVOS DE MÍDIA"
        self.APP_NAME = "Extrator 0.4"
        self.SALVAR = "SALVAR"
        self.VOLTAR = "KEYCODE_BACK"
        self.ROLAR_N_VEZES = 5
        self.parte_ultimo_chat = "#$dfge&&¨qq"
        self.tentar_novamente_chats_com_erros = False
        self.verbose = False


    
    def extract(self):
        init_db()
        device, serialno = ViewClient.connectToDeviceOrExit()
        ViewClient.sleep(2)
        vc = ViewClient(device, serialno)

        # path = Path(".") / "extracted.txt"
        # try:
        #     listContatos = path.read_text(encoding="utf-8").split("\n")
        # except FileNotFoundError:
        #     listContatos = []
       
        repeticoes = 0
        finalizar = False
        while repeticoes < 100:
            vc.dump(window=-1)
            textViews = vc.findViewsWithAttribute("class", "android.widget.TextView")
            listaAtualizada = False
            if self.verbose:
                print_safe(f"{len(textViews)} views encontradas de todos os tipos")
            for texView in textViews:
                if(texView.getId() == 'com.whatsapp:id/conversations_row_contact_name'):
                    contato = texView.getText()
                    get_or_new(contato)
                    if self.verbose:
                        print_safe(f"Encontrada view de chat com texto \"{contato}\"")
                    if has_been_extracted(contato) or (has_been_tried(contato) and not self.tentar_novamente_chats_com_erros):
                        if self.parte_ultimo_chat in contato:
                            print("Ultimo chat encontrado. Finalizando.")
                            finalizar = True
                            break
                        else:
                            if self.verbose:
                                print_safe(f"Pulando contato \"{contato}\" porque já consta como já extraido anteriormente")
                            continue
                    register_start_extraction(contato)
                    
                    print_safe(f"Exportando dados do contato: {contato}")
                    listaAtualizada = True
                    try:
                        vc.sleep(1)
                        texView.touch()
                        vc.sleep(1)
                        vc.dump(window=-1)
                        if self.verbose:
                            print_safe(f"Agora vou clicar em \"Mais opções\"")
                        vc.findViewWithContentDescriptionOrRaise(u'''Mais opções''').touch()
                        vc.dump(window=-1)
                        vc.findViewWithTextOrRaise(self.MENU_MAIS).touch()
                        vc.dump(window=-1)
                        try:
                            if self.verbose:
                                    print_safe(f"Agora vou clicar em \"{self.EXPORTAR}\"")
                            vc.findViewWithTextOrRaise(self.EXPORTAR).touch()
                            vc.sleep(1)
                            vc.dump(window=-1)
                            try:
                                if self.verbose:
                                    print_safe(f"Agora vou clicar em \"{self.INCLUIR_MIDIA}\"")
                                vc.findViewWithTextOrRaise(self.INCLUIR_MIDIA).touch()
                                vc.sleep(3)
                            except:
                                print("Contato sem mídias ")
                            try:
                                vc.dump(window=-1)
                                if self.verbose:
                                    print_safe(f"Agora vou clicar em \"{self.APP_NAME}\"")
                                vc.findViewWithTextOrRaise(self.APP_NAME).touch()
                            except:
                                # A exportação pode ser demorada
                                vc.sleep(15)
                                vc.dump(window=-1)
                                if self.verbose:
                                    print_safe(f"Agora vou clicar em \"{self.APP_NAME}\"")
                                vc.findViewWithTextOrRaise(self.APP_NAME).touch()
                                print("Exportação demorando mais que o normal ")
                            vc.sleep(1)
                            vc.dump(window=-1)
                            if self.verbose:
                                print_safe(f"Agora vou clicar em \"{self.SALVAR}\"")
                            vc.findViewWithTextOrRaise(self.SALVAR).touch()
                            vc.sleep(2)
                            if self.verbose:
                                print_safe(f"Agora vou clicar em \"{self.VOLTAR}\"")
                            device.press(self.VOLTAR)
                            vc.sleep(1)
                            if self.verbose:
                                print_safe(f"Agora vou clicar em \"{self.VOLTAR}\"")
                            device.press(self.VOLTAR)
                        except Exception as e:
                            print("Opção de enviar por e-mail não encontrada! ")
                            if self.verbose:
                                print_safe(f"Agora vou clicar em \"{self.VOLTAR}\"")
                            device.press(self.VOLTAR)
                            vc.sleep(1)
                            if self.verbose:
                                print_safe(f"Agora vou clicar em \"{self.VOLTAR}\"")
                            device.press(self.VOLTAR)
                            print(e)
                        register_finish_extraction(contato)
                    except Exception as e:
                        print_safe(f"View não encontrada: {contato}")
                        print(e)
                elif self.verbose:
                    print_safe(f"Encontrada uma view que não é de chat com id \"{texView.getId()}\"")
            if not listaAtualizada:
                repeticoes = repeticoes + 1
            for i in range(self.ROLAR_N_VEZES):
                if self.verbose:
                    print_safe(f"Agora vou clicar em \"KEYCODE_DPAD_DOWN\"")
                device.press('KEYCODE_DPAD_DOWN')
            if finalizar:
                break

        chats = get_not_extracted()
        if chats:
            print("\nNÃO FOI POSSÍVEL EXTRAÍR OS SEGUINTES CHATS:")
            for i, chat in enumerate(chats):
                print(f"{i} - {chat.name}")
       



