import jinja2schema
import settings
import codecs
import os

with codecs.open(os.path.join(settings.items_folder, 'celular.html'), 'r', 'utf-8') as f:
    text = f.read()
variables = jinja2schema.infer(text)
print(variables)