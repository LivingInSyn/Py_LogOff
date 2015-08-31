'''
Created by Jeremy Mill, originally for use in the hi tech classrooms at the University of CT

Licensed under the GPLv3

jeremymill@gmail.com
github.com/livinginsyn
'''



#run the config first to properly size the window
from kivy.config import Config

Config.set('graphics','height',480)
Config.set('graphics','width',800)
Config.set('input','mouse','mouse,disable_multitouch')
Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
import subprocess
import time
import threading
import os.path
import os
import sys
import ConfigParser
import getpass
import ldap
#next line disables cert checking, which is OK because we query only
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)


#Try and open the counter file, if it fails for some reason, assume run = 2
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
try:
    #save_path = 'c:\\uits\\'
    filename=os.path.join(application_path,"counterfile")
    f = open(filename,'r')
    run = int(f.read())
except IOError:
    run=2


class warning_time(Screen):
    #pass
    def change_banner(self,image):
        self.ids.banner_image.source = image
        
    def set_username(self,name):
        #HERE IS THE SET TEXT METHOD!!
        self.ids.Text_label.text = name + " is the currently logged in user.\nIf this is you and you need 5 more minutes, select 5 more minutes below.\nOtherwise, select \'Logout Now\' and login with your account."
    
class Logout_Time(Screen):
    pass
    
class Custom_Time(Screen):
    pass

class Angry_Custom_Time(Screen):
    pass
    
class warning_App(App):
    icon = 'myicon.ico'
    
    def build(self):
        #get the current directory
        self.path = self.find_current_dir()
        #set the icon/title/create the warning_times object
        self.icon = 'myicon.ico'
        self.title = 'HTC Logoff Utility'
        self.warning_times = warning_time(name='warning')
        self.warning_times.set_username(self.get_username())
        self.transition = SlideTransition(duration=.35)
        #create the screen manager and add warning times to it
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.warning_times)
        '''make the close window binding and initialize self.time to 0'''
        Window.bind(on_close=self.window_closed)
        self.time = 0
        #no choice = 2 tells it that warning is running, not logout_app
        self.no_choice = 1
        self.auto_time = 300
        #self.auto_time = 10
        self.no_input_timer = threading.Thread(target=self.unattended_warning,args=())
        self.no_input_timer.start()
        #run the config reader and change the banner
        self.read_config()
        self.warning_times.change_banner(self.banner_image)
        
        return root
        
    def unattended_warning(self):
        #this function logs off if you ignore the warning after 5 minutes
        while self.no_choice == 1:
            time.sleep(1)
            print("running left open")
            if self.auto_time == 0:
                self.time = 1
                #Window.close()
                subprocess.Popen(["shutdown.exe","/l"])
                #os.system("shutdown.exe /l")
            else:
                self.auto_time -= 1
    
    def build_config(self,config):
        #pretty sure this can go away, but not yet
        Config.set('graphics','height',480)
        Config.set('graphics','width',800)
        Config.write()
        
    def read_config(self):
        #create the config object
        config = ConfigParser.ConfigParser()
        
        #create the path to the config file and read it. The config file needs to be in the same directory as the exe/main.py
        config_path = os.path.join(self.path,"logoff_config.cfg")
        config.read(config_path)
        
        #get the banner config 
        self.banner_image = config.get('Banner','image',0)
    
    def extend_time(self):
        #if someone selects give me 5 more minutes
        config = self.config
        self.no_choice = 0
        self.time = 300
        Window.close()
        
    def logout_now(self):
        #if someone selects log out now, this should just log them out
        config = self.config
        self.no_choice = 0
        self.time = 3
        subprocess.Popen(["shutdown.exe","/l"])
        
    def decrease_counter(self):
        #save_path = 'c:\\uits\\'
        filename=os.path.join(self.path,"counterfile")
        f = open(filename,'w')
        f.write(str(run-1))
        f.close()
        
    def find_current_dir(self):
        #found this on Stack Overflow, returns the correct current working directory for exe's or py files
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path
        
    def get_username(self):
        netid = getpass.getuser()
        result = None

        try:
            l = ldap.initialize('ldaps://ldap.uconn.edu:636')
            result = l.search_st('uid={0},ou=people,dc=uconn,dc=edu'.format(netid), ldap.SCOPE_SUBTREE, 'objectClass=*', None)
        except ldap.LDAPError as error:
            return netid
            
        returnedName = result[0][1]['displayName'][0]
        last_first = returnedName.replace(' ','').split(',')
        
        if len(last_first) > 1:
            username = last_first[1] + " " + last_first[0]
        else:
            username = last_first[0]
        
        return username
        
        
    def window_closed(self, event):
        print("window closed")
        if self.time==0:
            #pass
            '''This Next line will have to change to the exe once it's made. It's to relaunch the app if someone closes
            it, forcing them to enter a time'''
            
            #NOTE! The no choice thread is still running even if we relaunch here!
            executable_name = os.path.join(self.path,"warning.exe")
            subprocess.Popen([executable_name])
            
        else:
            self.decrease_counter()
            time.sleep(self.time)
            executable_name = os.path.join(self.path,"warning.exe")
            subprocess.Popen([executable_name])
            #subprocess.Popen(["shutdown.exe","/l"])
            #print("would've logged out")
            exit()
        #make sure we exit so that we can relaunch
        exit()

if __name__ == '__main__':
    if run>0:
        warning_App().run()   
    else:
        subprocess.Popen(["shutdown.exe","/l"])
