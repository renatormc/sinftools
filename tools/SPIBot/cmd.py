import click
import subprocess
import config
import shutil
import os
from database import *
from replacer import adjust_timestamp

windows_path = os.getenv("PATH")
adb_folder = config.sinftools_dir / "extras/ADB"
os.environ['PATH'] = f"{adb_folder};{windows_path}"

os.system("where adb")

@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option("--app", type=click.Choice(['spi', 'extractor']), default='extractor')
def install(app):
    apk = config.app_dir / \
        "EXTRATOR_0.4.apk" if app == 'extractor' else config.app_dir / 'spitools-1.2.apk'
    print(f"Instalando {apk.name}")
    args = ['adb', 'install', str(apk)]
    subprocess.run(args)


@cli.command()
def extract():
    shutil.copy(config.app_dir / "bot.py", "bot.py")
    shutil.copy(config.app_dir / "extrair.py", "extrair.py")
    shutil.copy(config.app_dir / "database.py", "database.py")
    args = ['s-idlex', "extrair.py"]
    subprocess.run(args)

@cli.command()
def apk():
    shutil.copy(config.app_dir / "EXTRATOR_0.4.apk", "EXTRATOR_0.4.apk")
    shutil.copy(config.app_dir / "EXTRATOR_0.4.apk", 'spitools-1.2.apk')


@cli.command()
def log():
    chats = get_not_extracted()
    if chats:
        print("\nCHATS NÃO EXTRAIDOS: ")
        for i, chat in enumerate(chats):
            print(f"{i} - {chat.name}")
    chats = get_extracted()
    if chats:
        print("\nCHATS EXTRAIDOS: ")
        for i, chat in enumerate(chats):
            print(f"{i} - {chat.name}")

@cli.command()
def media():
    os.system("s-adb pull /sdcard/Whatsapp/Media Media")


@cli.command("adjust-timestamp")
def adjust_timestamp_():
    adjust_timestamp()

if __name__ == '__main__':
    cli(obj={})
