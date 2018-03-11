# -*- mode: python -*-

import platform

name = 'pqcom' + platform.architecture()[0][:2] + '.exe'

a = Analysis(['pqcom/main.py'],
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
          name=name,
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='pqcom-logo.ico')
