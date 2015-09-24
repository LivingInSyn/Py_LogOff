'''
Created by Jeremy Mill, originally for use in the hi tech classrooms at the University of CT

Licensed under the GPLv3

jeremymill@gmail.com
github.com/livinginsyn
'''


#put the graphics stuff up here so it'll change
from kivy.config import Config
Config.set('graphics','height',480)
Config.set('graphics','width',800)
Config.set('input','mouse','mouse,disable_multitouch')
Config.write()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
import subprocess
import time
import threading
import ConfigParser
import os.path
import os
import sys


class Logout_Time(Screen):
    '''This is the main screen class that loads on start'''
    #change the buttons to their correct text values
    def change_buttons(self,buttonlist):
        self.ids.button1.text = buttonlist.pop()
        self.ids.button2.text = buttonlist.pop()
        self.ids.button3.text = buttonlist.pop()
        self.ids.button4.text = buttonlist.pop()
    
    def change_banner(self,image):
        self.ids.banner_image.source = image

        
class Warning_Time(Screen):
    '''stub, defined in KV file'''
    pass
            
class Custom_Time(Screen):
    '''stub, defined in KV file'''
    pass
    
class Angry_Custom_Time(Screen):
    '''stub, defined in KV file'''
    pass


class Logout_App(App):
    
    def build(self):
        
        #get the app_path
        self.path = self.find_current_dir()
        
        #init the counter file
        self.counter_file()
        #set the icon and title
        self.icon = 'myicon.ico'
        self.title = 'HTC Logoff Utility'
        #make the first screen, slide transition, screenmanager and add it to the root
        self.logout_times = Logout_Time(name='logout')
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.logout_times)
        #make the close window binding and initialize self.time to 0
        Window.bind(on_close=self.window_closed)
        self.time = 0
        self.no_choice = 1
        self.auto_time = 3600
                
        #start the one hour no input timer
        self.no_input_timer = threading.Thread(target=self.left_open,args=())
        self.no_input_timer.start()
        
        #get the button text and times
        self.read_config()
        self.logout_times.change_buttons(self.button_list)
        #banner change
        self.logout_times.change_banner(self.banner_image)
               
        return root
        
    def counter_file(self):
        #this is the file that lets us know how many times warning has left to be called
        #need to call it before warning does
        filename=os.path.join(self.path,"counterfile")
        f=open(filename,'w')
        f.write('3')
        f.close()
        
        
    def read_config(self):
        #create the config object
        config = ConfigParser.ConfigParser()
        
        #create the path to the config file and read it. The config file needs to be in the same directory as the exe/main.py
        config_path = os.path.join(self.path,"logoff_config.cfg")
        config.read(config_path)
        
        #grab the text from the buttons, put it into a list and reverse it, so it can be sent to logout_times
        '''this needs to be cleaned up and placed into a loop'''
        self.button1_text = config.get('Buttons','time_1',0)
        self.button2_text = config.get('Buttons','time_2',0)
        self.button3_text = config.get('Buttons','time_3',0)
        self.button4_text = config.get('Buttons','time_4',0)
        self.button_list = []
        self.button_list.append(self.button1_text)
        self.button_list.append(self.button2_text)
        self.button_list.append(self.button3_text)
        self.button_list.append(self.button4_text)
        self.button_list.reverse()
        #now grab the times for each of the buttons and cast as ints
        self.button1_time = int(config.get('Times','time_1',0))
        self.button2_time = int(config.get('Times','time_2',0))
        self.button3_time = int(config.get('Times','time_3',0))
        self.button4_time = int(config.get('Times','time_4',0))
        #get the banner config 
        self.banner_image = config.get('Banner','image',0)
        
    def find_current_dir(self):
        #returns the correct current working directory for exe's or py files
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        return application_path
              
    def left_open(self):
        #this function runs in a sep. thread and closes the window after one hour if left open
        while self.no_choice == 1:
            time.sleep(1)
            #print("running left open")
            if self.auto_time == 0:
                self.time = 1
                Window.close()
            else:
                self.auto_time -= 1
        
    def set_time(self,button):
        #sets the times for the buttons based off of the config file
        '''This needs to be cleaned up'''
        self.no_choice = 0
        if button==1:
            self.time = self.button1_time*60
            Window.close()
        elif button==2:
            self.time = self.button2_time*60
            Window.close()
        elif button==3:
            self.time = self.button3_time*60
            Window.close()
        elif button==4:
            self.time = self.button4_time*60
            Window.close()
            
    def custom_time(self,hours,minutes):
        #This is the test for custom time. We need to make sure that custom time isn't 0,0 and to make sure that it meets
        #the criteria we defined as the maximum time. This needs to be added to the configuration file as well
        good = 0
        if hours == "":
            hours = 0
        if minutes == "":
            minutes = 0
        try:
            hours = int(hours)
            minutes = int(minutes)
            if hours !=0:
                if hours <= 8 and minutes < 60 and minutes >= 0 :
                    good = 1
            else:
                if minutes !=0 and minutes < 60 and minutes >= 0:
                    good = 1
        except ValueError:
            #print("calling angry custom from except")
            self.angry_custom()
        if good==1:
            self.time = (hours * 3600)+(minutes * 60)
            self.no_choice = 0
            Window.close()
        else:
            self.angry_custom()
               
    def call_custom(self):
        '''This calls the custom time class'''
        #remove logout
        if self.root.has_screen('logout'):
            self.root.remove_widget(self.root.get_screen('logout'))
            
        #create the custom time view and add it to the screen manager
        view = Custom_Time(name='cutom_time')
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name
        
    def angry_custom(self):
        #If someone enters a bad time, remove regular custom_time and replace it with a new angry_custom
        if self.root.has_screen('custom_time'):
            self.root.remove_widget(self.root.get_screen('custom_time'))
        view = Angry_Custom_Time(name='angry_custom')
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name
        
    def custom_back(self):
        #if someone selects back, remove the current screen and replace it with logout_times
        if self.root.has_screen('custom_time'):
            self.root.remove_widget(self.root.get_screen('custom_time'))
        elif self.root.has_screen('angry_costom'):
            self.root.remove_widget(self.root.get_screen('angry_custom'))
        
        self.root.add_widget(self.logout_times)
        self.transition.direction = 'right'
        self.root.current = self.logout_times.name
            
    
    def window_closed(self, event):
        #called on the close of a window
        if self.time==0:
            '''This Next line will have to change to the exe once it's made. It's to relaunch the app if someone closes
            it, forcing them to enter a time'''
            executable_name = os.path.join(self.path,"HTC-LogOut.exe")
            subprocess.Popen([executable_name])   
        else:
            #sleep until it's time to call a 5 minute warning
            time.sleep(self.time)
            executable_name = os.path.join(self.path,"warning.exe")
            subprocess.Popen([executable_name])
        #make sure we exit
        exit()
        
          
if __name__ == '__main__':
    Logout_App().run()
