# Python for Android with Kivy Testing...
# Testing term 1: Bluetooth Scan
# Testing term 2: Android Service Auto Start / Boot Start
# Testing term 3: numpy operation testing
# This code is written by Steven HH Chen

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.label import Label

# Note: inherit class App!, Add __ function prefix to make it private
# Note: App, Builder, Layout can be polymorphism
class TestApp(App):
	def build(self):
		ui = Builder.load_file("layout.kv")
		return ui

if __name__=="__main__":
	myapp = TestApp()
	myapp.run()
