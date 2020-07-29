# Python for Android with Kivy Testing...
# Testing term 1: Bluetooth Scan
# Testing term 2: Android Service Auto Start / Boot Start
# Testing term 3: numpy operation testing
# This code is written by Steven HH Chen

# UI import
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# Other import
import numpy as np
import sys, traceback, time

# Note: inherit class App!, Add __ function prefix to make it private
# Note: App, Builder, Layout can be polymorphism
class TestApp(App):
	def build(self):
		ui = Builder.load_file("layout.kv")
		return ui

if __name__=="__main__":
	myapp = TestApp()
	myapp.run()
