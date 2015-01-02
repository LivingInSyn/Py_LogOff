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
import subprocess
import time



class Logout_Time(Screen):
	
	data = ListProperty()
	
	def args_converter(self, row_index, item):
		return {
			'note_index': row_index,
			'note_content': item['content'],
			'note_title': item['title']}


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
		return root
		
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
			
	
	def window_closed(self, event):
		print("window closed")
		if self.time==0:
			#pass
			'''This Next line will have to change to the exe once it's made. It's to relaunch the app if someone closes
			it, forcing them to enter a time'''
			subprocess.Popen(["C:\uits\Kivy-1.8.0-py2.7-win32\kivy.bat","C:\Users\student1953\Documents\GitHub\Py_LogOff\main.py"])
		else:
			time.sleep(self.time)
			subprocess.Popen(["shutdown.exe","/l"])
		exit()

if __name__ == '__main__':
	Logout_App().run()
