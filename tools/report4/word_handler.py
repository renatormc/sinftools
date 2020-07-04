from renderizer.renderizer import Renderizer
from models import *
import win32com.client as win32
import imgkit
import os
import pythoncom
import settings
import pathlib
from docx_tpl_manager import WordManager

sinftools_dir = os.getenv("SINFTOOLS")

class WordHandler:
    def __init__(self):
        self.temp_folder = r'.report\temp'
        path = os.path.join(settings.app_dir, 'renderizer', 'html_files', 'assets')
        self.assets_url = pathlib.Path(path).as_uri()
        if not os.path.exists(self.temp_folder):
            os.mkdir(self.temp_folder)
        pythoncom.CoInitialize()
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        self.doc = self.word.ActiveDocument

    def insert_chat_messages_table(self, caption_, messages):
        word_manager = WordManager()
        context = {'caption': caption_, 'messages': messages}
        word_manager.render_word('chat_messages.docx', caption=caption_, messages=messages)
        

    def insert_chat_messages_html(self, caption_, per_figure, tags):
        caption_ = str(caption_).strip()
        path_wkthmltoimage = f'{sinftools_dir}\\extras\\wkhtmltox\\bin\\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        temp_files = []
        generated_files = self.render_chat_message_word(tags=tags, per_figure=per_figure)
        for i, filename in enumerate(generated_files):
            temp_image_name = f"{self.temp_folder}\\chat_image_{i+1}.jpg"
            try:
                imgkit.from_file(filename, temp_image_name, config=config)
            except:
                pass
            path = os.path.join(os.getcwd(), temp_image_name)
            if os.path.exists(path):
                temp_files.append(path)
        n_col = 1
        n_row = len(temp_files)
        if n_row > 0:
            table = self.doc.Tables.Add(self.word.Selection.Range, n_row, n_col)
            table.Borders.InsideLineStyle = 0
            table.Borders.OutsideLineStyle = 0
            for i in range(1, n_row + 1):
                for j in range(1, n_col + 1):
                    k = n_col * (i - 1) + j - 1
                    if k >= len(generated_files):
                        break
                    shape = table.Cell(i, j).Range.InlineShapes.AddPicture(temp_files[k])
                    shape.Select
                    table.Cell(i, j).Range.Paragraphs(1).Alignment = win32.constants.wdAlignParagraphCenter
                    caption = shape.Range.InsertCaption(Label="Figura", Title=f" - {caption_}",
                                                        Position=win32.constants.wdCaptionPositionBelow)
            table.Select()
            try:
                self.word.Selection.Style = self.doc.Styles("Legenda")
            except:
                pass

    def select_after(self):
        self.word.Selection.Collapse(0)
        self.word.Selection.InsertBreak(6)


    def insert_images(self, n_col, files, caption="?"):
        if len(files) % n_col != 0:
            n_row = int(len(files) / n_col) + 1
        else:
            n_row = int(len(files) / n_col)
        n_row += 1
        table = self.doc.Tables.Add(self.word.Selection.Range, n_row, n_col)
        table.Borders.InsideLineStyle = 1
        table.Borders.OutsideLineStyle = 1
        for i in range(1, n_row):
            for j in range(1, n_col + 1):
                k = n_col * (i - 1) + j - 1
                if k >= len(files):
                    break
                if os.path.exists(files[k]):
                    path = pathlib.Path(files[k]).absolute()
                    table.Cell(i + 1, j).Range.InlineShapes.AddPicture(str(path))
        table.Cell(1, 1).Merge(MergeTo=table.Cell(1, n_col))
        table.Cell(1,1).Select
        table.Borders.InsideLineStyle = 1
        table.Borders.OutsideLineStyle = 1
        table.Rows(1).Borders(1).LineStyle = 0
        table.Rows(1).Borders(2).LineStyle = 0
        table.Rows(1).Borders(4).LineStyle = 0
        table.Cell(1, 1).Range.Select
        caption =  table.Cell(1, 1).Range.InsertCaption(Label="Tabela", Title=f" - {caption}", Position =0)
        table.Rows(1).HeadingFormat = True
        table.Rows(1).Range.Style = self.doc.Styles("Legenda")


    def render_chat_message_word(self, tags, per_figure=5):
        renderizer = Renderizer(".")
        query = db_session.query(Message).filter(Message.tags.any(Tag.id.in_(tags))).order_by(Message.chat_id.asc(),
                                                                                  Message.timestamp.asc())
        n_messages = query.count()
        n_parts = int(n_messages / per_figure)
        rest = n_messages % per_figure
        generated_files = []
        for i in range(n_parts):
            first = i * per_figure
            messages = query.offset(first).limit(per_figure).all()
            for message in messages:
                for attachment in message.attachments:
                    if attachment.type_ == "video" and attachment.thumb_path:
                        path = os.path.join(os.getcwd(), attachment.thumb_path)
                    else:
                        path = os.path.join(os.getcwd(), attachment.extracted_path)
                    attachment.temp_link = pathlib.Path(path).as_uri()
            context = {"messages": messages, 'assets_url': self.assets_url}
            filename = f"{self.temp_folder}\\chat_messages_word_{i+1}.html"
            renderizer.render_template("chat_messages_word.html", filename, context)
            generated_files.append(filename)
        if rest > 0:
            first = n_parts * per_figure
            context = {"items": query.offset(first).limit(first + rest).all(), 'assets_url': self.assets_url}
            filename = f"{self.temp_folder}\\chat_messages_word_{n_parts + rest}.html"
            renderizer.render_template("chat_messages_word.html", filename, context)
            generated_files.append(filename)
        return generated_files
