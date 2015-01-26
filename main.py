'''
Created by Jeremy Mill, originally for use in the hi tech classrooms at the University of CT

Licensed under the GPLv3

jeremymill@gmail.com
github.com/livinginsyn
'''

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



class Logout_Time(Screen):
    pass
    
    '''data = ListProperty()
    
    def args_converter(self, row_index, item):
        return {
            'note_index': row_index,
            'note_content': item['content'],
            'note_title': item['title']}'''
            
class Custom_Time(Screen):
    pass
    
class Angry_Custom_Time(Screen):
    pass


class Logout_App(App):

    '''set the window title and the icon here''' ''' '''
    icon = 'myicon.ico'    
    def build(self):
        self.icon = 'myicon.ico'
        self.title = 'HTC Logoff Utility'
        self.logout_times = Logout_Time(name='logout')
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.logout_times)
        '''make the close window binding and initialize self.time to 0'''
        Window.bind(on_close=self.window_closed)
        self.time = 0
        self.no_choice = 1
        self.auto_time = 3600
        #self.auto_time = 10
        test = "test"
        self.no_input_timer = threading.Thread(target=self.left_open,args=())
        self.no_input_timer.start()
        return root
        
    def left_open(self):
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
        
    def set_time(self,time):
        config = self.config
        self.time = time
        if self.time==45:
            self.time = self.time*60
            #next line is for debugging
            #self.time = 0
            self.no_choice = 0
            Window.close()
        elif self.time==1:
            self.time = self.time*3600
            #next line is for debugging
            #self.time = 7
            Window.close()
        elif self.time==2:
            self.time = self.time*3600
            Window.close()
        elif self.time==3:
            self.time = self.time*3600
            Window.close()
            
    def custom_time(self,hours,minutes):
        if hours == "":
            hours = 0
        if minutes == "":
            minutes = 0
        try:
            hours = int(hours)
            minutes = int(minutes)
            print(hours)
            print(minutes)
        except ValueError:
            self.angry_custom()
        self.time = (hours * 3600)+(minutes * 60)
        Window.close()
        
            
    def call_custom(self):
        #remove logout
        if self.root.has_screen('logout'):
            self.root.remove_widget(self.root.get_screen('logout'))
            
        view = Custom_Time(name='cutom_time')
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name
        
    def angry_custom(self):
        print('called angry custom')
        if self.root.has_screen('custom_time'):
            self.root.remove_widget(self.root.get_screen('custom_time'))
        view = Angry_Custom_Time(name='angry_custom')
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name
        
    def custom_back(self):
        if self.root.has_screen('custom_time'):
            self.root.remove_widget(self.root.get_screen('custom_time'))
        
        self.root.add_widget(self.logout_times)
        self.transition.direction = 'right'
        self.root.current = self.logout_times.name
            
    
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

if __name__ == '__main__':
    Logout_App().run()
