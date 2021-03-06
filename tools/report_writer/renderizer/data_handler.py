from secretary import Renderer
from renderizer.filters import filters
from renderizer.env_funcs import env_funcs
from pathlib import Path
import json
import config
import context_store
from uuid import uuid4


class Renderizer:
    def __init__(self) -> None:
        self.renderer = Renderer(media_path=str(config.pics_folder))
        for filter_ in filters:
            self.renderer.environment.filters[filter_.__name__] = filter_
        for function_ in env_funcs:
            self.renderer.environment.globals[function_.__name__] = function_


    def render_subdoc(self, template, context):
        template = config.app_dir / "templates" / template
        if not template.exists():
            return
        name = uuid4()

        path = config.subdocs_temp_dir / f"{name}.odt"
        result = self.renderer.render(template, **context)
        with path.open("wb") as f:
            f.write(result)
        return name

    def render(self, context):
        

        template = config.app_dir / "templates/laudo.odt"
        result = self.renderer.render(template, **context)
        with config.laudo_file.open('wb') as f:
            f.write(result)

        template = config.app_dir / "templates/capa.odt"
        result = self.renderer.render(template, **context)
        with config.capa_file.open('wb') as f:
            f.write(result)

        template = config.app_dir / "templates/midia.odt"
        result = self.renderer.render(template, **context)
        with config.midias_file.open('wb') as f:
            f.write(result)
