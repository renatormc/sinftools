#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, hashlib, sys
import io
import codecs
#from uteis.carrega_configuracoes import *
##config = carrega_configuracoes(os.path.abspath(__file__),0)



#Definições   - BEGIN
NomeDoArquivoHash = 'Hash.txt'
NomeDoArquivoHashdoHash = 'Hash do hash.txt'
NomeDoArquivoDeLogs ="Hash Logs.txt"
ignore=[
    ".report"
]
#Definições - END

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(357, 129)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_cancelar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancelar.setObjectName("btn_cancelar")
        self.horizontalLayout.addWidget(self.btn_cancelar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculando Hash"))
        self.btn_cancelar.setText(_translate("MainWindow", "Calcelar"))

    def atualizar_progresso(self, valor):
        self.progressBar.setValue(valor)

class hash_calculator(QtCore.QObject):
    calculou_mais_um = QtCore.pyqtSignal(float)
    finalizou = QtCore.pyqtSignal()

    def __init__(self, dir):
        super(self.__class__, self).__init__()
        self.diretorio = dir
        self.pediu_para_cancelar = False

    def ListaDeArquivos(self, rootDir):
        arquivos = []
        list_dirs = os.walk(rootDir)
        for root, dirs, files in list_dirs:
            if root.split('\\')[-1] in ignore:
                continue
            for f in files:
                arquivos.append(os.path.join(root, f))
        return arquivos

    def Sha512(self, fname):
        hash_sha512 = hashlib.sha512()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()

    def run(self):
        config = {}
        config["Diretorio"] = self.diretorio
        config["Diretorio_arquivo_hash"] = self.diretorio
        erros = []

        Arq = io.StringIO()
        ArqHashdoHash = io.StringIO()
        lista_arquivos = self.ListaDeArquivos(config['Diretorio'])
        total = len(lista_arquivos)
        for count, item in enumerate(lista_arquivos):
            if self.pediu_para_cancelar:
                break
            try:
                # print("Calculando arquivo " + item.replace(config['Diretorio'] + '\\',"").replace('\\','/'))
                Arq.write(self.Sha512(item) + '  ' + item.replace(config['Diretorio'] + '\\', "").replace('\\', '/'))
                self.calculou_mais_um.emit(100 * (count + 1) / total)
                Arq.write('\n')
            except:
                try:
                    Arq.write(
                        self.Sha512(item) + '  ' + item.replace(config['Diretorio'] + '\\', "").replace('\\', '/'))
                    Arq.write('\n')
                except:
                    erros.append("\nErro no arquivo: " + str(item))
        Arq.seek(0)
        with codecs.open(config["Diretorio"] + "\\" + NomeDoArquivoHash, 'w', encoding='utf-8') as f:
            f.write(Arq.read())

        HashdoHash = self.Sha512(config['Diretorio'] + "\\" + NomeDoArquivoHash)
        ArqHashdoHash.write(HashdoHash)

        ArqHashdoHash.seek(0)
        with open(config["Diretorio"] + "\\" + NomeDoArquivoHashdoHash, 'w') as f:
            f.write(ArqHashdoHash.read())
        print("\nTerminou!")
        self.finalizou.emit()


if __name__ == "__main__":
    os.chdir(sys.argv[1])
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()


    def cancelar_procedimento():
        calculator.pediu_para_cancelar = True

    thread = QtCore.QThread()
    calculator = hash_calculator(os.getcwd())
    calculator.calculou_mais_um.connect(ui.atualizar_progresso)
    ui.btn_cancelar.clicked.connect(cancelar_procedimento)
    ##calculator.finalizou.connect(app.quit)
    thread.finished.connect(app.quit)
    calculator.finalizou.connect(thread.quit)
    calculator.moveToThread(thread)
    thread.started.connect(calculator.run)
    thread.start()
    sys.exit(app.exec_())

