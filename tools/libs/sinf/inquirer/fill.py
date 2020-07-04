import os
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QMessageBox, QFileDialog, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QIcon, QIcon
from helpers import get_config, organize_items_rows_and_columns
from widgets.repeat import get_widget
import traceback
import settings
import codecs
import json


class WindowFill(QWidget):
    def __init__(self, filepath, tempfile):
        QWidget.__init__(self)
        self.filepath = filepath
        self.tempfile = tempfile
        self.config = get_config(self.filepath)
        self.setup_ui()
        self.connections()
        

    def setup_ui(self):

        self.setWindowIcon(QIcon(os.path.join(settings.app_dir, "resources", "form.png")))
        self.main_layout = QVBoxLayout()

        self.setWindowTitle(self.config['label'])
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

       
    
        self.btn_ok = QPushButton("OK")
        icon = QIcon(os.path.join(settings.app_dir, "resources", "ok.png"))
        self.btn_ok.setIcon(icon)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.btn_ok)

        self.main_layout.addLayout(self.buttons_layout)
        # self.main_layout.addWidget(self.btn_ok, i + 1, 1)

        self.setLayout(self.main_layout)

    def connections(self):
        self.btn_ok.clicked.connect(self.ok_exec)
       

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

    def ok_exec(self):
        try:
            context = {}
            for widget in self.widgets:
                if widget.has_data:
                    context[widget.config['name']] = widget.get_data()
            with codecs.open(self.tempfile, "w", "utf-8") as f:
                f.write(json.dumps(context, indent=4, ensure_ascii=False))
            self.close()
        except Exception as e:
            self.printError(e)
            self.showError(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    web = WindowFill(sys.argv[1], sys.argv[2])
    web.setGeometry(600, 300, 600, 100)
    web.show()
    sys.exit(app.exec_())  # only need one app, one running event loop
