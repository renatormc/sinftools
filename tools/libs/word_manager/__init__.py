import win32com.client as win32
import pythoncom
from pathlib import Path
import tempfile
from docxtpl import DocxTemplate
from sinf.sinftools_config import SinfToolsConfig
import constants

sc = SinfToolsConfig()


class WordManager(object):

    def __init__(self):
        super().__init__()
        self.word = None
        self.doc = None


    def connect(self):
        pythoncom.CoInitialize()
        # self.word = win32.gencache.EnsureDispatch('Word.Application')
        self.word = win32.Dispatch('Word.Application')
        if not self.word:
            raise Exception("Não foi possível se conectar ao Word")
        self.doc = self.word.ActiveDocument

    def imprimir_laudo(self):
        self.doc.Application.ActivePrinter = sc.getprop(
            "laudos.printer_name") or ""
        self.doc.PrintOut(Copies=1, Pages="S2")
        self.doc.PrintOut(Copies=2, Pages="S1", ManualDuplexPrint=False)
        path = Path(self.doc.FullName).with_suffix(".pdf")
        self.doc.SaveAs2(FileName=str(path), FileFormat=17)

    @property
    def doc_path(self):
        return Path(self.doc.FullName)

    def goto(self, slot):
        self.word.ActiveDocument.Content.Select()
        self.word.Selection.Find.Text = slot
        found = self.word.Selection.Find.Execute(Forward=False)
        if found:
            self.word.Selection.Delete()
            # for el_ in el:
            #     self.add_element(el_)
        else:
            self.word.Selection.Collapse(
                Direction=constants.wdCollapseEnd)

    def insert_paragraph(self, text, enter=False, indent=True, style="Normal"):
        if enter:
            par = self.word.Selection.TypeParagraph()
        self.word.Selection.Style = style
        if not indent:
            self.word.Selection.Paragraphs(1).FirstLineIndent = 0
        self.insert_text(text)

    def insert_text(self, text):
        text = text or ""
        start = self.word.Selection.Range.End
        self.word.Selection.TypeText(text)
        end = self.word.Selection.Range.End
        self.word.Selection.SetRange(Start=start, End=end)
        self.word.Selection.SetRange(Start=end, End=end)

    def replace(self, old, new):
        for myStoryRange in self.doc.StoryRanges:
            while True:
                myStoryRange.Find.Text = old
                myStoryRange.Find.Replacement.Text = new
                myStoryRange.Find.Wrap = constants.wdFindContinue
                myStoryRange.Find.Execute(Replace=constants.wdReplaceAll, Forward=True)
                myStoryRange = myStoryRange.NextStoryRange
                if myStoryRange == None:
                    break

    def insert_pictures(self, pics, n_col, max_width=300):
        # convert to table
        table = [pics[i:i + n_col] for i in range(0, len(pics), n_col)]

        # insert table
        for row in table:
            n_col = len(row)
            tabela = self.doc.Tables.Add(self.word.Selection.Range, 1, n_col)
            tabela.Borders.InsideLineStyle = 0
            tabela.Borders.OutsideLineStyle = 0
            for i, pic in enumerate(row):
                shape = tabela.Cell(
                    1, i + 1).Range.InlineShapes.AddPicture(pic['path'])
                shape.LockAspectRatio = -1
                if shape.Width > max_width:
                    shape.Width = max_width
                shape.Select

                tabela.Cell(
                    1, i + 1).Range.Paragraphs(1).Alignment = 1
                caption = shape.Range.InsertCaption(
                    Label="Foto", Title=" - " + pic['caption'], Position=constants.wdCaptionPositionAbove)
            tabela.Select()
            self.word.Selection.Collapse(0)
            self.word.Selection.TypeParagraph()

     

    def type_enter(self):
        self.word.Selection.TypeParagraph()

    def insert_doc(self, path):
        path = Path(path).absolute()
        if path.exists():
            self.word.Selection.InsertFile(str(path))

    def render_template_insert(self, template, **context):
        if not Path(template).exists():
            return
        doc = DocxTemplate(template)
        doc.render(context)
        temp_file = tempfile.mktemp(suffix=".docx")
        doc.save(temp_file)
        self.insert_doc(temp_file)
