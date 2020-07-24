import re
import sys
import os
import string
import re
try:
    sys.path.append(os.path.join(
        os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException


# def dropDownMenu(device,numberOfTimes):
#     for i in range(0,numberOfTimes):
#         device.press('KEYCODE_DPAD_DOWN')


class Bot:
    def __init__(self):
        self.MENU_MAIS = "Mais"
        self.EXPORTAR = 'Exportar conversa'
        self.INCLUIR_MIDIA = "INCLUIR ARQUIVOS DE MÍDIA"
        self.APP_NAME = "Extrator 0.4"
        self.SALVAR = "SALVAR"
        self.CHECK_CHAT_LIST = "STATUS"
        self.CHECK_CHAT_INSIDE = "Digite uma men"
        self.extracted = []
        self.max_wait = 10
        self.device, self.serial_no = ViewClient.connectToDeviceOrExit()
        ViewClient.sleep(2)
        self.vc = ViewClient(self.device, self.serial_no)

    def clear_extracted(self):
        self.extracted = []

    def append_extracted(self, chat):
        self.extracted.append(chat)
    

    def extract(self):
        views = self.get_new_chats_views()
        for view in views:
            print(view.getText())
            self.extract_chat(view)
            break



    def extract_chat(self, view):
        self.vc.sleep(1)
        self.assert_screen(self.CHECK_CHAT_LIST)
        view.touch()
        # self.assert_screen(self.CHECK_CHAT_INSIDE)
        self.vc.findViewWithContentDescriptionOrRaise('Mais opções').touch()
        self.find_and_touch(self.MENU_MAIS, raise_=True)
        ok = self.find_and_touch(self.EXPORTAR)
        if not ok:
            print("Opção de exportar não foi encontrada")
            return
        self.sleep(1)
        ok = self.find_and_touch(self.INCLUIR_MIDIA)
        if not ok:
            print("Contato sem mídia")
        ok = self.find_and_touch(self.APP_NAME, repeat=4)
        ok = self.find_and_touch(self.SALVAR, repeat=4)
        self.press('KEYCODE_ESCAPE')
        self.sleep(1)
        self.press('KEYCODE_ESCAPE')

    
    def press(self, key):
        self.device.press(key)
        
        
    def sleep(self, seconds):
        self.vc.sleep(seconds)
        

    def get_new_chats_views(self):
        """Analisa a tela do celular e retorna todas as views de chats que aparecem nela
        que ainda não foram extraídos"""
        views = []
        self.vc.dump(window=-1)
        text_views = self.vc.findViewsWithAttribute(
            "class", "android.widget.TextView")
        for text_view in text_views:
            if(text_view.getId() == 'com.whatsapp:id/conversations_row_contact_name'):
                contact = text_view.getText()
                if contact not in self.extracted:
                    views.append(text_view)
        return views

    def find_and_touch(self, text, exactly=True, repeat=1, raise_=False):
        for i in range(repeat):
            self.vc.dump(window=-1)
            if not exactly:
                text = re.compile(f".*{text}.*")
            try:
                self.vc.findViewWithTextOrRaise(text).touch()
                return True
            except ViewNotFoundException:
                if i <= repeat - 1:
                    if raise_:
                        raise Exception(f"View \"{text}\" não foi encontrada")
                    return False
            self.sleep(1)
           

    def assert_screen(self, text, exactly=True, wait=10):
        if not exactly:
            text = re.compile(f".*{text}.*")
        reg = re.compile(f".*{text}.*")
        time_ = 0
        while time_ < wait:
            try:
                self.vc.findViewWithTextOrRaise(text)
                return
            except ViewNotFoundException:
                time_ += 1
                self.vc.sleep(1)
        raise Exception(f"Não foi encontrada a tela {text}")
