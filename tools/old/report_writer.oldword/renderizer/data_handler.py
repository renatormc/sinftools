import excel_handler
from renderizer.filters import filters
from renderizer.env_funcs import env_funcs
from pathlib import Path
import json
import config
from docxtpl import DocxTemplate, InlineImage, Subdoc
import jinja2
from excel_handler import ExcelHandler

class Renderizer:
    def __init__(self) -> None:
        loader = jinja2.FileSystemLoader(str(config.templates_dir.absolute()))
        self.jinja_env = jinja2.Environment(autoescape=True, loader=loader)
        for filter_ in filters:
            self.jinja_env.filters[filter_.__name__] = filter_
        for function_ in env_funcs:
            self.jinja_env.globals[function_.__name__] = function_

    def get_context(self) -> dict:
        excel = ExcelHandler()
        return excel.get_objects_info()

    def render(self):
        tpl_file = "laudo.docx"
        tpl = DocxTemplate(str(tpl_file))
        context = self.get_context()
        tpl.render(context, self.jinja_env)
        tpl.save(str(config.generated_laudo))

    def gen_laudo(self):
        print(self.get_context())

