from pathlib import Path
from com.sun.star.beans import PropertyValue
from datetime import datetime

def compile_path(doc):
    path = Path(doc.getURL().replace("file:///", ""))
    path = path.parent / f"compiled{path.suffix}"
    path_pdf = path.parent / f"compiled.pdf"
    return path.as_uri(),  path_pdf.as_uri()


def save_pdf(doc, url):
    property = (
    PropertyValue( "FilterName" , 0, "writer_pdf_Export" , 0 ),
    )
    doc.storeToURL(url, property)

def dictToProperties(dictionary): #normally I'd just import this
    """
    Utitlity to convert a dictionary to properties
    """
    props = []
    for key in dictionary:
        prop = PropertyValue()
        prop.Name = key
        prop.Value = dictionary[key]
        props.append(prop)
    return tuple(props)

def convert_data(value, type):
    if type == 'string':
        return value
    if type == 'int':
        try:
            return int(value)
        except:
            return 0
    if type == 'float':
        try:
            return float(value)
        except:
            return 0.0
    if type == 'date':
        try:
            return datetime.strptime(value, "%d/%m/%Y")
        except:
            return None

 