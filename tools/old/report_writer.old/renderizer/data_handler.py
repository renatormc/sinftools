from secretary import Renderer
from renderizer.filters import filters
from renderizer.env_funcs import env_funcs, SubdocFunction, ObjectSpot
from pathlib import Path
import json
import config
from pre_process import pre_process
import context_store
from uuid import uuid4


class Renderizer:
    def __init__(self) -> None:
        self.renderer = Renderer(media_path=str(config.pics_folder))
        for filter_ in filters:
            self.renderer.environment.filters[filter_.__name__] = filter_
        for function_ in env_funcs:
            self.renderer.environment.globals[function_.__name__] = function_
        self.renderer.environment.globals["subdoc"] = SubdocFunction(self)
        self.renderer.environment.globals["object_spot"] = ObjectSpot(self)

    def render_subdoc(self, template, context):
        template = config.app_dir / "templates" / template
        print(template)
        if not template.exists():
            return
        name = uuid4()

        path = config.subdocs_temp_dir / f"{name}.odt"
        print(path)
        result = self.renderer.render(template, **context)
        with path.open("wb") as f:
            f.write(result)
        return name

    def render(self):
        context = context_store.read_context()
        context['contexto_local'] = config.contexto_local
        pre_process(context)

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
