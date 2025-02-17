import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=unmark',
    '--onefile',
    '--noconsole',
    '--clean',
    '--add-data=src;src',  # For Windows
    '--add-data=unmark-ico.ico;.',  # Add icon to root of bundled resources
    # '--add-data=src:src',  # For Linux/Mac
    '--icon=unmark-ico.ico',  # Optional: Add this line if you have an icon
    '--uac-admin',  # Force admin privileges
    '--manifest', 'unmark.manifest'  # Correct syntax for manifest
]) 