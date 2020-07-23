# -*- coding: utf-8 -*-
#! /usr/bin/env python
'''

  ___________________.___                                       
 /   _____/\______   \   |                                      
 \_____  \  |     ___/   |                                      
 /        \ |    |   |   |                                      
/_______  / |____|   |___|                                      
        \/                                                      

'''


import re
import sys
import os
import string

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient


def dropDownMenu(device,numberOfTimes):
    for i in range(0,numberOfTimes):
        device.press('KEYCODE_DPAD_DOWN')

device, serialno = ViewClient.connectToDeviceOrExit()

ViewClient.sleep(2)

vc = ViewClient(device, serialno)



listContatos = ['Willian']
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
                print(texView.getText())
                # print(f"")
                print (f"Exportando dados do contato: {contato}")
                listaAtualizada = True
                try:
                    vc.sleep(1)
                    texView.touch()
                    vc.sleep(1)
                    vc.dump(window=-1)
                    vc.findViewWithContentDescriptionOrRaise(u'''Mais opções''').touch()
                    vc.dump(window=-1)
                    vc.findViewWithTextOrRaise(u'Mais').touch()
                    vc.dump(window=-1)
                    try:
                        vc.findViewWithTextOrRaise(u'Enviar por email').touch()
                        vc.sleep(1)
                        vc.dump(window=-1)
                        try:
                            vc.findViewWithTextOrRaise(u'ANEXAR MÍDIA').touch()
                            vc.sleep(3)
                        except:
                            print ("Contato sem mídias ")
                        try:
                            vc.dump(window=-1)
                            vc.findViewWithTextOrRaise(u'Email Bkp Para Arquivo').touch()
                        except:
                            # A exportação pode ser demorada
                            vc.sleep(15)
                            vc.dump(window=-1)
                            vc.findViewWithTextOrRaise(u'Email Bkp Para Arquivo').touch()
                            print ("Exportação demorando mais que o normal ")
                        vc.sleep(1)
                        vc.dump(window=-1)
                        vc.findViewWithTextOrRaise(u'SELECIONAR').touch()
                        vc.sleep(2)
                        device.press('KEYCODE_ESCAPE')
                        vc.sleep(1)
                        device.press('KEYCODE_ESCAPE')
                    except Exception as e:
                        print ("Opção de enviar por e-mail não encontrada! ")
                        device.press('KEYCODE_ESCAPE')
                        vc.sleep(1)
                        device.press('KEYCODE_ESCAPE')
                        print (e)
                except Exception as e:
                    print ("View não encontrada: ") + (contato.encode('utf-8'))
                    print (e)
    if not listaAtualizada:
        repeticoes = repeticoes + 1
    dropDownMenu(device,5)

for contato in listContatos:
    print (contato.encode('utf-8'))
    
