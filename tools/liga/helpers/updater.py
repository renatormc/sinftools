from pathlib import Path
import os
import subprocess

username = "sinf"
password = "sptcICLR."
sinftools_dir = os.getenv("SINFTOOLS")
sinftools_dir_server = r'\\10.129.3.14\compartilhada\SOFTWARE\sinftools'
dirs = [
    'Miniconda3',
    'notebooks',
    'scripts',
    'tools'
]


class Updater:

    def connect_network(self, folder):
        if not os.path.isdir(folder):
            mount_command = "net use /user:" + username + " " + folder + " " + password
            os.system(mount_command)
            if not os.path.isdir(folder):
                return None
        return Path(folder)

    def sync_files_dir(self, source, dest):
        args = ['robocopy', str(source), str(
            dest), '/mir', '/R:10', '/W:3']
        process = subprocess.Popen(args, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        text = out.decode("CP850")
        text += "\n" + err.decode("CP850")
        return text

    def update(self):
        folder = self.connect_network(sinftools_dir_server)
        if not folder:
            return f"Não foi possível se conectar a pasta {folder}"
        results = []
        for dir_ in dirs:
            results.append(self.sync_files_dir(folder / dir_, os.path.join(sinftools_dir, dir_)))
        return "\n".join(results)

  