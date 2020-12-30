from odt_handler import OdtHandler
from uno_handler import UnoHandler

# handler = OdtHandler("generico", folder="/media/renato/linux_data/temp")
# context = {'rg': 123, 'ano': 2020, 'pic1': {'path': '/home/renato/Pictures/Chaves.jpg',
#                                             'caption': "Chaves na 1"}, 'pic2': {'path': '/home/renato/Pictures/Chaves.jpg', 'caption': "Chaves na 2"}}
# handler.render(context)


handler = UnoHandler()
handler.connect()
handler.open_doc("/media/renato/linux_data/laudos/AA/laudo/data.ods")
vars = handler.read_vars()
print(vars)