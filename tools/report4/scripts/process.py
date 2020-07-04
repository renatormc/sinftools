import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *
from processor import Processor


devices = db_session.query(Device).all()
for device in devices:
    for read_source in device.read_sources:
        processor = Processor()
        processor.set_read_source(read_source)
        processor.exclude_duplicates_file_attachment()
        processor.generate_friendly_identifier_chat()
        processor.genenerate_friendly_identifier_participant()
        processor.process_avatars()
        processor.process_files()
        processor.generate_image_thumbs()
        processor.generate_video_thumbs()
        processor.count_messages_per_chat()
        processor.remove_file_zero_size()
        processor.translate_call()
        processor.translate_sms()
        processor.add_info_files()
        processor.set_render_config()
