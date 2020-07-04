from ui_main import Ui_MainWindow
from widgets.w import W
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
import win32com.client as win32
import os
import sys
import re

word = win32.gencache.EnsureDispatch('Word.Application')
doc = word.ActiveDocument

class MainWindow(QMainWindow):
    mudou_diretorio = pyqtSignal(str)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.inspecionarWord()
        if len(sys.argv) > 1:
            self.dir = sys.argv[1]
        else:
            self.dir = "C:\\"
        self.criarWidgets()
       

    def inspecionarWord(self):
        comp = re.compile(r'#.*?#')
        self.lista = []
        for par in word.Selection.Paragraphs:
            for item in comp.findall(str(par)):
                if item not in self.lista and item.replace(" ", "")[1] == "@":
                    self.lista.append(item)

    def criarWidgets(self):
        self.widgets = []
        for item in self.lista:
            widget = W()
            # res = re.search(r'#@(.*?)[{#]', item)
            # widget.ui.lblTag.setText(res.groups()[0])
            widget.ui.lblTag.setText(item)
            widget.mudou_diretorio.connect(self.mudouDiretorio)
            self.mudou_diretorio.connect(widget.setDir)
            self.ui.layout.addWidget(widget)
            self.widgets.append(widget)
        self.mudou_diretorio.emit(self.dir)
    
    def mudouDiretorio(self, dire):
        self.mudou_diretorio.emit(dire)

    def connections(self):
        self.ui.btnOk.clicked.connect(self.ok)

    def ok(self):
        selecao = word.Selection
        for widget in self.widgets:
            tag, path = widget.ui.lblTag.text(), widget.ui.edtArquivo.text()
            res = re.search(r'\{(.*?)\}', tag)
            largura_desejada = float(res.group().strip().replace('{', '').replace('}','')) if res else None
            if path != '':
                selecao.Find.Text = tag
                selecao.Find.Execute(Forward=True)
                pic = word.Selection.InlineShapes.AddPicture(path.replace("/", "\\"))
                if largura_desejada:
                    proporcao = largura_desejada/pic.Width
                    pic.Width = largura_desejada
                    pic.Height = proporcao*pic.Height
        self.close()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
