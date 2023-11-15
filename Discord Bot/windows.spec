# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['gui.py'],
             pathex=[],
             binaries=[],
             datas=[('images', 'images')],  # Include the images directory
             hiddenimports=['requests'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Discord Bot',  # Name of the executable
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)

# If you only want the EXE without the COLLECT directory, comment out or remove the following lines
# coll = COLLECT(exe,
#                a.binaries,
#                a.zipfiles,
#                a.datas,
#                strip=False,
#                upx=True,
#                upx_exclude=[],
#                name='Discord Bot')

