from docxtpl import DocxTemplate, InlineImage
import jinja2
from widgets.helpers import DataContext
from docx.shared import Pt
import win32com.client as win32
import math
import settings
from filters import filters
from jinja_env_functions import global_functions
import os
import codecs
import json
import jinja_env_functions as jef

class WordManagerDocx:
    def __init__(self):
        self.jinja_env = jinja2.Environment()
        for filter in filters:
            self.jinja_env.filters[filter.__name__] = filter
        for function in global_functions:
            self.jinja_env.globals[function.__name__] = function

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


    def render(self, config, context, file_):
        if os.path.exists(settings.file_variables):
            with codecs.open(settings.file_variables, 'r', 'utf-8') as f:
                variables = json.load(f)
            context.update(variables)
            context['__resources_folder'] = settings.resources_folder
        template_file = os.path.join(settings.items_folder, config['template'])
        tpl = DocxTemplate(template_file)
        context = self.format_context(context, tpl)
        tpl.render(context, self.jinja_env)
        tpl.save(file_)


    def render_word(self, config, context):
        if os.path.exists(settings.file_variables):
            with codecs.open(settings.file_variables, 'r', 'utf-8') as f:
                variables = json.load(f)
            context.update(variables)
        template_file = os.path.join(settings.items_folder, config['template'])
        tpl = DocxTemplate(template_file)
        context = self.format_context(context, tpl)
        tpl.render(context, self.jinja_env)
        tempfile = f"{settings.app_dir}\\temp\\temp.docx"
        tpl.save(tempfile)
        word = win32.gencache.EnsureDispatch('Word.Application')
        word.Selection.InsertFile(tempfile)
