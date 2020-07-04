from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QVBoxLayout, QPushButton
from widgets.celular.controller import Celular
from view import Ui_MainWindow
from word_handler import WordHandler
import json
import codecs
import importlib
from inflection import camelize
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.wh = WordHandler()
        self.connections()
        with open("{}\\widget_list.json".format(script_dir), "r") as json_file:
            widgets = json.load(json_file)
        for widget in widgets:
            self.ui.liwItensDisponiveis.addItem(widget)
        self.itens_categorias = {}
        self.widgets = {}
    
    def connections(self):
        self.ui.btnOK.clicked.connect(self.gerar)
        self.ui.liwItensDisponiveis.itemDoubleClicked.connect(self.adicionar_item)
        self.ui.liwItensAdicionados.itemDoubleClicked.connect(self.deletar_item)

       
    def gera_nome(self, categoria):
        if categoria in self.itens_categorias:
            self.itens_categorias[categoria] += 1
        else:
            self.itens_categorias[categoria] = 1
        return "{}_{}".format(camelize(categoria), self.itens_categorias[categoria])

    def adicionar_item(self, item):
        nome = self.gera_nome(item.text())
        self.ui.liwItensAdicionados.addItem(nome)
        module_name = "widgets.{}.controller".format(item.text())
        class_name = camelize(item.text())
        class_= getattr(importlib.import_module(module_name), class_name)
        instance = class_()
        instance.setWordHandler(self.wh)
        instance.ui.groGeral.setTitle(nome)
        self.widgets[nome] = instance
        self.ui.scrollArea.widget().layout().addWidget(instance)

    def deletar_item(self, item):
        self.widgets[item.text()].deleteLater()
        del(self.widgets[item.text()])
        self.ui.liwItensAdicionados.takeItem(self.ui.liwItensAdicionados.row(item))

    def gerar(self):
        for wd in self.widgets:
            self.widgets[wd].inserir_word()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    principal = Principal()
    principal.show()
    sys.exit(app.exec_())