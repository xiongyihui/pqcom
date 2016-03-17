# -*- mode: python -*-
a = Analysis(['pqcom.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('img', 'img'),
          name='pqcom.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='pqcom-logo.ico')
