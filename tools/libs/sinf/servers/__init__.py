from subprocess import Popen
import os
from sinf.servers import config
import subprocess

def quote(value):
    value = value.strip()
    if " " in value:
        return f"\"{value}\""
    return value


# def exec_cmd(args):
#     cmd = " ".join([quote(arg) for arg in args]
#                    ) if isinstance(args, list) else args
#     os.system(cmd)

def exec_cmd(args):
    CREATE_NO_WINDOW = 0x08000000
    subprocess.check_output(args, creationflags=CREATE_NO_WINDOW)
# def exec_cmd(args):
#     subprocess.check_output(args)


def iped_process(sources, output, profile):
    iped = config.iped_folder / "iped.jar"
    args = [
        "javaw",
        "-jar",
        str(iped),
        "-profile",
        profile,
        "-o",
        output,
        "--nogui"
    ]

    for source in sources:
        args.append("-d")
        args.append(source)
    exec_cmd(args)

def make_image(source, dest):
    args = [
        str(config.ftkimager),
        source,
        dest,
        "--e01",
        "--verify"
    ]
    exec_cmd(args)