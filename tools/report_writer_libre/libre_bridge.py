import subprocess
import config

def run(*params):
    args = [config.python_libre]
    process = Popen(, stdout=PIPE)
    process.communicate()
    exit_code = process.wait()

def test():
    process = Popen(shlex.split(cmd), stdout=PIPE)
    process.communicate()
    exit_code = process.wait()