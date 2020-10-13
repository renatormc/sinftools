import socket
import uno
from com.sun.star.awt import Size
from com.sun.star.text.TextContentAnchorType import AS_CHARACTER
from com.sun.star.awt import Point
from com.sun.star.connection import NoConnectException
from handler import helpers
import config
import re
from pathlib import Path
import json
from handler import constants
from com.sun.star.beans import PropertyValue
import context_store
from handler.pos_processor import PosProcessor
import subprocess
import os
import time


class NameAnalyzer:
    def __init__(self):
        self.reg =  re.compile(r'((^[A-Za-z]+)(\d+))(?:[\d\.\-]+)?(?:_(\d+))?$')

    def analise_name(self, name):
        res = self.reg.search(name)
        if not res:
            return
        ret = {
            'obj_name': res.group(1),
            'alias': res.group(2),
            'obj_number': res.group(3),
            'pic_seq': res.group(4)
        }
        if ret['obj_number'] is not None:
            return ret


class Handler:
    def __init__(self, workdir="."):
        self.workdir = Path(workdir)

    def connect(self):
        localContext = uno.getComponentContext()
        self.resolver = localContext.ServiceManager.createInstanceWithContext(
            "com.sun.star.bridge.UnoUrlResolver", localContext)
        try:
            self.ctx = self.resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        except NoConnectException:
            vbs_file = config.app_dir / "scripts/windows/_Libreoffice.vbs"
            if os.name == "nt":
                os.system(str(vbs_file))
            else:
                subprocess.Popen(["soffice", "--accept='socket,host=0.0.0.0,port=2002;urp;StarOffice.Service'"])
            while True:
                try:
                    print("Tentando se conectar ao LibreOffice via socket")
                    self.ctx = self.resolver.resolve(
                        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
                    print("Conexão com LibreOffice efetuada")
                    break
                except NoConnectException:
                    time.sleep(0.5)

        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)

    def replace(self, var, value):
        doc = self.desktop.getCurrentComponent()
        replace = doc.createReplaceDescriptor()
        # replace.SearchRegularExpression = True
        replace.SearchString = f"#{var}#"
        # replace.ReplaceString =value
        selsFound = doc.findAll(replace)
        for selIndex in range(0, selsFound.getCount()):
            selFound = selsFound.getByIndex(selIndex)
            selFound.setString(value)

    def add_image(self, doc, path):
        path = uno.systemPathToFileUrl(path)
        vc = doc.getCurrentController().getViewCursor()
        draw_page = doc.DrawPage
        draw_page.set = vc.Start
        image = doc.createInstance('com.sun.star.drawing.GraphicObjectShape')
        image.GraphicURL = path
        draw_page.add(image)
        image.setSize(Size(75000, 5000))
        image.setPropertyValue('AnchorType', AS_CHARACTER)

    def find_variable(self, var, doc=None):
        if not doc:
            doc = self.desktop.getCurrentComponent()
        replace = doc.createReplaceDescriptor()
        replace.SearchRegularExpression = True
        reg = r'\{\{\s*$var\s*\}\}'.replace("$var", var)
        replace.SearchString = reg
        selsFound = doc.findAll(replace)
        return doc.findFirst(replace)
        # if selsFound:
        #     return selsFound.getByIndex(0)

    def create_table(self, spot, n_rows, n_cols, doc=None):
        if not doc:
            doc = self.desktop.getCurrentComponent()
        if isinstance(spot, str):
            spot = self.find_variable(spot, doc=doc)
        if spot:
            spot.setString("")
            table = doc.createInstance("com.sun.star.text.TextTable")
            table.initialize(n_rows, n_cols)
            spot.Text.insertTextContent(spot, table, 0)
            return table

    def image_in_table(self, table, path, width, height, cell, doc=None):
        if not doc:
            doc = self.desktop.getCurrentComponent()
        if table:
            tableText = None
            if isinstance(cell, str):
                tableText = table.getCellByName(cell)
            elif isinstance(cell, tuple):
                tableText = table.getCellByPosition(cell[1], cell[0])
            else:
                return
            img = doc.createInstance('com.sun.star.text.TextGraphicObject')
            path = Path(path).absolute()
            img.GraphicURL = path.as_uri()
            img.setPropertyValue('AnchorType', AS_CHARACTER)
            img.setSize(Size(width, height))
            tableText.insertTextContent(tableText, img, False)

    def pos_process(self, doc=None):
        open_doc = False
        pos_processor = PosProcessor()
        laudo_url = config.laudo_file.absolute().as_uri()
        if not doc:
            doc = self.desktop.loadComponentFromURL(
                laudo_url, "_blank", 0, helpers.dictToProperties({"Hidden": True, "ReadOnly": False}))
            open_doc = True
        try:
            reg = r'\[(.*)\((.{1,100}?)\)\]'
            replace = doc.createReplaceDescriptor()
            replace.SearchRegularExpression = True
            replace.SearchString = reg
            cur = doc.findFirst(replace)
            while cur:
                text = cur.getString()
                res = re.search(reg, text)
                funcname = res.group(1).strip()
                params = res.group(2).strip()

                ok = pos_processor.exec(funcname, doc, cur, params)
                if not ok:
                    print(f"Pos Processing function _{funcname}_ not found")
                cur = doc.findNext(cur.End, replace)
            doc.storeToURL(laudo_url, ())
        finally:
            if open_doc:
                doc.close(True)

    def replace_vars(self, doc=None):
        if not doc:
            doc = self.desktop.getCurrentComponent()
        vars = self.get_vars()
        reg = r'\{\{\s*(\S{1,15}?)\s*\}\}'
        for key, value in vars.items():
            replace = doc.createReplaceDescriptor()
            replace.SearchRegularExpression = True
            replace.SearchString = reg
            selsFound = doc.findAll(replace)
            for i in range(0, selsFound.getCount()):
                selFound = selsFound.getByIndex(i)
                res = re.search(reg, selFound.getString())

                try:
                    key = res.group(1)
                    selFound.setString(vars[key])
                except (AttributeError, KeyError) as e:
                    pass

    def compile(self, hidden=True):
        doc = self.desktop.getCurrentComponent()
        odt_url, pdf_url = helpers.compile_path(doc)
        doc.storeToURL(odt_url, ())
        doc = self.desktop.loadComponentFromURL(
            odt_url, "_blank", 0, helpers.dictToProperties({"Hidden": hidden}))
        try:
            self.replace_numbers(doc)
            self.replace_vars(doc=doc)
            doc.store()
            helpers.save_pdf(doc, pdf_url)
        finally:
            doc.close(True)

    def get_vars(self):
        vars = {}
        path = config.data_file.absolute()
        data_url = path.as_uri()
        calc = self.desktop.loadComponentFromURL(
            data_url, "_blank", 0, helpers.dictToProperties({"Hidden": True, "ReadOnly": True}))

        try:
            # sheet = calc.Sheets[0]
            sheet = calc.Sheets["Variables"]
            n_rows = sheet.getRows().getCount()
            for i in range(1, n_rows):
                name = sheet.getCellByPosition(0, i).getString().strip()
                if not name:
                    break
                type_ = sheet.getCellByPosition(2, i).getString().strip()
                cell = sheet.getCellByPosition(1, i)
                vars[name] = cell.getString()
        finally:
            calc.close(False)
        return vars

    def get_objects_info(self):
        objs = []
        path = config.data_file.absolute()
        pics_folder = config.pics_folder.absolute()
        data_url = path.as_uri()
        calc = self.desktop.loadComponentFromURL(
            data_url, "_blank", 0, helpers.dictToProperties({"Hidden": True, "ReadOnly": True}))
        try:
            sheet = calc.Sheets["Objects"]
            n_rows = sheet.getRows().getCount()
            for i in range(1, n_rows):
                name = sheet.getCellByPosition(0, i).getString().strip()
                type_ = sheet.getCellByPosition(1, i).getString().strip()
                if not name:
                    break
                pics = sheet.getCellByPosition(2, i).getString().split(",")
                # pics = [(pics_folder / pic).as_uri() for pic in pics]
                objs.append({'name': name, 'type': type_, 'pics': pics})
        finally:
            pass
            # calc.close(False)
        return objs

    def get_objects_from_pics(self):
        objects = {}
        analyzer = NameAnalyzer()
        for entry in config.pics_folder.iterdir():
            if entry.name.startswith("_"):
                continue
            res = analyzer.analise_name(entry.stem)
            if not res:
                raise Exception(f"A foto {entry.name} não está nomeada no padrão exigido")
            
            # res = reg.search(entry.name)
            obj = res['obj_name']
            try:
                objects[obj]['pics'].append(entry.name)
            except KeyError:
                objects[obj] = {'number': res['obj_number'], 'pics': [entry.name]}
        items = []
        for key, value in objects.items():
            objects[key]['pics'].sort()
            items.append(
                {'name': key, 'number': value['number'], 'pics': value['pics']})
        items.sort(key=lambda x: x['number'])
        return items

    def insert_pics2(self):
        pics = self.get_pics()
        n_rows = len(pics) + 1
        table = self.create_table("table_pics", n_rows, 3)
        for i, item in enumerate(pics):
            row = i + 1
            path = Path(item['pic']).absolute()
            table.getCellByPosition(0, row).setString(item['name'])
            table.getCellByPosition(1, row).setString(item['pic'].name)
            self.image_in_table(table, path, 2000, 2000, (row, 2))
            table.getCellByPosition(3, row).setString(
                f"Evidência {item['number']}")

    def scan_pics(self):
        # calc = self.desktop.getCurrentComponent()
        path = self.workdir / "data.ods"
        odt_url = path.absolute().as_uri()
        calc = self.desktop.loadComponentFromURL(
            odt_url, "_default", 0, helpers.dictToProperties({"Hidden": False}))
        try:
            objs = self.get_objects_from_pics()
            n_rows = len(objs) + 1
            sheet = calc.Sheets['Objects']
            for i, obj in enumerate(objs):
                row = i + 1
                sheet.getCellByPosition(0, row).setString(
                    f"Evidência {obj['number']}")
                sheet.getCellByPosition(1, row).setString("Celular")
                pics = ",".join(obj['pics'])
                sheet.getCellByPosition(2, row).setString(pics)
            calc.store()
        finally:
            # calc.close(True)
            pass

    def insert_pics(self, cur, pics, doc=None):
        n = len(pics)
        rest = n % 2
        n_rows = int(n/2)
        if rest != 0:
            n_rows += 1
        self.create_table(cur, n_rows, 2, doc=doc)

    def write_objects(self):
        doc = self.desktop.getCurrentComponent()
        cur = self.find_variable("objetos", doc=doc)
        if cur:
            cur.setString("")
            objs = self.get_objects_info()
            for obj in objs:
                doc.Text.insertString(cur, obj['name'], 0)
                doc.Text.insertString(cur, "\n", 0)
                path = config.app_dir / f"templates/{obj['type']}.odt"
                print(path)
                if path.exists():
                    cur.gotoEnd(False)

                    cur.insertDocumentFromURL(path.as_uri(), ())
                cur.gotoEnd(False)
                doc.Text.insertString(cur, "\n", 0)
                self.insert_pics(cur, obj['pics'], doc=doc)

    def read_calc(self):
        context = self.get_vars()
        context['objects'] = self.get_objects_info()
        context_store.save_context(context)

    def print_all(self, printer_name, n_copies=2, print_media=False):
        doc = self.desktop.getCurrentComponent()
        printer = doc.getPrinter()
        printer[0].Value = printer_name
        doc.setPrinter(printer)

        # Imprimir capa
        path = self.workdir / "data/capa.odt"
        odt_url = path.absolute().as_uri()
        doc_capa = self.desktop.loadComponentFromURL(
            odt_url, "_blank", 0, helpers.dictToProperties({"Hidden": True}))
        outProps = (
            PropertyValue("Wait", 0, True, 0),
            PropertyValue("DuplexMode", 0, constants.DuplexMode.OFF, 0),
            PropertyValue("CopyCount", 0, 1, 0),
        )
        doc_capa.print(outProps)
        doc_capa.close(True)

        # Imprimir laudo
        outProps = (
            PropertyValue("Wait", 0, True, 0),
            PropertyValue("DuplexMode", 0, constants.DuplexMode.LONGEDGE, 0),
            PropertyValue("CopyCount", 0, n_copies, 0),
        )
        doc.print(outProps)

        path_pdf = Path("./data/laudo.pdf").absolute()
        helpers.save_pdf(doc, path_pdf.as_uri())

        if print_media:
            # Imprimir anexo mídias
            path = self.workdir / "data/midia.odt"
            odt_url = path.absolute().as_uri()
            doc_midia = self.desktop.loadComponentFromURL(
                odt_url, "_blank", 0, helpers.dictToProperties({"Hidden": True}))
            outProps = (
                PropertyValue("Wait", 0, True, 0),
                PropertyValue("DuplexMode", 0, constants.DuplexMode.OFF, 0),
                PropertyValue("CopyCount", 0, n_copies, 0),
            )
            doc_midia.print(outProps)
            doc_midia.close(True)
