from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor, QIntValidator, QTextCursor, QKeySequence
from PyQt5.QtCore import QTimer, Qt
import sys
import os
import config
from database import db_session, init_db
from models import *
from helpers.process_manager import ProcessManager
from pathlib import Path
from datetime import datetime
import traceback
from .scheduler import Scheduler
from functools import partial
from .new_script_dialog import NewScriptDialog
from .script_dialog import ScriptDialog
import shutil
import subprocess
from helpers.logger import logging, get_log_tail
# from .servers.com import request_check_process
from sinf_requests import Requester
from helpers.user_manage import who_is_connected


class Window(QMainWindow):
    def __init__(self, standalone=False):
        QMainWindow.__init__(self)
        self.standalone = standalone
        self.column_map = {
            0: ('id', 'ID'),
            1: ('script', 'Script'),
            2: ('perito', "Perito"),
            3: ('type', "Tipo"),
            4: ('pid', 'PID'),
            5: ('start_waiting', 'Agendamento'),
            6: ('start', 'Inicio'),
            7: ('finish', 'Finalização'),
            8: ('dependencies_ids', 'Dependencias'),
            9: ('status', 'Status')
        }
        self.setup_ui()
        self.create_user_sinf()
        self.process_manager = ProcessManager(db_session)
        self.scheduler = Scheduler(parent=self, standalone=self.standalone)
        # self.scheduler.updated.connect(self.periodic)
        self.scheduler.start()
        self.connections()
        self.check_process()
        self.update_table()
        self.new_data_form = None
        self.proc_context_menu = None
        self.editing_proc = None
        self.pause = False
        self.current_process_console = None
        self.processes = {}
        self.create_reload_action()
        if not self.standalone:
            self.restart_fila_service()
        self.queue_blocked_ = False
        self.update_blocking_state()

    def create_user_sinf(self):
        user = db_session.query(User).filter_by(name="sinf").first()
        if not user:
            user = User()
            user.name = "sinf"
            db_session.add(user)
            db_session.commit()

    def check_process(self):
        if self.standalone:
            self.process_manager.check_process()
        else:
            try:
                req = Requester(config.SINF_TOKEN)
                url = f"http://localhost:{config.service_port}/check-process"
                req.get(url, timeout=5)
            except Exception as e:
                logging.error(str(e))

    def restart_fila_service(self):
        os.system("s-nssm restart fila")

    def create_reload_action(self):
        shortcut = QShortcut(QKeySequence("F5"), self)
        shortcut.activated.connect(self.f5_pressed)
        shortcut.setEnabled(True)

    def f5_pressed(self):
        self.check_process()
        self.update_table()
        self.update_console()
        print("F5")

    def convert_data(self, value):
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M:%S")
        if isinstance(value, int):
            return str(value)
        return value

    def setup_ui(self):
        self.setWindowIcon(
            QIcon(f"{config.app_dir}\\fila\\resources\\icone.png"))
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

        lbl = QLabel(
            "Utilize F5 para atualizar e dois cliques na tabela para editar o escript.")
        lbl.setStyleSheet("color: red;font-size: 10pt;")
        self.main_layout.addWidget(lbl)
        self.tbw_process = QTableWidget()
        self.tbw_process.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tbw_process.setSelectionBehavior(QAbstractItemView.SelectRows)
        n_columns = len(self.column_map.keys())
        self.tbw_process.setColumnCount(n_columns)
        self.tbw_process.setHorizontalHeaderLabels(
            [item[1] for item in self.column_map.values()])
        header = self.tbw_process.horizontalHeader()
        for i in range(n_columns):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.main_layout.addWidget(self.tbw_process)

        # slot para mostrar ou ocultar a mensagem
        self.block_message_layout = QHBoxLayout()
        self.lbl_block_message = None
        self.main_layout.addLayout(self.block_message_layout)

        self.create_menus()
        self.create_console()

    def create_menus(self):
        menubar = self.menuBar()
        self.file_menu = menubar.addMenu('&Arquivo')
        self.new_script_action = menubar.addAction("Criar novo")
        self.open_sqlite_action = QAction("Abrir sqlite")
        self.file_menu.addAction(self.open_sqlite_action)
        self.open_logfile_action = QAction("Abrir arquivo de log")
        self.file_menu.addAction(self.open_logfile_action)
        self.toggle_blocking_queue_action = QAction(
            "Bloquear/Desbloquear fila")
        self.file_menu.addAction(self.toggle_blocking_queue_action)
        self.open_config_action = QAction("Configurações")
        self.file_menu.addAction(self.open_config_action)

    def create_console(self):

        self.txe_stdout = QTextEdit()
        self.txe_stdout.setStyleSheet(
            "background-color: rgb(64,64,64); color: white; font-size: 10pt;")
        self.txe_stdout.setReadOnly(True)

        self.txe_stderr = QTextEdit()
        self.txe_stderr.setStyleSheet(
            "background-color: rgb(64,64,64); color: white; font-size: 10pt;")
        self.txe_stderr.setReadOnly(True)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.txe_stdout, "STDOUT")
        self.tabs.addTab(self.txe_stderr, "STDERR")
        self.main_layout.addWidget(self.tabs)

    # def periodic(self):
    #     # self.check_process()
    #     self.update_table()

    def open_sqlite(self):
        self.process_manager.exec(['s-dbb', str(config.sqlite_path)])

    def open_config(self):
        self.process_manager.exec(['s-np', str(config.configpath)])

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        cancel_action = contextMenu.addAction("Cancelar")
        queue_action = contextMenu.addAction("Incluir na fila")
        remove_action = contextMenu.addAction("Remover")
        edit_script_action = contextMenu.addAction("Editar script")
        open_stdout_file_action = contextMenu.addAction(
            "Abrir arquivo de console")
        open_stderr_file_action = contextMenu.addAction(
            "Abrir arquivo de erros")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        self.proc_context_menu = self.get_selected_proc()
        if action == cancel_action:
            self.cancel()
        elif action == queue_action:
            self.queue()
        elif action == remove_action:
            self.remove()
        elif action == edit_script_action:
            self.edit_process()
        elif action == open_stdout_file_action:
            self.open_stdout_file()
        elif action == open_stderr_file_action:
            self.open_stderr_file()

    def set_block_message(self, message):
        if message:
            self.lbl_block_message = QLabel(message)
            self.lbl_block_message.setAlignment(Qt.AlignCenter)
            self.lbl_block_message.setStyleSheet(
                "color: red; font-size: 20pt;")
            self.block_message_layout.addWidget(self.lbl_block_message)
        elif self.lbl_block_message is not None:
            self.block_message_layout.removeWidget(self.lbl_block_message)
            self.lbl_block_message.deleteLater()
            self.lbl_block_message = None

    def update_blocking_state(self):
        pm = ProcessManager(db_session)
        user = pm.get_blocking_user()
        if user:
            timestamp_str = user['timestamp'].strftime("%d/%m/%Y %H:%M:%S")
            self.set_block_message(
                f"Fila bloqueada por {user['user']} desde {timestamp_str}")
        else:
            self.set_block_message(None)

    def toggle_blocking_queue(self):
        pm = ProcessManager(db_session)
        user = pm.get_blocking_user()
        if user:
            pm.set_blocking_user(None)
        else:
            who = who_is_connected()
            if who and who['name'] != "Alguém":
                pm.set_blocking_user(who['name'])
            else:
                users = db_session.query(User).order_by(User.name).all()
                items = [user.name for user in users]
                text, okPressed = QInputDialog.getItem(self, "Perito",
                                                       "Selecione seu nome na lista", items, 0, False)
                if okPressed:
                    if len(text.strip()) < 4:
                        self.show_error(
                            "O nome precisa ter no mínimo 4 caracteres")
                        return
                    pm.set_blocking_user(text)
        self.update_blocking_state()

    def get_selected_proc(self) -> Process:
        i = self.tbw_process.currentRow()
        try:
            id = self.tbw_process.item(i, 0).data(Qt.UserRole)
            return db_session.query(Process).get(id)
        except:
            pass

    def tail_output_file(self):
        try:
            if self.proc_context_menu:
                self.current_process_console = self.proc_context_menu
                self.update_console()
        except Exception as e:
            self.show_error(e)

    def update_console(self):
        try:
            process = self.get_selected_proc()
            if process:
                text = process.get_output_tail()
                self.txe_stdout.setPlainText(text)
                cursor = self.txe_stdout.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.txe_stdout.setTextCursor(cursor)

                text = process.get_output_tail(stderr=True)
                self.txe_stderr.setPlainText(text)
                cursor = self.txe_stderr.textCursor()
                cursor.movePosition(QTextCursor.End)
                self.txe_stderr.setTextCursor(cursor)

        except Exception as e:
            logging.error(str(e))

    def open_stdout_file(self):
        try:
            if self.proc_context_menu:
                self.process_manager.exec(
                    ['s-np', str(self.proc_context_menu.stdout)])
        except Exception as e:
            self.show_error(e)

    def open_stderr_file(self):
        try:
            if self.proc_context_menu:
                self.process_manager.exec(
                    ['s-np', str(self.proc_context_menu.stderr)])
        except Exception as e:
            self.show_error(e)

    def edit_process(self):
        try:
            proc = self.get_selected_proc()
            if proc:
                dialog = ScriptDialog(proc)
                dialog.exec_()
        except Exception as e:
            self.show_error(e)

    def cancel(self):
        try:
            if self.proc_context_menu:
                self.process_manager.cancel_process(self.proc_context_menu)
        except Exception as e:
            self.show_error(e)

    def queue(self):
        try:
            if self.proc_context_menu:
                self.process_manager.queue(self.proc_context_menu)
                self.check_process()
        except Exception as e:
            self.show_error(e)

    def remove(self):
        try:
            if self.proc_context_menu:
                db_session.delete(self.proc_context_menu)
                db_session.commit()
                self.process_manager.kill_process(self.proc_context_menu)
        except Exception as e:
            self.show_error(e)

    def __get_process_by_row(self, i, onlyid=False):
        item = self.tbw_process.item(i, 0)
        id = item.data(Qt.UserRole)
        if onlyid:
            return id
        return db_session.query(Process).get(id)

    def __add_item_table(self, p, i):
        for key, value in self.column_map.items():
            item = QTableWidgetItem(self.convert_data(getattr(p, value[0])))
            item.setData(Qt.UserRole, p.id)
            # item.setFlags(Qt.ItemIsSelectable)
            if p.status == "ERRO":
                item.setBackground(QColor(255, 182, 182))
            elif p.status == "FINALIZADO":
                item.setBackground(QColor(182, 255, 214))
            elif p.status == "PROCESSANDO":
                item.setBackground(QColor(255, 246, 182))
                # self.set_color_row(i, QColor(125, 125, 125))
            self.tbw_process.setItem(i, key, item)

    def update_table_worker(self, raise_except=False):
        try:
            print("Atualizando tabela")
            processes_rows = {self.tbw_process.item(i, 0).data(
                Qt.UserRole): i for i in range(self.tbw_process.rowCount())}
            procs = db_session.query(Process).order_by(
                Process.start_waiting.asc()).all()
            for proc in procs:

                try:
                    # Atualizar existente
                    row = processes_rows[proc.id]
                    self.__add_item_table(proc, row)
                    del processes_rows[proc.id]
                except KeyError:
                    # Adicionar novo
                    row = self.tbw_process.rowCount()
                    self.tbw_process.insertRow(row)
                    self.__add_item_table(proc, row)

            # Deletar o que não existem mais no banco
            rows = list(processes_rows.values())
            if rows:
                rows.sort(reverse=True)
                for i in rows:
                    self.tbw_process.removeRow(i)
            db_session.remove()
        except Exception as e:
            if raise_except:
                raise e

    def update_table(self):
        try:
            self.scheduler.periodic()
            # self.update_table_worker(raise_except=True)
        except Exception as e:
            self.show_error(e)

    def get_error_string(self, e, tb=True):
        ex_type, ex_value, ex_traceback = sys.exc_info()
        if tb:
            trace_back = traceback.extract_tb(ex_traceback)
            stack_trace = list()
            for trace in trace_back:
                stack_trace.append(
                    "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        text = "Exception type : %s " % ex_type.__name__
        text += "\nException message : %s" % ex_value
        if tb:
            text += "\n".join(stack_trace)
        return text

    def show_error(self, e):
        if isinstance(e, str):
            text = e
        else:
            text = self.get_error_string(e, tb=True)
        msg = QMessageBox()
        msg.setWindowIcon(
            QIcon('{}\\fila\\resources\\icone.png'.format(config.app_dir)))
        msg.setWindowTitle("Erro")
        msg.setText(text)
        print(text)
        msg.exec()

    def show_message(self, message, title="Mensagem"):
        msg = QMessageBox()
        msg.setWindowIcon(
            QIcon('{}\\fila\\resources\\icone.png'.format(config.app_dir)))
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def pause(self):
        self.paused = not self.paused

    def create_new_script(self):
        dialog = NewScriptDialog()
        dialog.exec_()
        if dialog.ok_clicked:
            name = dialog.led_name.displayText()
            perito = dialog.cbx_perito.currentText()
            type = dialog.cbx_template.currentText()
            script = config.fila_scripts_template[type]['script']
            to_script = config.scripts_folder / f"{name}.bat"
            i = 1
            while to_script.exists():
                to_script = config.scripts_folder / f"{name}_{i}.bat"
                i += 1
            from_script = config.app_dir / f"cmdtool/scripts/{script}"
            shutil.copy(from_script, to_script)
            process = Process()
            process.script = str(to_script.absolute())
            process.perito = perito
            process.type = config.fila_scripts_template[type]['process_type']
            process.status = "ADICIONADO"
            db_session.add(process)
            db_session.commit()
            script_dialog = ScriptDialog(process, initial=True)
            script_dialog.exec_()

    def open_logfile(self):
        self.process_manager.exec(['s-np', str(config.logfile)])

    def open_config_file(self):
        path = config.sinftools_dir / "var/config/servers_config.yaml"
        self.process_manager.exec(['s-np', str(path)])

    def connections(self):
        self.open_sqlite_action.triggered.connect(self.open_sqlite)
        self.open_logfile_action.triggered.connect(self.open_logfile)
        self.toggle_blocking_queue_action.triggered.connect(
            self.toggle_blocking_queue)
        self.open_config_action.triggered.connect(self.open_config_file)
        # self.blo.triggered.connect(self.open_logfile)
        self.tbw_process.selectionModel().currentRowChanged.connect(self.update_console)
        self.tbw_process.clicked.connect(self.update_console)
        self.new_script_action.triggered.connect(self.create_new_script)
        self.tbw_process.doubleClicked.connect(self.edit_process)


if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    standalone = len(sys.argv) > 1 and sys.argv[1] == 'standalone'
    w = Window(standalone=standalone)
    w.setGeometry(500, 50, 1300, 800)
    w.setWindowTitle(f"Gerenciador de fila de processos")
    w.show()
    sys.exit(app.exec_())
