from secretary import Renderer
from renderizer.filters import filters
from renderizer.env_funcs import env_funcs
from pathlib import Path
import json
import config
from pre_process import pre_process

class Renderizer:
    def __init__(self) -> None:
        self.renderer = Renderer(media_path='./data/fotos')
        for filter_ in filters:
            self.renderer.environment.filters[filter_.__name__] = filter_
        for function_ in env_funcs:
            self.renderer.environment.globals[function_.__name__] = function_

    def read_context(self, file):
        path = Path(file)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def render(self, context_file):
        context = self.read_context(context_file)
        context['contexto_local'] = config.contexto_local
        pre_process(context)
        
        template = config.app_dir / "templates/laudo.odt"
        result = self.renderer.render(template, **context)
        with open('data/laudo.odt', 'wb') as f:
            f.write(result)

        template = config.app_dir / "templates/capa.odt"
        result = self.renderer.render(template, **context)
        with open('data/capa.odt', 'wb') as f:
            f.write(result)

        template = config.app_dir / "templates/midia.odt"
        result = self.renderer.render(template, **context)
        with open('data/midia.odt', 'wb') as f:
            f.write(result)

