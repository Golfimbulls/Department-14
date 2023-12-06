# -*- mode: python ; coding: utf-8 -*-

"""
    Enhanced PyInstaller Specification File for Discord Bot Application (macOS)
    ===========================================================================
    This enhanced PyInstaller spec file is designed for optimal packaging 
    of the Discord Bot application for macOS systems. It includes configurations 
    for a macOS app bundle, custom icons, and more.

    Key Enhancements:
    - macOS app bundle for native macOS application experience.
    - Custom icon for the macOS application.
    - Version information and additional plist settings for macOS compatibility.
    - Runtime hooks and hidden imports for comprehensive dependency management.

    Usage Notes:
    - Replace 'app_icon.icns' with the path to your application's icon file in ICNS format.
    - Adjust version information and other plist settings as needed.

    Instructions:
    - To generate the macOS app bundle, run: 'pyinstaller macOS.spec'
    - Modify the spec file as needed for specific requirements or additional files.
"""

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
          name='Discord Bot macOS',  # Updated name of the executable
          debug=False,  # Set to True for debugging
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)  # No console for macOS windowed applications

app = BUNDLE(exe,
             name='Discord Bot macOS.app',  # Name of the macOS app bundle
             icon='app_icon.icns',  # Path to your application's icon in ICNS format
             bundle_identifier='com.yourcompany.discordbot',  # Bundle identifier
             version='0.0.1',  # Application version
             info_plist={
                'NSPrincipalClass': 'NSApplication',
                'NSAppleScriptEnabled': False,
                'CFBundleDocumentTypes': [
                    {
                        'CFBundleTypeName': 'Discord Bot File',
                        'CFBundleTypeIconFile': 'file_icon.icns',
                        'LSItemContentTypes': ['com.yourcompany.discordbot.file'],
                        'LSHandlerRank': 'Owner'
                    }
                ]
             },
         )

# Note: Ensure that 'app_icon.icns' and other referenced files exist and are correctly referenced.
