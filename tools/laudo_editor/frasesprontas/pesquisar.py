from views.ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from model import *
import win32com.client as win32

word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument


class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()

    def connections(self):
        self.ui.btnPesquisar.clicked.connect(self.pesquisar)
        self.ui.lswResultados.itemDoubleClicked.connect(self.itemClicked)
        self.ui.edtPesquisar.returnPressed.connect(self.pesquisar)
        self.ui.btnDeletar.clicked.connect(self.deletar)

    def deletar(self):
        reply = QMessageBox.question(self, 'Mensagem', 
                     "Tem certeza que deseja deletar esta frase?", QMessageBox.Yes, QMessageBox.No)
        if reply:
            row = self.ui.lswResultados.currentRow()
            session.query(Frase).filter_by(id=self.resultados[row]).delete()
            session.commit()
            del self.resultados[row]
            self.ui.lswResultados.takeItem(row)
            

    def pesquisar(self):
        termo = self.ui.edtPesquisar.displayText()
        self.resultados = []
        if self.ui.cbxCampo.currentText() == "Conteúdo":
            frases = session.query(Frase).filter(Frase.texto.like(r'%{}%'.format(termo))).limit(10).all()
        else:
             frases = session.query(Frase).filter(Frase.palavras_chave.like(r'%{}%'.format(termo))).limit(10).all()
        self.ui.lswResultados.clear()
        for frase in frases:
            texto = frase.texto
            if len(texto) > 500:
                texto = texto[:500] + "..."
            self.ui.lswResultados.addItem(texto)
            self.resultados.append(frase.id)

    def itemClicked(self, item):
        frase = session.query(Frase).get(self.resultados[self.ui.lswResultados.currentRow()])
        word.Selection.TypeText(frase.texto)
        self.close()

    # def showEvent(self, event):
    #     self.ui.edtPesquisar.setText(word.Selection.Text)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
