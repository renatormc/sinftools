import os
import shutil
for root, dirs, files in os.walk(os.getcwd()):
   for name in files:
      shutil.move(os.path.join(root, name), name)

for root, dirs, files in os.walk(os.getcwd()):
   for dir_ in dirs:
       path = os.path.join(root, dir_)
       if os.path.exists(path):
           shutil.rmtree(path)
     