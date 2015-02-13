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



class Logout_Time(Screen):
    
    #change the buttons to their correct text values
    def change_buttons(self,buttonlist):
        self.ids.button1.text = buttonlist.pop()
        self.ids.button2.text = buttonlist.pop()
        self.ids.button3.text = buttonlist.pop()
        self.ids.button4.text = buttonlist.pop()
        #time.sleep(7)
        
    
    #pass

            
class Warning_Time(Screen):
    pass
            
class Custom_Time(Screen):
    pass
    
class Angry_Custom_Time(Screen):
    pass


class Logout_App(App):

    '''set the window title and the icon here''' ''' '''
    icon = 'myicon.ico'    
    def build(self):
        
        self.button_config()
        #init the counter file
        self.counter_file()
        
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
        
        #start the one hour no input timer
        self.no_input_timer = threading.Thread(target=self.left_open,args=())
        self.no_input_timer.start()
        
        #get the button text and times
        self.button_config()
        self.logout_times.change_buttons(self.button_list)
        
        return root
        
    def counter_file(self):
        f=open('counterfile','w')
        f.write('3')
        f.close()
        
    def button_config(self):
        config = ConfigParser.ConfigParser()
        #for some reason, kivy on windows needs the absolute path
        #I will have the change this around later when I compile
        
        #for windows:
        #config.read('C:\\Users\\student1953\\Documents\\GitHub\\Py_LogOff\\logoff_config.cfg')
        #for *nix
        config.read('logoff_config.cfg')
        
        #grab the text from the buttons, put it into a list and reverse it, so it can be sent to logout_times
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
        
    def set_time(self,button):
        #config = self.config
        #self.time = time
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
        
        #self.time = self.time*60
        #Window.close()
            
    def custom_time(self,hours,minutes):
        good = 0
        if hours == "":
            hours = 0
        if minutes == "":
            minutes = 0
        try:
            hours = int(hours)
            minutes = int(minutes)
            if hours !=0:
                if hours < 8:
                    good = 1
            else:
                if minutes !=0:
                    if minutes < 59:
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
            #pass
            '''This Next line will have to change to the exe once it's made. It's to relaunch the app if someone closes
            it, forcing them to enter a time'''
            subprocess.Popen(["C:\uits\HTC-LogOut.exe"])
            #print("called self.stop")   
        else:
            #sleep until it's time to call a 5 minute warning
            
            time.sleep(self.time)
            subprocess.Popen(["C:\uits\warning.exe"])
            
            #for debuggin on *nix
            #subprocess.Popen(["python","/home/bobo/Documents/programming/Py_LogOff/warning/warning.py"])
            
            
        #make sure we exit
        exit()
        
          
if __name__ == '__main__':
    Logout_App().run()
