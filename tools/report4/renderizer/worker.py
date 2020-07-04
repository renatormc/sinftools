from renderizer.renderizer import Renderizer
import os 
import shutil
from renderizer import Renderizer
script_dir = os.path.dirname(os.path.realpath(__file__))


class Worker:
    def render(self):
        self.copy_files()
        self.renderizer = Renderizer(os.path.join(script_dir, 'templates'))

    def copy_files():
        folder = os.path.join(script_dir, 'html_files')
        if not os.path.exists('html_files'):
            shutil.copytree(folder, 'html_files')