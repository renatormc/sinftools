from pathlib import Path

p = Path(r'D:\laudos\trabalhando\D\midia\dados\celular\WhatsApp\EXTRATOR')
for i in p.glob('**/*'):
     print(i)

