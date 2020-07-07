from PyQt5.QtWidgets import QApplication
from fila.main_window import Window
import sys

app = QApplication(sys.argv)
app.setStyle('Fusion')
standalone = len(sys.argv) > 1 and sys.argv[1] == 'standalone'
w = Window(standalone=standalone)
w.setGeometry(500, 50, 1300, 800)
w.setWindowTitle(f"Gerenciador de fila de processos")
w.show()
sys.exit(app.exec_())