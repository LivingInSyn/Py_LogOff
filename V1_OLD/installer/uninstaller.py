'''
Created by Jeremy Mill, originally for use in the hi tech classrooms at the University of CT

Licensed under the GPLv3

jeremymill@gmail.com
github.com/livinginsyn
'''

import os
import shutil as util
import _winreg as wreg
import subprocess
import sys



#first thing to find is the version of the OS
def uninstall_actions():
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
    try:
        start_run_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,wreg.KEY_ALL_ACCESS)
        wreg.DeleteValue(start_run_key,'LogOff Utility')
        wreg.CloseKey(start_run_key)
    except WindowsError:
        pass
    #now the uninstall info
    try:
        uninstall_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Logoff_Utility",0,wreg.KEY_ALL_ACCESS)
        wreg.DeleteValue(uninstall_key,'DisplayName')
        wreg.DeleteValue(uninstall_key,'UninstallString')
        wreg.CloseKey(uninstall_key)
    except WindowsError:
        pass
    #finally the subkey
    try:
        uninstall_subkey = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall",0,wreg.KEY_ALL_ACCESS)
        wreg.DeleteKey(uninstall_subkey,'Logoff_Utility')
    except:
        pass

def find_current_dir():
        #found this on Stack Overflow, returns the correct current working directory for exe's or py files
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path
        
def copy_exe_to_temp():
    try:
        os.environ["PROGRAMFILES(X86)"]
        ver = 64
    except:
        ver = 32
    if ver == 32:
        directory = 'C:\\Program Files\\HTC-Logout\\'
    else:
        directory = 'C:\\Program Files (x86)\\HTC-Logout\\'
    filename = directory+"uninstall.exe"
    tempdir = os.environ['TEMP']
    util.copy(filename,tempdir)
    executable_name = os.path.join(tempdir,"uninstall.exe")
    subprocess.Popen([executable_name])
    exit()

#the meat and potatoes
path = find_current_dir()
if path == os.environ['TEMP']:
    uninstall_actions()
else:
    copy_exe_to_temp()