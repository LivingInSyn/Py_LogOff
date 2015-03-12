import os
import shutil as util
import _winreg as wreg


#first thing to find is the version of the OS
try:
    os.environ["PROGRAMFILES(X86)"]
    ver = 64
except:
    ver = 32
    
#quick variable
overwrite = False
    
#function for 64 bit programfiles
def sixty_folder():
    directory = 'C:\\Program Files (x86)\\HTC-Logout\\'
    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        overwrite = True

def thirty_folder():
    directory = 'C:\\Program Files\\HTC-Logout\\'
    if not os.path.exists(directory):
        os.mkdir(directory)
    else:
        overwrite = True
        
def install():
    #put the files where they need to go
    files = ["HTC-LogOut.exe","warning.exe","logoff_config.cfg","logout_banner.png"]
    for item in files:
        util.copy(item,directory)
    #make the runtime registry key
    #note the KEY ALL ACCESS is important, and so are the escaped quotes in the key
    #this one is tested and working
    start_run_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(start_run_key, 'LogOff Utility', 0, wreg.REG_SZ, "\""+directory+"HTC-LogOut.exe"+"\"")
    wreg.CloseKey(start_run_key)
    
    #create the subkey
    uninstall_subkey = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall",0,wreg.KEY_ALL_ACCESS)
    wreg.SetValue(uninstall_subkey, 'Logoff_Utility', wreg.REG_SZ, '')
    wreg.CloseKey(uninstall_subkey)
    #create the uninstall information
    uninstall_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Logoff_Utility",0,wreg.KEY_ALL_ACCESS)
    wreg.SetValueEx(uninstall_key, 'DisplayName', 0, wreg.REG_SZ, "HTC Logoff Utility")
    #as a side note...this uninstaller doesn't exist...yet....
    wreg.SetValueEx(uninstall_key, 'UninstallString', 0, wreg.REG_SZ, "\""+directory+"uninstall.exe"+"\"")
    wreg.CloseKey(uninstall_key)
    
        
        
#the meat and potatoes
if ver == 64:
    sixty_folder()
    install()
elif ver == 32:
    thirty_folder()
    install()