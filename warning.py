from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
import subprocess
import time
import threading


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
        self.icon = 'myicon.ico'
        self.title = 'HTC Logoff Utility'
        self.warning_times = warning_time(name='warning')
        self.transition = SlideTransition(duration=.35)
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
        while self.no_choice == 1:
            time.sleep(1)
            #print("running left open")
            if self.auto_time == 0:
                self.time = 1
                Window.close()
            else:
                self.auto_time -= 1
    
    def build_config(self,config):
        Config.set('graphics','height',480)
        Config.set('graphics','width',800)
        Config.write()
        #Config.update_config('config.ini',overwrite=True)
        
    def extend_time(self):
        config = self.config
        self.time = 300
        Window.close()
        
    def logout_now(self):
        config = self.config
        self.time = 3
        Window.close()
        
    def window_closed(self, event):
        print("window closed")
        if self.time==0:
            #pass
            '''This Next line will have to change to the exe once it's made. It's to relaunch the app if someone closes
            it, forcing them to enter a time'''
            subprocess.Popen(["C:\uits\HTC-LogOut.exe"])
        else:
            time.sleep(self.time)
            #subprocess.Popen(["shutdown.exe","/l"])
            print("would've logged out")
            exit()
        exit()
