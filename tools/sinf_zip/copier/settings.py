import os
import sys

if getattr(sys, 'frozen', False):
    app_dir = sys._MEIPASS
else:
    app_dir = os.path.dirname(os.path.realpath(__file__)) 