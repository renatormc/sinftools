from parsers.spi2db.spi2db import SPIParser
from parsers.xml2db.xml2db import XmlParser
from parsers.sqlite2db.sqlite2db import Sqlite2Db
from parsers.files_folder2db.files_folder2db import FilesFolder2Db
from parsers.fbmessenger2db.fbmessenger2db import FBMessenger2Db
from parsers.fbmessenger2db2.fbmessenger2db2 import FBMessenger2Db2
from parsers.sqlite_iphone.sqlite_iphone import SqliteIphone
from parsers.whatsapp_dr_phone.whatsapp_dr_phone import WhatsAppDrPhone



parsers_dict = {
    "xml_ufed": XmlParser,
    "spi_tools": SPIParser,
    "sqlite": Sqlite2Db,
    "files_folder": FilesFolder2Db,
    "fbmessenger": FBMessenger2Db,
    "fbmessenger2": FBMessenger2Db2,
    "sqlite_iphone": SqliteIphone,
    "whatsapp_dr_phone": WhatsAppDrPhone
}
