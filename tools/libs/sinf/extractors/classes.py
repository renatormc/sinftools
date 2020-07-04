import jinja2
import os
import sqlite3
script_dir = os.path.dirname(os.path.realpath(__file__))
import codecs


class Contact:
    def __init__(self):
        self.name = ''
        self.entries = []
        self.source = ''
        self.deleted = ''
    
    def __str__(self):
        return self.name
   
    def __repr__(self):
        return self.name

class Sms:
    def __init__(self):
        self.contact = ''
        self.time = ''
        self.type = ''
        self.deleted = ''
        self.body = ''
    
    def __str__(self):
        return self.body
   
    def __repr__(self):
        return self.body

class Call:
    def __init__(self):
        self.contact = ''
        self.timestamp = None
        self.duration = None
        self.type = ''
        self.deleted = ''
           
    def __str__(self):
        return f"{self.contact}-{self.timestamp}"
   
    def __repr__(self):
        return f"{self.contact}-{self.timestamp}"

def datetime(input):
    try:
        return input.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ''

class Render:
    def __init__(self):
        self.loader = jinja2.FileSystemLoader(os.path.join(script_dir, "templates"))
        self.env = jinja2.Environment(autoescape=True, loader=self.loader)
        self.env.filters['datetime'] = datetime
        
    def render(self, what, data, out_file):
        whats = {
            "contact": "contact.html",
            "sms": "sms.html",
            "calllog": "calllog.html"
        }
        with codecs.open(out_file, 'w', 'utf-8') as f:
            text = self.env.get_template(whats[what]).render({"data":data})
            f.write(text)