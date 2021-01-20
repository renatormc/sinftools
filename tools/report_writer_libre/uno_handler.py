import uno
from pathlib import Path
from com.sun.star.beans import PropertyValue
from com.sun.star.connection import NoConnectException
from com.sun.star.awt import Size
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from subprocess import Popen
import time
import re
from libre_helpers import *
import config
import constants


class UnoHandler:

    def __init__(self) -> None:
        self.desktop = None
        self.doc = None

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
                self.doc = self.desktop.getCurrentComponent()
                break
            except NoConnectException:
                Popen(['s-loffice'])
                time.sleep(0.5)

    def open_doc(self, path, hidden=False):
        path = Path(path)
        self.doc = self.desktop.loadComponentFromURL(
            path.absolute().as_uri(), "_blank", 0, dictToProperties({"Hidden": hidden}))

    def save_close(self):
        self.doc.storeToURL(self.doc.getURL(), ())
        self.doc.close(True)

    def close(self):
        self.doc.close(True)

    def __add_image(self, path, width, cur):
        path = Path(path).absolute()
        if not path.exists():
            print(f"File {path} not existent")
        img = self.doc.createInstance('com.sun.star.text.TextGraphicObject')
        img.GraphicURL = path.as_uri()
        img.setPropertyValue('AnchorType', AS_CHARACTER)
        width = width*100
        cur.setString("")
        cur.Text.insertTextContent(cur, img, False)
        alfa = width/img.Width
        height = int(alfa*img.Height)
        img.setSize(Size(width, height))

    def replace_action(self, action, args, cur):
        if action == "pic":
            self.__add_image(args[0], int(args[1]), cur)

    def pos_process(self):
        replace = self.doc.createReplaceDescriptor()
        replace.SearchRegularExpression = True
        reg = r'@(.{1,15}?)\((.{1,50}?)\)'
        replace.SearchString = reg
        selsFound = self.doc.findAll(replace)
        for i in range(0, selsFound.getCount()):
            selFound = selsFound.getByIndex(i)
            name = selFound.getString().strip()
            res = re.search(reg, name)
            action, args = res.group(1), res.group(2).split(",")
            args = [arg.strip() for arg in args]
            self.replace_action(action, args, selFound)

    def print(self, n=1, duplex=False):
        printer = self.doc.getPrinter()
        printer[0].Value = config.printer_name
        self.doc.setPrinter(printer)

        duplex_mode = constants.DuplexMode.LONGEDGE if duplex else constants.DuplexMode.OFF

        out_props = (
            PropertyValue("Wait", 0, True, 0),
            PropertyValue("DuplexMode", 0, duplex_mode, 0),
            PropertyValue("CopyCount", 0, n, 0),
        )

        self.doc.print(out_props)


    def save_pdf(self):
        url = self.doc.getURL()
        path = Path(url.replace("file://", ""))
        url = path.with_suffix(".pdf").as_uri()
        property = (PropertyValue( "FilterName" , 0, "writer_pdf_Export" , 0 ),)
        self.doc.storeToURL(url, property)
