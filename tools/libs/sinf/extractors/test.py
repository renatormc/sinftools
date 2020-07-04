from sinf.extractors.readers import  *
from sinf.extractors.classes import Render

contacts = getContacts_1(r'J:\laudos\trabalhando\319.2017\extracoes\C2\contacts2.db')
smss = getSmss_1(r'J:\laudos\trabalhando\319.2017\extracoes\C2\mmssms.db')
render = Render()
render.render(data=contacts, what='contact', out_file=r'C:\temp\Contatos.html')
render.render(data=smss, what='sms', out_file=r'C:\temp\sms.html')
