# -*- mode: python -*-
import os
from inspect import getfile
import PyQt5

block_cipher = None

a = Analysis(['src/main.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SEASide',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          # console=True makes it perform as a normal app on Mac (no double-bounce)
          # TODO: Check on Windows/Linux
          console=True, icon='icons/icon.ico')
app = BUNDLE(exe,
             name='SEASide.app',
             icon='icons/icon.icns',
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'}
             )
