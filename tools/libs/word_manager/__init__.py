import win32com.client as win32
import pythoncom
from pathlib import Path
import tempfile
from docxtpl import DocxTemplate
from sinf.sinftools_config import SinfToolsConfig

sc = SinfToolsConfig()


class WordManager(object):

    def __init__(self):
        super().__init__()

    def connect(self):
        pythoncom.CoInitialize()
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        if not self.word:
            raise Exception("Não foi possível se conectar ao Word")
        self.doc = self.word.ActiveDocument

    def imprimir_laudo(self):
        self.doc.Application.ActivePrinter = sc.getprop("laudos.printer_name") or ""
        self.doc.PrintOut(Copies=1, Pages="S2")
        self.doc.PrintOut(Copies=2, Pages="S1", ManualDuplexPrint=False)
        path = Path(self.doc.FullName).with_suffix(".pdf")
        self.doc.SaveAs2(FileName=str(path), FileFormat=17)

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
                Direction=win32.constants.wdCollapseEnd)

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
                myStoryRange.Find.Wrap = 1  # win32.constants.wdFindContinue
                # win32.constants.wdReplaceAll
                myStoryRange.Find.Execute(Replace=2, Forward=True)
                myStoryRange = myStoryRange.NextStoryRange
                if myStoryRange == None:
                    break

    def insert_pictures(self, pics, n_col, max_width=300):
        qtd = len(pics)
        if qtd < n_col:
            n_col = qtd
        if qtd % n_col != 0:
            n_row = int(qtd/n_col) + 1
        else:
            n_row = int(qtd/n_col)
        for i in range(1, n_row + 1):
            tabela = self.doc.Tables.Add(self.word.Selection.Range, 1, n_col)
            tabela.Borders.InsideLineStyle = 0
            tabela.Borders.OutsideLineStyle = 0
            for j in range(1, n_col + 1):
                k = n_col*(i-1) + j-1
                if k >= qtd:
                    break
                shape = tabela.Cell(
                    1, j).Range.InlineShapes.AddPicture(pics[k]['path'])
                shape.LockAspectRatio = -1
                if shape.Width > max_width:
                    shape.Width = max_width
                shape.Select

                tabela.Cell(1, j).Range.Paragraphs(
                    1).Alignment = win32.constants.wdAlignParagraphCenter
                caption = shape.Range.InsertCaption(
                    Label="Foto", Title=" - " + pics[k]['caption'], Position=win32.constants.wdCaptionPositionAbove)
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
