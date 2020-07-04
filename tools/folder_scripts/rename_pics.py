import os

files_ = os.listdir()
n_objects = int(len(files_)/3)

ext = files_[0].split(".")[-1]

for i in range(n_objects):
    for j in range(3):
        pos = j*n_objects + i
        os.rename(files_[pos], f"C{i+1}_{j+1}.{ext}")
       