from pathlib import Path
import jinja2
from filters import filters
from env_functions import global_functions
from datetime import datetime
from secretary import Renderer
import config
import models
from uno_handler import UnoHandler


class OdtHandler:
    def __init__(self, model, folder="."):
        self.model = model
        self.model_folder = config.models_folder / model
        self.folder = Path(folder)
        self.engine = Renderer()
        for filter_ in filters:
            self.engine.environment.filters[filter_.__name__] = filter_
        for function_ in global_functions:
            self.engine.environment.globals[function_.__name__] = function_

    def render_one(self, context, template, filename=None):
        template = self.model_folder / f"templates/{template}"
        if not template.exists():
            print(f"Arquivo {template} não existe")
            return
        result = self.engine.render(str(template), **context)
        destfile = self.folder / filename if filename else self.folder / f"{template.stem}.odt"
        with destfile.open("wb") as f:
            f.write(result)
        self.pos_process(destfile)
        return destfile

    def pos_process(self, path):
        hd = UnoHandler()
        hd.connect()
        hd.open_doc(path)
        hd.pos_process()
        hd.save_close()

# handler.open_doc("/media/renato/linux_data/temp/laudo.odt")


    def render(self, context):
        function = getattr(models, self.model).pre.pre
        function(context)
        self.render_one(context, "laudo.odt")
        self.render_one(context, "capa.odt")
        self.render_one(context, "midia.odt")

