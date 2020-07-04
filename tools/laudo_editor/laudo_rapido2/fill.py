import os
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QMessageBox, QFileDialog, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QIcon, QIcon
from helpers import get_config, organize_items_rows_and_columns, get_folder_recently
from widgets.repeat import get_widget
from word_manager_xml import WordManagerXml
from word_manager_docx import WordManagerDocx
import traceback
import settings
import codecs
import json
from pathlib import Path
import pickle


class WindowFill(QWidget):
    def __init__(self, item):
        QWidget.__init__(self)
        self.item = item
        self.config = get_config(self.item)
        self.setup_ui()
        self.connections()

    def setup_ui(self):
        self.setWindowIcon(QIcon(os.path.join(settings.app_dir, "icon.png")))
        self.main_layout = QVBoxLayout()
        self.setWindowTitle(f"Inserir {self.config['label']}")
        items = self.config['items']
        self.widgets = []
        rows = organize_items_rows_and_columns(items)
        for key, items in rows.items():
            h_layout = QHBoxLayout()
            for item in items:
                label, widget = get_widget(item, self.config)
                layout = QVBoxLayout()
                self.widgets.append(widget)
                if label is not None:
                    layout.addWidget(label)
                if item['type'] == 'spacer':
                    layout.addSpacerItem(widget)
                elif item['type'] in ['cat_edit']:
                    layout.addLayout(widget)
                else:
                    layout.addWidget(widget)
                h_layout.addLayout(layout, item['stretch'])
            self.main_layout.addLayout(h_layout)

        spacer = QSpacerItem(500, 10,  QSizePolicy.Minimum,
                             QSizePolicy.Expanding)
        self.main_layout.addSpacerItem(spacer)
        self.btn_recently_load = QPushButton("Carregar último preenchimento")
        icon = QIcon(os.path.join(settings.app_dir, "resources", "file.png"))
        self.btn_recently_load.setIcon(icon)
        self.btn_fill_load = QPushButton("Carregar preenchimento")
        icon = QIcon(os.path.join(settings.app_dir, "resources", "file.png"))
        self.btn_fill_load.setIcon(icon)
        self.btn_fill_save = QPushButton("Salvar preenchimento")
        icon = QIcon(os.path.join(settings.app_dir, "resources", "save.jpg"))
        self.btn_fill_save.setIcon(icon)
        self.btn_clear = QPushButton("Limpar")
        icon = QIcon(os.path.join(settings.app_dir, "resources", "clear.png"))
        self.btn_clear.setIcon(icon)
        self.btn_insert_word = QPushButton("Inserir no Word aberto")
        icon = QIcon(os.path.join(settings.app_dir, "resources", "word3.jpg"))
        self.btn_insert_word.setIcon(icon)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.btn_recently_load)
        self.buttons_layout.addWidget(self.btn_fill_load)
        self.buttons_layout.addWidget(self.btn_fill_save)
        self.buttons_layout.addWidget(self.btn_clear)
        self.buttons_layout.addWidget(self.btn_insert_word)

        self.main_layout.addLayout(self.buttons_layout)
        # self.main_layout.addWidget(self.btn_ok, i + 1, 1)

        self.setLayout(self.main_layout)

    def connections(self):
        self.btn_insert_word.clicked.connect(self.insert_word)
        self.btn_clear.clicked.connect(self.clear_)
        self.btn_fill_save.clicked.connect(self.fill_save)
        self.btn_fill_load.clicked.connect(self.fill_load)
        self.btn_recently_load.clicked.connect(self.load_recently)

    def save_to_file(self, file_):
        data = {}
        for widget in self.widgets:
            if widget.has_data:
                data[widget.config['name']] = widget.get_data_json()
        with codecs.open(file_, "w", "utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))

    def fill_save(self):
        filename, temp = QFileDialog.getSaveFileName(
            self, "Salvar preenchimento", "", "Arquivo json (*.json)")
        if filename and filename != "":
            self.save_to_file(filename)

    def save_recently(self):
        path = get_folder_recently()
        file_ = path / f"{self.item['name']}.json"
        self.save_to_file(file_)


    def load_from_file(self, file_):
        with codecs.open(file_, "r", "utf-8") as f:
            data = json.load(f)
        keys = data.keys()
        for widget in self.widgets:
            if widget.has_data and widget.config['name'] in keys:
                widget.set_data_json(data[widget.config['name']])
    
    def load_recently(self):
        path = get_folder_recently()
        file_ = path / f"{self.item['name']}.json"
        if file_.exists():
            self.load_from_file(file_)

   
    def fill_load(self):
        self.updateGeometry()
        filename, temp = QFileDialog.getOpenFileName(
            self, "Carregar preenchimento", "", "Arquivo json (*.json)")
        if filename and filename != "":
           self.load_from_file(filename)

    def printError(self, e):
        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" % ex_value)
        print("\n".join(stack_trace))

    def showError(self, e):
        ex_type, ex_value, ex_traceback = sys.exc_info()
        trace_back = traceback.extract_tb(ex_traceback)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        lines = []
        lines.append("Exception type : %s " % ex_type.__name__)
        lines.append("Exception message : %s" % ex_value)
        text = "Exception type : %s " % ex_type.__name__
        text += "\nException message : %s" % ex_value
        text += "\n" + "\n".join(stack_trace)
        QMessageBox.warning(self, "Erro", text)

    def insert_word(self):
        self.save_recently()
        try:

            context = {}
            for widget in self.widgets:
                if widget.has_data:
                    context[widget.config['name']] = widget.get_data()

            #load old data
            path = Path(sys.argv[1]) / "old_data"
            old_data = {}
            if path.exists():
                with path.open("rb") as f:
                    old_data = pickle.load(f)
                    print(old_data)
            for key, value in old_data.items():
                if key not in context.keys():
                    context[key] = value

            if self.config['template'].endswith('xml') or self.config['template'].endswith('html'):
                word_manager = WordManagerXml()
            else:
                word_manager = WordManagerDocx()
            word_manager.render_word(self.config, context)
           
            #save old data
            with path.open("wb") as f:
                pickle.dump(context, f)
                              
         
        except Exception as e:
            self.printError(e)
            self.showError(e)

    def clear_(self):
        for widget in self.widgets:
            widget.clear_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    web = WindowFill({"name": "celular"})
    web.setGeometry(600, 300, 600, 100)
    web.show()
    sys.exit(app.exec_())  # only need one app, one running event loop
