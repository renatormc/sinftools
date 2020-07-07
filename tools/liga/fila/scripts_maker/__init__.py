from ..scripts_maker.iped_process import IpedProcessDialog
from ..scripts_maker.image_process import ImageProcessDialog

def get_maker(process):
    if process.type == 'IPED':
        return IpedProcessDialog(process)
    elif process.type == 'Imagem':
        return ImageProcessDialog(process)
    

def has_maker(process):
    return process.type in ['IPED', 'Imagem']