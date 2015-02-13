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


#Try and open the counter file, if it fails for some reason, assume run = 2
try:
    f = open('counterfile','r')
    run = int(f.read())
except IOError:
    run=2


class warning_time(Screen):
    pass
    
class Logout_Time(Screen):
    pass
    
class Custom_Time(Screen):
    pass

class Angry_Custom_Time(Screen):
    pass
    
class warning_App(App):
    icon = 'myicon.ico'
    
    def build(self):
        #set the icon/title/create the warning_times object
        self.icon = 'myicon.ico'
        self.title = 'HTC Logoff Utility'
        self.warning_times = warning_time(name='warning')
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
        return root
        
    def unattended_warning(self):
        #this function logs off if you ignore the warning after 5 minutes
        while self.no_choice == 1:
            time.sleep(1)
            print("running left open")
            if self.auto_time == 0:
                self.time = 1
                Window.close()
            else:
                self.auto_time -= 1
    
    def build_config(self,config):
        #pretty sure this can go away, but not yet
        Config.set('graphics','height',480)
        Config.set('graphics','width',800)
        Config.write()
        #Config.update_config('config.ini',overwrite=True)
        
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
        f = open('counterfile','w')
        f.write(str(run-1))
        f.close()
        
    def window_closed(self, event):
        print("window closed")
        if self.time==0:
            #pass
            '''This Next line will have to change to the exe once it's made. It's to relaunch the app if someone closes
            it, forcing them to enter a time'''
            
            #NOTE! The no choice thread is still running even if we relaunch here!
            subprocess.Popen(["C:\uits\warning.exe"])
            
        else:
            self.decrease_counter()
            time.sleep(self.time)
            subprocess.Popen(["C:\uits\warning.exe"])
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
