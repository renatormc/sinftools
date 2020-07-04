from widgets.scat_edit import SCatEdit
from widgets.scheck_box import SCheckBox
from widgets.scombo_box import SComboBox
from widgets.simage_chooser import SImageChooser
from widgets.simage_group import SImageGroup
from widgets.sline_edit import SLineEdit
from widgets.spacer import Spacer
from widgets.stext_edit import STextEdit
from widgets.repeat import Repeat
from helpers import get_list
from PyQt5.QtWidgets import QLabel

def get_widget(config, config_all):
    label = QLabel(config['label']) if 'label'in config.keys(
    ) and config['label'] else None
    if config['type'] == "edit":
        widget = SLineEdit(config)
        return label, widget
    if config['type'] == "text":
        widget = STextEdit(config)
        return label, widget
    if config['type'] == "combo":
        widget = SComboBox(config)
        if isinstance(config['list'], str):
            list_ = get_list(config['list'])
            for item in list_:
                widget.addItem(item)
        if isinstance(config['list'], list):
            for item in config['list']:
                widget.addItem(item)
        return label, widget
    if config['type'] == "cat_edit":
        widget = SCatEdit(config)
        if isinstance(config['list'], str):
            list_ = get_list(config['list'])
            for item in list_:
                widget.combo.addItem(item)
        if isinstance(config['list'], list):
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