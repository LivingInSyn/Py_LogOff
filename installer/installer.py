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
    if overwrite == False:
        start_run_key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "Software\\Microsoft\\Windows\\CurrentVersion\\Run",0,wreg.KEY_ALL_ACCESS)
        #I"M HERE WORKING--NEED TO SET THE VALUE
            #NEXT -- put in add/remove programs and then create uninstaller
        
#the meat and potatoes
if ver == 64:
    sixty_folder()
    install()
elif ver == 32:
    thirty_folder()
    install()