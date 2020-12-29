from odt_handler import OdtHandler
from uno_handler import UnoHandler

handler = UnoHandler()
handler.connect()
handler.open_doc("/media/renato/linux_data/temp/laudo.odt")
handler.pos_process()
handler.save_close()

# handler = OdtHandler("generico", folder="/media/renato/linux_data/temp")


# handler.render({'rg': 123, 'ano': 2020})

# import uno

# localContext = uno.getComponentContext()
# resolver = localContext.ServiceManager.createInstanceWithContext(
#                 "com.sun.star.bridge.UnoUrlResolver", localContext )
# ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
# smgr = ctx.ServiceManager
# desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)
# doc = desktop.getCurrentComponent()
# text = doc.Text
# cursor = text.createTextCursor()
# text.insertString( cursor, "The first line in the newly created text document.\n", 0 )