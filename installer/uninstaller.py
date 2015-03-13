'''
Created by Jeremy Mill, originally for use in the hi tech classrooms at the University of CT

Licensed under the GPLv3

jeremymill@gmail.com
github.com/livinginsyn
'''

import os
import shutil as util
import _winreg as wreg

#first thing to find is the version of the OS
try:
    os.environ["PROGRAMFILES(X86)"]
    ver = 64
except:
    ver = 32
    
if ver == 32:
    directory = 'C:\\Program Files\\HTC-Logout\\'
else:
    directory = 'C:\\Program Files (x86)\\HTC-Logout\\'

#delete the directory    
util.rmtree(directory,ignore_errors=True)

#remove registry entries
#first the run entry
start_run_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,wreg.KEY_ALL_ACCESS)
wreg.DeleteValue(start_run_key,'LogOff Utility')
wreg.CloseKey(start_run_key)
#now the uninstall info
uninstall_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Logoff_Utility",0,wreg.KEY_ALL_ACCESS)
wreg.DeleteValue(uninstall_key,'DisplayName')
wreg.DeleteValue(uninstall_key,'UninstallString')
wreg.CloseKey(uninstall_key)
#finally the subkey
uninstall_subkey = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall",0,wreg.KEY_ALL_ACCESS)
wreg.DeleteKey(uninstall_subkey,'Logoff_Utility')

