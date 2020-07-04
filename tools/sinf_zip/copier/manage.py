import sys
import os
import shutil
import settings

def build():
    destdir = "C:\\sinftools\\tools\\sinf_zip\\MB"
    if os.path.exists(destdir):
        shutil.rmtree(destdir)
    os.mkdir(destdir)
    name = "sinf_copier"
    os.system(f"s-pyinstaller --clean --win-private-assemblies --distpath {settings.app_dir}\\dist --add-data \"icon.png\";. --workpath ./build --name {name} --hidden-import PyQt5.sip main.py")
   
   
locals()[sys.argv[1]]()

