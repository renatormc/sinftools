from views.ui_adicionar import Ui_adicionar
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from model import *
import win32com.client as win32

# word = win32.gencache.EnsureDispatch('Word.Application')
word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument

class adicionar(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_adicionar()
        self.ui.setupUi(self)
        self.conenctions()
    
    def conenctions(self):
        self.ui.btn_ok.clicked.connect(self.okClick)

    def okClick(self):
        msg = QMessageBox()
        palavras_chave = self.ui.edt_palavras_chave.displayText()
        if len(palavras_chave) != 0:
            frase = Frase()
            frase.texto = self.ui.edt_palavras_chave.displayText()
            print(self.ui.txt_texto.toPlainText())
            frase.texto = self.ui.txt_texto.toPlainText()
            frase.palavras_chave = palavras_chave
            session.add(frase)
            session.commit()
            msg.setWindowTitle("Sucesso")
            msg.setText("Registro incluido!")
            msg.exec()
            self.close()
        else:
            msg.setWindowTitle("Erro")
            msg.setText("Nenhuma palavra-chave foi digitada.")
            msg.exec()
        
    
    def showEvent(self, event):
        self.ui.txt_texto.setPlainText(word.Selection.Text)

if __name__ == "__main__":
    print(word.Selection.Text)
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = adicionar()
    w.show()
    sys.exit(app.exec_())

