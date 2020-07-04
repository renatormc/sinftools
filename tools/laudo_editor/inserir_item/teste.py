from widgets.teste2.controller import Teste2
import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
teste = Teste2()
teste.show()
sys.exit(app.exec_())
