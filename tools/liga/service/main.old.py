from nameko.rpc import rpc
from sinf.servers.models import *
from sinf.servers.database import db_session
from uteis import *
import subprocess
from schemas import ProcessSchema
import config
import requests
from helpers import print_for_pid
from process_manager import ProcessManager
from nameko.web.handlers import http


class ServersService:
    name = config.SERVICE_NAME

    @rpc
    def get_processes(self):
        processes = db_session.query(Process).order_by(Process.queue_order.asc(), Process.start_waiting.asc()).all()
        schema = ProcessSchema(many=True)
        return schema.dump(processes)
        
    @rpc
    def process(self, id):
        process = db_session.query(Process).get(id)
        schema = ProcessSchema()
        return schema.dump(process)

    @http('GET', '/someone-connected')
    def someone_connected(self, request):
        cmd = f"query session |findstr Ativo"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        output, err = p.communicate()
        p_status = p.wait()
        text = output.decode("utf-8")
        if "rdp-tcp" in text:
            return u"yes"
        return u"no"

    @rpc
    def progress(self, id):
        process = db_session.query(Process).get(id)
        pm = ProcessManager(db_session)
        pm.check_process()
        tempfile = None
        if process.status == "PROCESSANDO":
            path = print_for_pid(process.pid)
            if path and path.exists():
                files = {'file': path.open("rb")}
                url = f"{config.local_config['SINFWEB_URL']}/servers/upload-file"
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    tempfile = response.text
                else:
                    print(response.text)
        schema = ProcessSchema()
        return {
            'process': schema.dump(process),
            'tempfile': tempfile
        }

    @rpc
    def include_queue(self, id):
        process = db_session.query(Process).get(id)
        pm = ProcessManager(db_session)
        try:
            pm.queue(process)
        except Exception as e:
            return str(e)
        