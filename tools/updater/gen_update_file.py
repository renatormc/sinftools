from pathlib import Path
import os
import click
from subprocess import Popen

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))
config_file = sinftools_dir / "var/config/updater.json"
tempfile = (app_dir / "temp/temp.ffs_gui")



@click.command()
@click.option('--directory', '-d', default=r'\\10.129.3.14\compartilhada\SOFTWARE\sinftools')
@click.option('--onlyextras', '-e', is_flag=True)
@click.option('--upload', '-u', is_flag=True)
def update(directory, onlyextras, upload):
    from_, to_ = ('%SINFTOOLS%', directory) if upload else (directory, '%SINFTOOLS%')
    template = "config_files/server2local_extras_template.ffs_gui" if onlyextras else "config_files/server2local_template.ffs_gui"
    text = (app_dir / template).read_text()
    text = text.replace("${fromFolder}", from_)
    text = text.replace("${toFolder}", to_)
    tempfile.write_text(text)
    Popen(['s-ffs', str(tempfile)])


if __name__ == '__main__':
    update()



