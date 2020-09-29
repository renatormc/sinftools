from handler import Handler

handler = Handler(workdir=r'C:\temp\A')
handler.connect()
handler.scan_pics()
handler.write_objects()