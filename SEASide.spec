# -*- mode: python -*-
import platform

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

console = platform.system() != 'Darwin'  # console should only be false on Mac

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
          # TODO: Check on Windows/Linux
          console=console, icon='icons/icon.ico')
app = BUNDLE(exe,
             name='SEASide.app',
             icon='icons/icon.icns',
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'}
             )
