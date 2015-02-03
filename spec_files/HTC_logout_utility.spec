# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())
a = Analysis(['C:\\Users\\student1953\\Documents\\GitHub\\Py_LogOff\\main.py'],
             pathex=['C:\\uits\\Kivy-1.8.0-py2.7-win32\\PyInstaller-2.1\\HTC_logout_utility'],
             hiddenimports=[],
             runtime_hooks=None)
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
pyz = PYZ(a.pure)
exe = EXE(pyz,
		Tree('C:\\Users\\student1953\\Documents\\GitHub\\Py_LogOff\\'),
		a.scripts,
		a.binaries,
		a.zipfiles,
		a.datas,
		name='HTC_logout_utility.exe',
		debug=False,
		strip=None,
		upx=True,
		console=False,
		icon='C:\\Users\\student1953\\Documents\\GitHub\\Py_LogOff\\myicon.ico')
