from docxtpl import DocxTemplate, InlineImage
import jinja2
from docx.shared import Pt
import win32com.client as win32
import pythoncom
import math
import settings
from filters import filters
from jinja_env_functions import global_functions
import codecs
import xml.etree.ElementTree as ET
import os
import formater
from helpers import set_defaults_attrib, to_points, remove_br
import codecs
import json


class WordManagerXml:
    def __init__(self):
        self.loader = jinja2.FileSystemLoader(str(settings.items_folder))
        self.jinja_env = jinja2.Environment(
            autoescape=True, loader=self.loader)
        for filter in filters:
            self.jinja_env.filters[filter.__name__] = filter
        for function in global_functions:
            self.jinja_env.globals[function.__name__] = function

    def render_template(self, template, context):
        if os.path.exists(settings.file_variables):
            with codecs.open(settings.file_variables, 'r', 'utf-8') as f:
                variables = json.load(f)
            context.update(variables)
            context['__resources_folder'] = settings.resources_folder
        return self.jinja_env.get_template(template).render(context)

    def format_range(self, range, el):
        if el.attrib['font-weight']:
            parts = el.attrib['font-weight'].split("|")
            for part in parts:
                getattr(formater.FontWeight, part)(range)
        if el.attrib['alignment']:
            formater.alignment(range, el)
        if el.attrib['font-size']:
            formater.font_size(range, el.attrib['font-size'])
        if el.attrib['font-name']:
            formater.font_name(range, el.attrib['font-name'])
        if el.attrib['font-color']:
            formater.font_color(range, el.attrib['font-color'])

    def replace(self, old, new):
        for myStoryRange in self.doc.StoryRanges:
            while True:
                myStoryRange.Find.Text = old
                myStoryRange.Find.Replacement.Text = new
                myStoryRange.Find.Wrap = 1  # win32.constants.wdFindContinue
                # win32.constants.wdReplaceAll
                myStoryRange.Find.Execute(Replace=2, Forward=True)
                myStoryRange = myStoryRange.NextStoryRange
                if myStoryRange == None:
                    break

    def add_template(self, data, from_file=False):
        if from_file:
            tree = ET.parse(os.path.join(settings.items_folder, data))
            root = tree.getroot()
        else:
            root = ET.fromstring(data)
        for el in root:
            if 'position' in el.attrib.keys() and el.attrib['position']:
                self.word.Selection.TypeText("!!@@##")
                self.word.ActiveDocument.Content.Select()
                self.word.Selection.Find.Text = el.attrib['position']
                found = self.word.Selection.Find.Execute(Forward=False)
                if found:
                    self.word.Selection.Delete()
                    self.add_element(el)
                self.word.ActiveDocument.Content.Select()
                self.word.Selection.Find.Text = "!!@@##"
                found = self.word.Selection.Find.Execute(Forward=False)
                if found:
                    self.word.Selection.Delete()
            else:
                self.add_element(el)

    def render_word(self, config, context):
        pythoncom.CoInitialize()
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        self.doc = self.word.ActiveDocument

        xml_text = self.render_template(config['template'], context)
        if settings.dev:
            with codecs.open(os.path.join(settings.app_dir, "temp", "template.html"), "w", "utf-8") as f:
                f.write(xml_text)
        # self.word.ScreenUpdating = False
        self.add_template(xml_text)
        # self.word.ScreenUpdating = True

    def add_element(self, el):
        set_defaults_attrib(el)
        if el.tag == 'p':
            self.insert_paragraph(el)
        elif el.tag == 'table':
            self.insert_table(el)
        elif el.tag.startswith('h') and len(el.tag) == 2:
            self.insert_title(el)
        elif el.tag in ['figure', 'picture']:
            self.insert_image(el)
        elif el.tag == 'br':
            self.insert_br()
        elif el.tag == 'backspace':
            self.insert_backspace()
        elif el.tag == 'delete':
            self.insert_delete()
        elif el.tag == 'text':
            self.insert_text(el)
        elif el.tag in ['ul', 'ol']:
            self.insert_list(el)
        elif el.tag == 'replace':
            self.replace(el)
        elif el.tag == 'set-style':
            self.set_style(el)
        elif el.tag == 'pause':
            input("Pressione uma tecla para prosseguir")
        elif el.tag == 'goto':
            self.go_to(el)

    def replace(self, el):
        for myStoryRange in self.doc.StoryRanges:
            while True:
                myStoryRange.Find.Text = el.attrib['marker']
                myStoryRange.Find.Replacement.Text = el.text
                myStoryRange.Find.Wrap = 1  # win32.constants.wdFindContinue
                # win32.constants.wdReplaceAll
                myStoryRange.Find.Execute(Replace=2, Forward=True)
                myStoryRange = myStoryRange.NextStoryRange
                if myStoryRange == None:
                    break

    def insert_list(self, el):
        if el.attrib['enter'].lower() != 'false':
            par = self.word.Selection.TypeParagraph()
        if el.tag == 'ol':
            self.word.Selection.Range.ListFormat.ApplyNumberDefault()
        else:
            self.word.Selection.Range.ListFormat.ApplyBulletDefault()
        for i, list_el in enumerate(el):
            set_defaults_attrib(list_el)
            if i != 0:
                self.word.Selection.TypeParagraph()
            self.insert_text(list_el)

    def insert_table(self, el):

        if el.attrib['enter'].lower() != 'false':
            par = self.word.Selection.TypeParagraph()
        self.word.Selection.Style = settings.styles['p']
        table = self.doc.Tables.Add(self.word.Selection.Range, 1, 1)
        row_els = el.findall('tr')
        for i, row_el in enumerate(row_els):
            self.word.Selection.InsertRowsBelow()
            n_cols = len(row_el)
            self.word.Selection.Cells.Merge()
            self.word.Selection.Cells.Split(NumRows=1, NumColumns=n_cols)
            for j, col_el in enumerate(row_el):
                set_defaults_attrib(col_el)
                cell = table.Cell(i+2, j+1)
                cell.Range.Select()
                # if col_el.attrib['style'].lower() != "false":
                #     self.word.Selection.Style = settings.styles['table']
                self.word.Selection.Style = el.attrib['style']
                self.format_range(cell.Range, col_el)
                if len(col_el):
                    for el_ in col_el:
                        self.add_element(el_)
                else:

                    self.insert_text(col_el)
                if col_el.tag == 'th':
                    cell.Range.Font.Bold = True
                width = to_points(col_el.attrib['w'])
                cell.SetWidth(ColumnWidth=width,
                              RulerStyle=win32.constants.wdAdjustNone)

        if ('border' not in el.attrib.keys() or el.attrib['border'].lower() != 'false'):
            table.Borders.InsideLineStyle = 1
            table.Borders.OutsideLineStyle = 1
        table.Rows(1).HeadingFormat = True
        cell_caption = table.Cell(1, 1)
        width = to_points(el.attrib['caption-col-width'])
        cell_caption.SetWidth(
            ColumnWidth=width, RulerStyle=win32.constants.wdAdjustNone)
        if el.attrib['caption']:
            label = el.attrib['caption-label']

            table.Range.InsertCaption(
                Label=label, Title=f" - {el.attrib['caption']}", Position=win32.constants.wdCaptionPositionAbove)
            table.Range.Previous(
                Unit=win32.constants.wdParagraph, Count=1).Select()
            self.word.Selection.Cut()
            cell_caption.Range.Paste()
            cell_caption.Range.Style = settings.styles['caption']
            table.Rows(1).Borders(1).LineStyle = 0
            table.Rows(1).Borders(2).LineStyle = 0
            table.Rows(1).Borders(4).LineStyle = 0
            table.Rows(2).HeadingFormat = True
        else:
            table.Rows(1).Delete()

        self.format_range(table, el)
        table.Range.Next(
            Unit=win32.constants.wdWord, Count=1).Select()
        self.word.Selection.Collapse(Direction=win32.constants.wdCollapseStart)

    def insert_title(self, el):
        type_ = el.tag
        if el.attrib['enter'].lower() != 'false':
            self.word.Selection.TypeParagraph()
        self.word.Selection.Style = settings.styles[type_]
        self.format_range(self.word.Selection, el)
        text = el.text or ""
        text = remove_br(text)
        self.word.Selection.TypeText(text)

    def insert_paragraph(self, el):
        if el.attrib['enter'].lower() != 'false':
            par = self.word.Selection.TypeParagraph()
        if el.attrib['style'].lower() != 'false':
            self.word.Selection.Style = settings.styles['p']
        if el.attrib['indent'].lower() == 'false':
            self.word.Selection.Paragraphs(1).FirstLineIndent = 0
        self.format_range(self.word.Selection, el)
        if len(el):
            for el_ in el:
                self.add_element(el_)
        else:
            self.insert_text(el)

    def insert_text(self, el):
        text = el.text or ""
        start = self.word.Selection.Range.End
        text = remove_br(text)
        self.word.Selection.TypeText(text)
        end = self.word.Selection.Range.End
        self.word.Selection.SetRange(Start=start, End=end)
        self.format_range(self.word.Selection, el)
        self.word.Selection.SetRange(Start=end, End=end)

    def insert_br(self):
        self.word.Selection.TypeParagraph()

    def insert_backspace(self):
        self.word.Selection.Collapse(Direction=win32.constants.wdCollapseEnd)
        self.word.Selection.TypeBackspace()

    def insert_delete(self):
        self.word.Selection.Delete()

    def set_style(self, el):
        self.word.Selection.Style = el.attrib['name']

    def insert_image(self, el):
        self.word.Selection.TypeText("")
        w = to_points(el.attrib['w'])
        filename = el.attrib['src'].replace("/", "\\")
        img = self.word.Selection.InlineShapes.AddPicture(
            FileName=filename, LinkToFile=False, SaveWithDocument=True)
        self.format_range(img, el)
        img.LockAspectRatio = True
        img.Width = w
        if 'caption' in el.attrib.keys():
            type_ = 'Figura' if el.tag == 'figure' else 'Foto'
            img.Range.InsertCaption(
                Label=type_, Title=f" - {el.attrib['caption']}", Position=win32.constants.wdCaptionPositionAbove)

    def go_to(self, el):
        slot = el.attrib['slot']
        self.word.ActiveDocument.Content.Select()
        self.word.Selection.Find.Text = slot
        found = self.word.Selection.Find.Execute(Forward=False)
        if found:
            self.word.Selection.Delete()
            for el_ in el:
                self.add_element(el_)
        else:
            self.word.Selection.Collapse(Direction=win32.constants.wdCollapseEnd)


if __name__ == "__main__":
    settings.set_dev()
    wm = WordManager()
    # pythoncom.CoInitialize()
    # wm.word = win32.gencache.EnsureDispatch('Word.Application')
    # wm.doc = wm.word.ActiveDocument

    # wm.add_template('teste.xml', from_file=True)

    # pessoas = [
    #     {'nome': 'Renato Martins Costa', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    #     {'nome': 'Jordana Cristina Soares de Castro', 'profissao': "AIS"},
    #     {'nome': 'Danilo Januario Camara', 'profissao': "Perito Criminal"},
    # ]
    # xml_text = wm.render_template('modelo1.html', {'pessoas': pessoas})
    # wm.add_template(xml_text)
