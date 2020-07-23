import click
import subprocess
import config
import shutil

@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def install():
    apk = config.app_dir / "EXTRATOR_0.4.apk"
    args = ['adb', 'install', str(apk)]
    subprocess.run(args)

@cli.command()
def extract():
    script = config.app_dir / "SPIWhatsAppExtracaoManual.py"
    shutil.copy(script, "SPIWhatsAppExtracaoManual.py")
    args = ['s-idlex', "SPIWhatsAppExtracaoManual.py"]
    subprocess.run(args)


if __name__ == '__main__':
    cli(obj={})