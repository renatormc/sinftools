from ui_editar_objeto import Ui_EditarObjeto
from PyQt5.QtWidgets import QDialog
import repo

class EditarObjeto(QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_EditarObjeto()
        self.ui.setupUi(self)
        self.connections()
        for tipo in repo.get_tipos_objetos():
            self.ui.cbx_tipo.addItem(tipo.nome)


    def connections(self):
        pass

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = EditarObjeto()
    w.show()
    sys.exit(app.exec_())