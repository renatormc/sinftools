import shutil
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

def copy_script():
    shutil.copy(os.path.join(script_dir, "macro.py"), "macro.py")
    shutil.copy(os.path.join(script_dir, "edit_script.vbs"), "edit_script.vbs")