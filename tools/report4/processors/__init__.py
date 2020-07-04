
from processors.chat_rename import ChatRename
from processors.proprietary_finder import ProprietaryFinder
from processors.thumb_video import ThumbVideo
from processors.thumb_image import ThumbImage
from processors.process_avatars import ProcessAvatars
from processors.file_type import FileType
from processors.add_file_info import AddFileInfo
from processors.file_duplicates import FileDuplicates
from processors.friendly_identifier import FriendlyIdentifier
from processors.chat_message_count import ChatMessageCount
from processors.translations import Translations
from processors.add_file_info import AddFileInfo
from processors.extension_generator import ExtensionGenerator
from processors.image_converter import ImageConverter
from processors.chat_last_activity import ChatLastActivity
from processors.group_info import GroupInfo
import inspect


def processor_factory(name, read_source=None):
    return globals()[name](read_source)
    
def get_list_processors():
    return [key for key, value in globals().items() if inspect.isclass(value)]