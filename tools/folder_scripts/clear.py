from pathlib import Path 
import os
from sys import exit
import shutil

folder = os.path.join(Path.home(), "AppData", "Local", "Temp", "gen_py", "3.7")
if not os.path.exists(folder):
    print(f"A pasta '{folder}' não foi encontrada.")
    exit()

for root, dirs, files in os.walk(folder):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))
