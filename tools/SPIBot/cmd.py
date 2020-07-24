import click
import subprocess
import config
import shutil
import os


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
    script = config.app_dir / "SPIWhatsAppExtracaoManual.py"
    shutil.copy(script, "SPIWhatsAppExtracaoManual.py")
    args = ['s-idlex', "SPIWhatsAppExtracaoManual.py"]
    subprocess.run(args)

@cli.command()
def apk():
    shutil.copy(config.app_dir / "EXTRATOR_0.4.apk", "EXTRATOR_0.4.apk")
    shutil.copy(config.app_dir / "EXTRATOR_0.4.apk", 'spitools-1.2.apk')


if __name__ == '__main__':
    cli(obj={})
