import uno
from pathlib import Path
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException
from subprocess import Popen
import time

def dictToProperties(dictionary): #normally I'd just import this
    """
    Utitlity to convert a dictionary to properties
    """
    props = []
    for key in dictionary:
        prop = PropertyValue()
        prop.Name = key
        prop.Value = dictionary[key]
        props.append(prop)
    return tuple(props)


class UnoHandler:

    def __init__(self) -> None:
        self.desktop = None

    def connect(self):
        while True:
            try:
                localContext = uno.getComponentContext()
                resolver = localContext.ServiceManager.createInstanceWithContext(
                    "com.sun.star.bridge.UnoUrlResolver", localContext)
                ctx = resolver.resolve(
                    "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
                smgr = ctx.ServiceManager
                self.desktop = smgr.createInstanceWithContext(
                    "com.sun.star.frame.Desktop", ctx)
                break
            except NoConnectException:
                Popen(['s-loffice'])
                time.sleep(0.5)
                

    def open_doc(self, path, hidden=False):
        path = Path(path)
        self.desktop.loadComponentFromURL(path.as_uri() ,"_blank",0, dictToProperties({"Hidden": hidden}))