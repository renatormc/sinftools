from ui_main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from subprocess import Popen
import os
import sys
#import qdarkstyle
script_dir = os.path.dirname(os.path.realpath(__file__))

sinftools_dir = os.getenv("SINFTOOLS")


class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        if len(sys.argv) > 1:
            self.dir = sys.argv[1]
        else:
            self.dir = "C:\\"

    def connections(self):
        self.ui.btnSubstituirSelecao.clicked.connect(self.substituirSelecao)
        self.ui.btnInserirFotos.clicked.connect(self.inserirFotos)
        self.ui.btnInserirQuadro.clicked.connect(self.inserirQuadro)
        self.ui.btnSubstituirTudo.clicked.connect(self.substituirTudo)
        self.ui.btnInserirFiguras.clicked.connect(self.inserirFiguras)
        self.ui.btnInserirTabela.clicked.connect(self.inserirTabela)
        self.ui.btnSubstituirFotos.clicked.connect(self.substituirFotos)
        self.ui.btnInserirFigurasLegenda.clicked.connect(self.inserirFigurasLegenda)
        self.ui.btnPesquisarFrase.clicked.connect(self.pesquisarFrase)
        self.ui.btnInserirModelo.clicked.connect(self.inserirModelo)
        self.ui.btnInserirModelos.clicked.connect(self.inserirModelos)
        self.ui.btnAdicionarFrase.clicked.connect(self.adicionarFrase)
        self.ui.btnAdicionarFraseRemota.clicked.connect(self.adicionarFraseRemota)
        self.ui.btnLaudoRapido.clicked.connect(self.laudoRapido)
        self.ui.btnOutrasAcoes.clicked.connect(self.outrasAcoes)

    def substituirSelecao(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\substituir_selecao.py".format(sinftools_dir, script_dir))
        self.close()

    def inserirFotos(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\inserir_fotos.py".format(sinftools_dir, script_dir))
        self.close()

    def inserirQuadro(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\quadro_inserir.py".format(sinftools_dir, script_dir))
        self.close()

    def substituirTudo(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\substituir_tudo.pyw".format(sinftools_dir, script_dir))
        self.close()

    def inserirFiguras(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\inserir_figuras.py".format(sinftools_dir, script_dir))
        self.close()

    def inserirTabela(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\tabela_inserir.py {}".format(script_dir, self.ui.edtDimensoesTabela.text()))
        self.close()

    def substituirFotos(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\substituir_fotos\main.pyw {}".format(script_dir, self.dir))
        self.close()

    def inserirFigurasLegenda(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\inserir_figuras_legenda.py".format(sinftools_dir, script_dir))
        self.close()

    def pesquisarFrase(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\frasesprontas\\pesquisar.py".format(sinftools_dir, script_dir))
        self.close()

    def inserirModelo(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\modelo_inserir\\modelo_inserir.pyw".format(sinftools_dir, script_dir))
        self.close()

    def inserirModelos(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\modelo_so_inserir\\modelo_so_inserir.pyw".format(sinftools_dir, script_dir))
        self.close()

    def adicionarFrase(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\frasesprontas\\adicionar.py".format(sinftools_dir, script_dir))
        self.close()

    def adicionarFraseRemota(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\frasesprontas\\adicionar_frase_remota.py".format(sinftools_dir, script_dir))
        self.close()

    def laudoRapido(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\tools\\laudo_editor\\laudo_rapido2\\main.py".format(sinftools_dir, script_dir))
        self.close()

    def outrasAcoes(self):
        Popen("\"{}\\extras\\Python\\pythonw\" {}\\..\\comandos.py".format(sinftools_dir, script_dir))
        self.close()
    

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
