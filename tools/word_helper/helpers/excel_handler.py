from pathlib import Path
import re
import win32com.client as win32
import win32com.client
import pythoncom
from helpers import get_nome_laudo


class ExcelHandler(object):
    def __init__(self):
        self.excel = None
        self._folder = Path(".")

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        self._folder = Path(value)

    @property
    def workbook_path(self):
        wb = self.excel.ActiveWorkbook
        if wb:
            return Path(wb.FullName)

    def connect_excel(self):
        pythoncom.CoInitialize()
        # self.excel = win32.gencache.EnsureDispatch('Excel.Application')
        # self.excel = win32com.client.Dispatch('Excel.Application')
        try:
            self.excel = win32com.client.GetActiveObject('Excel.Application')
        except:
            self.excel = win32com.client.Dispatch('Excel.Application')
            self.excel.Workbooks.Open(str((Path(".") / "data.xlsx").absolute()))
        if not self.excel:
            raise Exception("Não foi possível se conectar ao Excel")
        self.excel.Visible = True
        # exit()

    def analise_pics(self):
        objects = {}
        for entry in (self.folder / "fotos").iterdir():
            reg = re.compile(r'((^[A-Za-z]+)(\d+)).*')
            res = reg.search(entry.name)
            obj = res.group(1).upper()
            try:
                objects[obj]['pics'].append(str(entry))
            except KeyError:
                objects[obj] = {'number': int(res.group(3)), 'pics': [str(entry)]}
                # objects.sort(key=lambda x: x['number'])
        items = []
        for key, value in objects.items():
            for pic in value['pics']:
                items.append({'name': key, 'number': value['number'], 'pic': pic})
        items.sort(key=lambda x: x['number'])
        return items

    def write_pics_sheet(self):
        self.connect_excel()
        wb = self.excel.ActiveWorkbook
        ws = wb.Worksheets("objetos")

        # Clear
        last_row = ws.Cells(ws.Rows.Count, "A").End(-4162).Row
        for i in range(2, last_row + 1):
            rgn = ws.Range(f"A{i}:Z{i}")
            rgn.Clear()
        for pic in ws.Pictures():
            pic.Delete()

        i = 2
        for item in self.analise_pics():
            ws.Rows(i).RowHeight = 100
            ws.Range(f"A{i}").Value = item['name']
            ws.Range(f"B{i}").Value = 'Outro'

            ws.Range(f"E{i}").Value = f"Evidência {item['number']}"
            path = Path(item['pic']).absolute()
            ws.Range(f"C{i}").Value = str(path)
            rng = ws.Range(f"D{i}")
            pic = ws.Pictures().Insert(str(path))
            pic.Left = rng.Left + 10
            pic.Top = rng.Top
            if pic.Width > pic.Height:
                pic.Width = 100
            else:
                pic.Height = 100
            i += 1
        wb.Save()

    def read_objects(self):
        self.connect_excel()
        wb = self.excel.ActiveWorkbook
        ws = wb.Worksheets("principal")
        ret = {}
        last_row = ws.Cells(ws.Rows.Count, "A").End(-4162).Row
        for i in range(1, last_row + 1):
            ret[ws.Range(f"A{i}").Value] = ws.Range(f"B{i}").Value
        ws = wb.Worksheets("objetos")
        objects = {}
        last_row = ws.Cells(ws.Rows.Count, "A").End(-4162).Row
        for i in range(2, last_row + 1):
            name = ws.Range(f"A{i}").Value
            try:
                objects[ws.Range(f"A{i}").Value]['pics'].append(
                    {'path': ws.Range(f"C{i}").Value, 'caption': ws.Range(f"E{i}").Value})
            except KeyError:
                nome_laudo = get_nome_laudo(ws.Range(f"A{i}").Value, ws.Range(f"B{i}").Value)
                objects[ws.Range(f"A{i}").Value] = {
                    'pics': [{'path': ws.Range(f"C{i}").Value, 'caption': ws.Range(f"E{i}").Value}],
                    'owner': ws.Range(f"F{i}").Value,
                    'lacre': ws.Range(f"G{i}").Value,
                    'type': ws.Range(f"B{i}").Value,
                    'nome_laudo': nome_laudo
                }
        pics = []
        for key, value in objects.items():
            for pic in value['pics']:
                pics.append(pic)
        ret['objects'] = objects
        ret['pics'] = pics
        return ret
