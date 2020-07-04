from docxtpl import DocxTemplate, InlineImage
import jinja2
from docx.shared import Pt
import win32com.client as win32
import math
import settings
from docx_tpl_manager.filters import *
import os
script_dir = os.path.dirname(os.path.realpath(__file__))


#Types: image, image_group
class DataContext:
    def __init__(self, type_, data):
        self.type = type_
        self.data = data

class WordManager:
    def __init__(self):
        self.jinja_env = jinja2.Environment()
        self.jinja_env.filters['not_null'] = not_null
        self.jinja_env.filters['data_completa'] = data_completa
        self.jinja_env.filters['strftime_complete'] = strftime_complete
        self.jinja_env.filters['hora_minuto'] = hora_minuto
        self.jinja_env.filters['dia'] = dia
        self.jinja_env.filters['dia_extenso'] = dia_extenso
        self.jinja_env.filters['mes_extenso'] = mes_extenso
        self.jinja_env.filters['data_mes_extenso'] = data_mes_extenso
        self.jinja_env.filters['xxx'] = xxx


    def get_table(self, data, tpl):
        images = data['images']
        n_images = len(images)
        n_cols = data['per_row']
        n_rows = math.ceil(n_cols)
        rows = []
        count = 0
        for i in range(n_rows):
            row = []
            for j in range(n_cols):
                if count >= n_images:
                    break
                item = {"caption": images[count]['caption'], "image": InlineImage(tpl, images[count]['path'], width=Pt(images[count]['width']))}
                row.append(item)
                count += 1
            if row:
                rows.append(row)
        return rows


    def format_context(self, context, tpl):
        for key in context.keys():
            if isinstance(context[key], DataContext):
                if context[key].type == "image":
                    context[key] = {"caption": context[key].data['caption'],"image": InlineImage(tpl, context[key].data['path'], width=Pt(context[key].data['width']))}
                elif context[key].type == "image_group":
                    context[key] = self.get_table(context[key].data, tpl)
        return context

    def replace_attachments(self, messages, tpl):
        items = []
        for i, message in enumerate(messages):
            item = {"attachment": None, 'message': message}
            if message.attachments.count() > 0:
                att_aux = message.attachments[0]
                thumb_path = att_aux.thumb_path
                if att_aux.type_ == "image":
                    item['attachment'] = {"image": InlineImage(tpl, att_aux.path, width=Pt(80))}
                
                elif att_aux.type_ == "video" and thumb_path is not None:

                    item['attachment'] = {"image": InlineImage(tpl, str(thumb_path), width=Pt(80))}
            items.append(item)
        return items
            

    def render(self, template, context, file_):
        template_path = os.path.join(script_dir, 'templates', template)
        tpl = DocxTemplate(template_path)
        context = self.format_context(context, tpl)
        tpl.render(context, self.jinja_env)
        tpl.save(file_)


    def render_word(self, template, caption, messages):
        template_path = os.path.join(script_dir, 'templates', template)
        tpl = DocxTemplate(template_path)
        items = self.replace_attachments(messages, tpl)
        context = {"caption": caption, 'items': items}
        tpl.render(context, self.jinja_env)
        tempfile = os.path.join(script_dir, "temp", "temp.docx")
        tpl.save(tempfile)
        word = win32.gencache.EnsureDispatch('Word.Application')
        word.Selection.InsertFile(tempfile)
