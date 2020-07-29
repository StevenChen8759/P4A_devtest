# Python for Android with Kivy Testing...
# Testing term 1: Bluetooth Scan
# Testing term 2: Android Service Auto Start / Boot Start
# Testing term 3: numpy operation testing
# This code is written by Steven HH Chen

# UI import
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color, Rectangle

# Other import
import numpy as np
import sys, traceback, time

# Note: inherit class App!, Add __ function prefix to make it private
# Note: App, Builder, Layout can be polymorphism
class TestApp(App):
	def build(self):
		ui = Builder.load_file("layout.kv")
		return ui

	def test(self):
		self.__infoshow("Info","Test")

	def __infoshow(self, msgtitle, msg):
		sl = StackLayout(size=(400, 400), orientation='bt-rl')
		butt = Button(text='Back', size_hint=(.20,.10))
		sl.add_widget(butt)
		lb = Label(text=msg, text_size=(200,200))
		sl.add_widget(lb)
		popup = Popup(title=msgtitle, content=sl, size_hint=(None, None), size=(400, 400))
		butt.on_release = popup.dismiss
		popup.open()

if __name__=="__main__":
	myapp = TestApp()
	myapp.run()
