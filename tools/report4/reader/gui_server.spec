# -*- mode: python -*-

block_cipher = None


a = Analysis(['gui_server.py'],
             pathex=['C:\\sinftools\\Miniconda3\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'C:\\sinftools\\tools\\report4\\reader'],
             binaries=[],
             datas=[('templates', 'templates'), ('static', 'static'), ('reader_server\\resources', 'reader_server\\resources'), ('report_docx\\templates', 'report_docx\\templates')],
             hiddenimports=['sqlalchemy.ext.baked', 'PyQt5.sip', 'inflection'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='gui_server',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gui_server')
