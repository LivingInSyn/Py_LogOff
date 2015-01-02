#import json
#from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
#from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
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
	def build(self):
		self.logout_times = Logout_Time(name='logout')
		self.transition = SlideTransition(duration=.35)
		root = ScreenManager(transition=self.transition)
		root.add_widget(self.logout_times)
		Window.bind(on_close=self.window_closed)
		return root
		
	def set_time(self,time):
		self.time = time
		if self.time==45:
			self.time = self.time*60
			Window.close()
		elif self.time==1:
			self.time = self.time*3600
			self.time = 7
			Window.close()
		elif self.time==2:
			self.time = self.time*3600
			Window.close()
		elif self.time==3:
			self.time = self.time*3600
			Window.close()
			
		
	'''def on_stop(self):
		print("I CLOSED")
		subprocess.Popen(['notepad.exe','test.txt'])
	'''
	
	def window_closed(self, event):
		print("window closed")
		time.sleep(self.time)
		subprocess.Popen(["shutdown.exe","/l"])
		exit()

if __name__ == '__main__':
	Logout_App().run()
