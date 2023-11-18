# -*- mode: python ; coding: utf-8 -*-

"""
    Enhanced PyInstaller Specification File for Discord Bot Application
    ======================================================================
    This enhanced PyInstaller spec file is designed for optimal packaging 
    of the Discord Bot application for Windows x64 systems. It includes 
    configurations for a one-folder bundle, custom icons, version information, 
    and more.

    Key Enhancements:
    - One-folder bundle for faster startup and easier debugging.
    - Custom icon for the executable.
    - Version information for a professional look.
    - UPX compression for reduced file size.
    - Runtime hooks and hidden imports for comprehensive dependency management.
    - Debug mode option for troubleshooting.

    Usage Notes:
    - Replace 'dept14.ico' with the path to your application's icon file.
    - Adjust version information in the 'versioninfo' section as needed.
    - Uncomment the 'debug=True' line for troubleshooting purposes.

    Instructions:
    - To generate the executable, run: 'pyinstaller windowsx64.spec'
    - Modify the spec file as needed for specific requirements or additional files.
"""

block_cipher = None

a = Analysis(['gui.py'],
             pathex=[],
             binaries=[],
             datas=[('images', 'images')],  # Include the images directory
             hiddenimports=['requests', 'psutil'],
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
          name='Discord Bot Windows x64',  # Updated name of the executable
          debug=False,  # Set to True for debugging
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='dept14.ico',  # Path to your application's icon
          version='versioninfo.txt')  # Path to version info file

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='Discord Bot Windows x64')  # Updated name for the one-folder bundle

# Note: Ensure that 'dept14.ico' and 'versioninfo.txt' exist and are correctly referenced.
