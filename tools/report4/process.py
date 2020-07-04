import sys
from database import db_session
from models import *
import parsers
import helpers_cmd as hp
from config_manager import config_manager
from processors import processor_factory

read_source = db_session.query(ReadSource).get(int(sys.argv[1]))
parser = parsers.parsers_dict[read_source.source_type]()
parser.set_read_source(read_source)
parser.check_env()
print(f"Iniciando processamento {read_source.folder}")
hp.clear_read_source(read_source)
parser.run()
parser = None
for item in config_manager.data['processors']:
    processor = processor_factory(item, read_source)
    processor.run()
config_manager.set_process(read_source.folder, False)
read_source.process = False
db_session.add(read_source)
db_session.commit()

