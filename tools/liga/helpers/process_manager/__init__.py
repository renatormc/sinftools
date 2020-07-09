from models import *
from helpers.database import filter_depends_on
import subprocess
import shlex
import psutil
from datetime import datetime, timedelta
import config
import time
from pathlib import Path
import os
import shutil
import stat
import errno
from sqlalchemy import or_, and_
# import sinf.servers.com as servers_com
from helpers.logger import logging
from sinfbot.helpers import bot_send_message


class ProcessManager:

    def __init__(self, db_session):
        super(ProcessManager, self).__init__()
        self.paused = False
        self.db_session = db_session

    def exec(self, args):
        p = subprocess.Popen(args)

    def edit_process(self, data_form, proc=None):
        process = proc or Process()
        process.script = data_form['script']
        process.perito = data_form['perito']
        process.type = data_form['type']
        if not proc:
            process.status = "ADICIONADO"
        self.db_session.add(process)
        self.db_session.commit()
        self.check_process()

    def queue(self, proc: Process):
        proc.status = "AGUARDANDO"
        proc.start_waiting = datetime.now()
        proc.delete_output_files()
        self.db_session.add(proc)
        self.db_session.commit()
        self.check_process()

    def get_args(self, proc: Process):

        # path = config.app_dir / "helpers/process_manager/run.ps1"
        path = config.app_dir / "helpers/process_manager/run.bat"
        args = ["cmd", "/K", str(path), proc.script]
        # args = ['powershell', '-windowstyle', 'Hidden', '-file', str(path), proc.script]
        # args = ['powershell', '-file', str(path), proc.script]
        return args

    def init_process(self, proc: Process):
        if self.is_queue_blocked():
            return
        try:
            proc.generate_output_filenames()
            args = self.get_args(proc)
            stdout_file = Path(proc.stdout)
            stderr_file = Path(proc.stderr)
            with stdout_file.open("w") as fstdout:
                with stderr_file.open("w") as fstderr:
                    p = subprocess.Popen(args, stdout=fstdout, stderr=fstderr)

            proc.pid = p.pid
            p = psutil.Process(proc.pid)
            proc.start = datetime.fromtimestamp(p._create_time)
            proc.finish = None
            proc.status = "PROCESSANDO"
            self.db_session.add(proc)
            self.db_session.commit()
        except Exception as e:
            logging.error(str(e))
            proc.status = "ERRO"
            self.db_session.add(proc)
            self.db_session.commit()

    def cancel_process(self, proc: Process):
        self.kill_process(proc)
        proc.status = "CANCELADO"
        self.db_session.add(proc)
        self.db_session.commit()

    def kill_process(self, proc):
        if not proc.pid:
            return
        try:
            p = psutil.Process(proc.pid)
            create_time = datetime.fromtimestamp(p._create_time)
            if create_time == proc.start:
                subprocess.check_output(
                    ["taskkill", "/F", "/T", "/IM", str(proc.pid)])
                # p.kill()
                self.check_process()
        except psutil.NoSuchProcess:
            print("Processo não existente")

    def startup_iped_procs(self):

        n = self.db_session.query(Process).filter(
            Process.status == 'PROCESSANDO', Process.type == "IPED").count()
        if n == 0:
            proc = self.db_session.query(Process).filter(Process.status == 'AGUARDANDO', Process.type == "IPED").order_by(
                Process.start_waiting.asc()).first()

            if proc:
                print(f"Iniciando {proc}")
                self.init_process(proc)

    def filter_ready_processes(self, query):
        query = query.filter(~Process.dependencies_as_blocked.any(
            Dependecy.blocker.has(Process.status != "FINALIZADO")
        ))
        return query

    def startup_image_procs(self):
        n = self.db_session.query(Process).filter(
            Process.status == 'PROCESSANDO', Process.type == "Imagem").count()
        if n == 0:
            query = self.db_session.query(Process).filter(
                Process.status == 'AGUARDANDO', Process.type == "Imagem")
            proc = query.order_by(
                Process.start_waiting.asc()).first()
            if proc:
                self.init_process(proc)

    def startup_synkdir_procs(self):
        n = self.db_session.query(Process).filter(Process.status == 'PROCESSANDO',
                                                  Process.type == "Sincronização de pastas").count()
        if n == 0:
            query = self.db_session.query(Process).filter(Process.status == 'AGUARDANDO',
                                                          Process.type == "Sincronização de pastas")
            proc = query.order_by(
                Process.start_waiting.asc()).first()
            if proc:
                self.init_process(proc)

    def startup_other_procs(self):
        query = self.db_session.query(Process).filter(
            Process.status == 'AGUARDANDO', Process.type == "Outro")

        query = query.order_by(Process.start_waiting.asc())
        for proc in query.all():
            self.init_process(proc)

    def check_process(self):
        print("Checando")
        # Checar se algum que estava processando finalizou ou deu erro
        procs = self.db_session.query(Process).filter(Process.status == "PROCESSANDO").order_by(
            Process.start_waiting.asc()).all()

        for proc in procs:
            try:
                p = psutil.Process(proc.pid)
                if abs(proc.start - datetime.fromtimestamp(p._create_time)) > timedelta(minutes=1):
                # if proc.start != datetime.fromtimestamp(p._create_time):
                    raise psutil.NoSuchProcess(p.pid)
            except psutil.NoSuchProcess:
                proc.status = self.check_process_finished(proc)
                if proc.telegram:
                    try:
                        proc_name = Path(proc.script).stem
                        if proc.status == "FINALIZADO":
                            bot_send_message(proc.perito,  f"Seu processo \"{proc_name}\" finalizou com sucesso!")
                        if proc.status == "ERRO":
                            bot_send_message(proc.perito, f"Infelizmente houve um erro no seu processo \"{proc_name}\"")
                    except:
                        pass
                proc.finish = datetime.now()
                self.db_session.add(proc)
        self.db_session.commit()

        # Bloquear processos com dependencias
        query = self.db_session.query(Process).filter(Process.status == "AGUARDANDO", Process.dependencies_as_blocked.any(
            Dependecy.blocker.has(~Process.status.in_(['FINALIZADO', 'ERRO']))
        ))
        for proc in query.all():
            proc.status = "AGUARDANDO DEPENDÊNCIA"
            self.db_session.add(proc)

        # desbloquear bloqueados
        query = self.db_session.query(Process).filter(Process.status == "AGUARDANDO DEPENDÊNCIA").filter(or_(
            ~Process.dependencies_as_blocked.any(
                Dependecy.blocker.has(Process.status != "FINALIZADO")
            ), ~Process.dependencies_as_blocked.any()))
        for proc in query.all():
            proc.status = "AGUARDANDO"
            self.db_session.add(proc)

        self.db_session.commit()

        # Verificar para mais quantos tem vaga e iniciar o processamento por ordem de chegada
        self.startup_iped_procs()
        self.startup_image_procs()
        self.startup_other_procs()
        self.startup_synkdir_procs()

    def check_process_finished(self, proc: Process):
        text = proc.get_output_tail()
        if "SINF: Processo finalizado com sucesso!" in text:
            return "FINALIZADO"
        return "ERRO"

    def set_blocking_user(self, user):
        if not user:
            print("ASDFFFFF")
            self.db_session.query(Document).filter(
                Document.key == "blocking_user").delete()
            self.db_session.commit()
            return
        doc = self.db_session.query(Document).filter(
            Document.key == "blocking_user").first()
        if not doc:
            doc = Document()
            doc.key = "blocking_user"
        doc.value = {
            'user': user,
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        print(doc)
        self.db_session.add(doc)
        self.db_session.commit()

    def get_blocking_user(self):
        doc = self.db_session.query(Document).filter(
            Document.key == "blocking_user").first()
        if doc:
            value = doc.value
            value['timestamp'] = datetime.strptime(
                value['timestamp'], "%d/%m/%Y %H:%M:%S")
            return value

    def is_queue_blocked(self):
        return self.db_session.query(Document).filter(Document.key == "blocking_user").count() > 0
