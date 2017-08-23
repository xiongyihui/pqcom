# -*- mode: python -*-
a = Analysis(['pqcom/pqcom.py'],
             pathex=['pqcom'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          Tree('pqcom/img', 'img'),
          name='pqcom.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='pqcom-logo.ico')
