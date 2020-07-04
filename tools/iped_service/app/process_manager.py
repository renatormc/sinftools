from models import *
from database import db_session
import subprocess
import shlex
import psutil
from datetime import datetime
import config
import win32con
import win32gui
import win32process
import time
from pathlib import Path
import os
import shutil
import stat
import errno
from iped_config_read import IpedConfigReader


def handleError(func, path, exc_info):
    print('Handling Error for file ', path)
    print(exc_info)
    # Check if file access issue
    if not os.access(path, os.W_OK):
        print('Hello')
        # Try to change the permision of file
        os.chmod(path, stat.S_IWUSR)
        # call the calling function again
        func(path)


class ProcessManager(object):
   
    def __init__(self):
        super(ProcessManager, self).__init__()
        

    def exec(self, args):
        p = subprocess.Popen(args)

    def edit_process(self, data_form, proc=None):
        try:
            process = proc or Process()
            process.name = data_form['name']
            process.perito = data_form['perito']
            process.profile = data_form['profile']
            process.output_folder = str(data_form['output_folder'])
            process.extra_params = data_form['extra_params']
            process.queue_order = data_form['queue_order']
            process.sources = "\n".join([str(item) for item in data_form['sources']])
            if not proc:
                process.status = "ADICIONADO"
            db_session.add(process)
            db_session.commit()
            self.check_process()
        except Exception as e:
            self.error.emit(e)

    def queue(self, proc: Process):
        path = Path(proc.output_folder) / "indexador"
        if path.exists() and path.is_dir():
            raise Exception(
                f"O diretório \"{path.parent}\" contém arquivos de processamentos anteriores que precisam ser deletados antes de se iniciar um novo processamento.")
        proc.status = "AGUARDANDO"
        proc.start_waiting = datetime.now()
        db_session.add(proc)
        db_session.commit()
        self.check_process()

    def get_args(self, proc: Process, iped_folder: Path):
        args = ['javaw', '-jar', str(iped_folder / "iped.jar"), '-profile', proc.profile]
        sources = proc.sources.split("\n")
        for source in sources:
            args.append('-d')
            args.append(str(source))
        args.append('-o')
        args.append(proc.output_folder)
        if proc.extra_params:
            args += shlex.split(proc.extra_params)
        return args

    def get_command_string(self, proc: Process):
        if not proc.iped_folder:
            return ''
        args = self.get_args(proc, Path(proc.iped_folder))
        for i, item in enumerate(args):
            item = item.strip()
            if " " in item and not (item.startswith('"') and item.endswith('"')):
                args[i] = f'"{item}"'
        return " ".join(args)


    def get_available_iped(self):
        ipeds_using = [proc.iped_folder for proc in
                       db_session.query(Process).filter(Process.status == "PROCESSANDO").all()]
        for folder in config.iped_folders:
            if str(folder) not in ipeds_using:
                return folder

    def delete_temp_files(self, iped_folder):
        reader = IpedConfigReader(iped_folder)
        temp = Path(reader.get_temp_folder())
        if temp.exists() and temp.is_dir():
            shutil.rmtree(temp)


    def init_process(self, proc: Process):
        try:
            path = Path(proc.output_folder)
            if not path.exists():
                os.makedirs(path)
            path2 = path / "indexador"
            if path2.exists() and path2.is_dir():
                raise Exception(
                    f"O diretório \"{path2}\" contém arquivos de processamentos anteriores que precisam ser deletados antes de se iniciar um novo processamento.")

            #checar se tem algum iped disponível
            iped_available = self.get_available_iped()
            if not iped_available:
                return

            self.delete_temp_files(iped_available)
            args = self.get_args(proc, iped_available)

            print(" ".join(args))
            path_log = proc.get_file_log()
            with path_log.open("w+") as f:
                p = subprocess.Popen(args, stdout=f)
            proc.pid = p.pid
            p = psutil.Process(proc.pid)
            proc.start = datetime.fromtimestamp(p._create_time)
            proc.finish = None
            proc.status = "PROCESSANDO"
            proc.iped_folder = str(iped_available)
            db_session.add(proc)
            db_session.commit()
        except Exception as e:
            proc.status = "ERRO"
            db_session.add(proc)
            db_session.commit()
            self.error.emit(e)

    def cancel_process(self, proc: Process):
        self.kill_process(proc)
        proc.status = "CANCELADO"
        db_session.add(proc)
        db_session.commit()
        self.updated.emit()


    def kill_process(self, proc):
        if not proc.pid:
            return
        try:
            p = psutil.Process(proc.pid)
            create_time = datetime.fromtimestamp(p._create_time)
            if create_time == proc.start:
                p.kill()
                self.check_process()
        except psutil.NoSuchProcess:
            print("Processo não existente")
        except Exception as e:
            self.error.emit(e)

    def check_process(self):
        return
        # Checar se algum que estava processando finalizou ou deu erro
        # processess = db_session.query(Process).order_by(Process.queue_order.desc(), Process.start_waiting.asc()).all()
        # for proc in processess:
        #     try:
        #         p = psutil.Process(proc.pid)
        #         if proc.start != datetime.fromtimestamp(p._create_time):
        #             raise psutil.NoSuchProcess(p.pid)
        #         proc.status = "PROCESSANDO"
        #     except psutil.NoSuchProcess:
        #         proc.status = self.check_process_finished(proc)
        #         proc.finish = datetime.now()
        #     db_session.add(proc)
        # db_session.commit()

        # # Verificar para mais quantos tem vaga e iniciar o processamento por ordem de chegada
        # n = config.max_simultaneous - db_session.query(Process).filter(Process.status == 'PROCESSANDO').count()
        # if n < 0:
        #     n = 0
        # procs = db_session.query(Process).filter(Process.status == 'AGUARDANDO').order_by(
        #     Process.start_waiting.asc()).limit(n).all()
        # for proc in procs:
        #     self.init_process(proc)
      

    def get_hwnds_for_pid(self, pid):
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds

    def maximize_pid(self, pid, term):
        for hwnd in self.get_hwnds_for_pid(pid):
            title = win32gui.GetWindowText(hwnd)
            print(title)
            if term in title:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
                # time.sleep(2.0)
                # rect = win32gui.GetClientRect(hwnd)
                # if rect:
                #     x0, y0, x1, y1 = rect
                #     x0, y0 = win32gui.ClientToScreen(hwnd, (x0, y0))
                #     x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x0, y1 - y0))
                #     im = pyautogui.screenshot(region=(x0, y0, x1, y1))
                #     return im

    def check_process_finished(self, proc: Process):
        path = proc.get_file_log()
        if path.exists():
            with path.open("r") as f:
                text = f.read()
            if "IPED finished." in text:
                return "FINALIZADO"
        return "ERRO"


    def open_iped_log(self, proc: Process):
        path = Path(proc.output_folder) / "sinf.log"
        if path.exists():
            try:
                with path.open("r") as f:
                    lines = f.readlines()
                if "Check the log at" in lines[-1] and "ERROR!!!" in lines[-2]:
                    file = lines[-1].replace("Check the log at ", "").replace("\n", "")
                    path = Path(file)
                    if path.exists():
                        self.exec(['s-np', str(path)])
            except:
                self.exec(['s-np', str(path)])
