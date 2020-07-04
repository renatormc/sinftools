from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QToolButton, QWidget, QSizePolicy, QSpacerItem, QLabel, QWidget
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import pyqtSignal, Qt
import settings
import os
from helpers import organize_items_rows_and_columns
import uuid
from widgets.scat_edit import SCatEdit
from widgets.scheck_box import SCheckBox
from widgets.scombo_box import SComboBox
from widgets.simage_chooser import SImageChooser
from widgets.simage_group import SImageGroup
from widgets.sline_edit import SLineEdit
from widgets.spacer import Spacer
from widgets.stext_edit import STextEdit
from widgets.sspin_box import SSpinBox
from helpers import get_list
from widgets.flow_layout import FlowLayout

def get_widget(config, config_all):
    label = QLabel(config['label']) if 'label'in config.keys(
    ) and config['label'] else None
    if config['type'] == "edit":
        widget = SLineEdit(config)
        return label, widget
    if config['type'] == "text":
        widget = STextEdit(config)
        return label, widget
    if config['type'] == "spinbox":
        widget = SSpinBox(config)
        return label, widget
    if config['type'] == "combo":
        widget = SComboBox(config)
        if isinstance(config['list'], str) and config['list'] == 'gender':
            widget.add_item('M')
            widget.add_item('F')
        elif isinstance(config['list'], str):
            list_ = get_list(config['list'])
            for item in list_:
                widget.add_item(item)
        elif isinstance(config['list'], list):
            for item in config['list']:
                widget.add_item(item)
        widget.update_default()
        return label, widget
    if config['type'] == "cat_edit":
        widget = SCatEdit(config)
        if isinstance(config['list'], str) and config['list'] == 'gender':
            widget.combo.addItem('M')
            widget.combo.addItem('F')
        elif isinstance(config['list'], str):
            list_ = get_list(config['list'])
            for item in list_:
                widget.combo.addItem(item)
        elif isinstance(config['list'], list):
            for item in config['list']:
                widget.combo.addItem(item)
        return label, widget
    if config['type'] == "image_chooser":
        widget = SImageChooser(config, config_all)
        return label, widget
    if config['type'] == "image_group":
        widget = SImageGroup(config, config_all)
        return label, widget
    if config['type'] == 'repeat':
        widget = Repeat(config, config_all)
        return label, widget
    if config['type'] == 'checkbox':
        widget = SCheckBox(config)
        label.setText("")
        return label, widget
    if config['type'] == 'spacer':
        widget = Spacer()
        return label, widget


class Repeat(QWidget):
    has_data = True
    changed_content = pyqtSignal()

    def __init__(self, config, config_all):
        super(QWidget, self).__init__()
        self.setupUi()
        self.config = config
        self.config_all = config_all
        self.widgets = {}
        self.clear_()

    def setupUi(self):
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0,0,0,50))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.main_layout = QVBoxLayout()
        self.items_layout = FlowLayout()
        self.setLayout(self.main_layout)
        h_layout = QHBoxLayout()

        self.btn_add = QToolButton()
        icon = QIcon(os.path.join(settings.app_dir, "resources", "icon.png"))
        self.btn_add.setIcon(icon)
        self.btn_add.clicked.connect(self.add)
        h_layout.addWidget(self.btn_add)
        self.main_layout.addLayout(h_layout)

        spacer = QSpacerItem(150, 10, QSizePolicy.Expanding)
        h_layout.addSpacerItem(spacer)

        self.main_layout.addLayout(self.items_layout)

    def add(self):
        group_widget = QWidget()
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255,229,204,100))
        group_widget.setAutoFillBackground(True)
        group_widget.setPalette(palette)

        v_layout = QVBoxLayout()
        items = self.config['items']
        rows = organize_items_rows_and_columns(items)
        widgets = []
        for key, items in rows.items():
            h_layout = QHBoxLayout()
            for item in items:
                label, widget = get_widget(item, self.config_all)
                layout = QVBoxLayout()
                widgets.append(widget)
                if label is not None:
                    layout.addWidget(label)
                if item['type'] == 'spacer':
                    layout.addSpacerItem(widget)
                else:
                    layout.addWidget(widget)
                h_layout.addLayout(layout, item['stretch'])
            v_layout.addLayout(h_layout)
        id = uuid.uuid4()
        btn = QToolButton()
        icon = QIcon(os.path.join(settings.app_dir,
                                  "resources", "exclude.png"))
        btn.setIcon(icon)
        btn.setFocusPolicy(Qt.NoFocus)
        btn.clicked.connect(lambda: self.delete_widget(id))
        group_h_layout = QHBoxLayout()
        group_h_layout.addLayout(v_layout)
        group_h_layout.addWidget(btn)
        group_widget.setLayout(group_h_layout)
        self.items_layout.addWidget(group_widget)
        self.widgets[id] = {'widgets': widgets, 'group_widget': group_widget}
        self.changed_content.emit()
        return id

  
    def delete_widget(self, id):
        self.widgets[id]['group_widget'].deleteLater()
        del self.widgets[id]

    def get_data(self):
        items = []
        for key, value in self.widgets.items():
            item = {}
            for w in value['widgets']:
                item[w.config['name']] = w.get_data()
            items.append(item)
        return items

    def get_data_json(self):
        items = []
        for key, value in self.widgets.items():
            values = []
            for w in value['widgets']:
                values.append(w.get_data_json())
            items.append(values)
        return items

    def set_data_json(self, data):
        self.clear_(set_default=False)
        for values in data:
            id = self.add()
            for i, w in enumerate(self.widgets[id]['widgets']):
                w.set_data_json(values[i])

    def clear_(self, set_default=True):
        for key in list(self.widgets.keys()):
            self.delete_widget(key)
        if set_default and 'initial' in self.config.keys():
            for i in range(self.config['initial']):
                self.add()
