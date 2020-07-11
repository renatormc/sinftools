from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from editar_objeto import EditarObjeto
from mongo import *
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.column_map = {
            0: ('nome', 'Nome'),
            1: ('tipo', 'Tipo')
        }
        self.load_objects()

    def connections(self):
        self.ui.act_new_object.triggered.connect(self.novo_objeto)

    def __add_item_table(self, objeto: Objeto):
        row = self.ui.tbw_objetos.rowCount()
        self.ui.tbw_objetos.insertRow(row)
        for key, value in self.column_map.items():
            item = QTableWidgetItem(getattr(objeto, value[0]))
            self.ui.tbw_objetos.setItem(row, key, item)
            item = QTableWidgetItem(objeto.tipo)
            self.ui.tbw_objetos.setItem(row, 1, item)
            # self.ui. tbw_process.setItem(i, key, item)

    def novo_objeto(self):
        editar_objeto = EditarObjeto()
        editar_objeto.exec_()
        objeto = Objeto()
        nome = editar_objeto.ui.led_nome.displayText().strip().upper()
        caso = re.search(r'(\w+).+', nome).group(1)
        objeto.nome = editar_objeto.ui.led_nome.displayText()
        objeto.caso = caso
        objeto.tipo = editar_objeto.ui.cbx_tipo.currentText()
        objeto.save()
        self.load_objects()

    def load_objects(self):
        objetos = Objeto.objects.all()
        for objeto in objetos:
            self.__add_item_table(objeto)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())