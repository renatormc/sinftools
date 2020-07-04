# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['c:\\sinftools\\tools\\sinf_zip\\copier'],
             binaries=[],
             datas=[('icon.png', '.')],
             hiddenimports=['PyQt5.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=True,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MB_reader',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
