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

# Pyjnius import and Autoclass declaration
from jnius import autoclass
#from android.broadcast import BroadcastReceiver

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')


# Other import
import numpy as np
import sys, traceback, time

# Note: inherit class App!, Add __ function prefix to make it private
# Note: App, Builder, Layout can be polymorphism
class TestApp(App):
	lb = None
	scanbutt=None
	def build(self):
		ui = Builder.load_file("layout.kv")
		self.lb = ui.ids['stat']
		self.scanbutt = ui.ids['scanbutt']
		return ui

	def test(self):
		self.__infoshow("Info","Test")

	def nptest(self):
		#----------- Declaration ------------
		ax = np.array([[1,2,3],[4,5,6]],dtype = np.int)
		self.__nparr_info("Basic Array Declaration - ax", ax)
		self.__nparr_info("np.zeros((3,4))", np.zeros((3,4)))
		self.__nparr_info("np.ones((3,4), int16)", np.ones((3,4),dtype = np.int16))
		self.__nparr_info("np.empty((3,4))", np.empty((3,4)))
		self.__nparr_info("np.arange(10,20,2)", np.arange(10,20,2))
		self.__nparr_info("np.arange(12).reshape(3,4)", np.arange(12).reshape(3,4))
		self.__nparr_info("np.linspace(1,10,5)", np.linspace(1,10,5))
		self.__nparr_info("np.linspace(1,10,6).reshape(2,3)", np.linspace(1,10,6).reshape(2,3))

		#------------ Basic OPs -----------

	def getbthstat(self):
		try:
			self.lb.text = "Already get default adapter, now you can scan the devs."
			adapter = BluetoothAdapter.getDefaultAdapter()
			if adapter != None:
				self.bthad=adapter
				self.scanbutt.disabled=False
			adinfo = "Name: %s \n Enabled: %s\n Address: %s \n Discovering: %s\n(Stat,Scan) Code: (%d,%d)" % (
                      adapter.getName(), str(adapter.isEnabled()), adapter.getAddress(),
                      str(adapter.isDiscovering()), adapter.getState(), adapter.getScanMode())
			self.__infoshow("Default Adapter", adinfo)
		except Exception as ex:
			self.__exshow(ex)


	def __nparr_info(self, npmsg, nparr):
		st = "content:\n %s \n______\ndim: %s \nshape: %s \nsize: %s \ndtype: %s" % (
			 str(nparr), str(nparr.ndim), str(nparr.shape),
			 str(nparr.size), str(nparr.dtype))
		self.__infoshow(npmsg, st)

	def __exshow(self, exobj):
		error_class = exobj.__class__.__name__
		detail = exobj.args[0]
		cl, exc, tb = sys.exc_info()
		lastCallStack = traceback.extract_tb(tb)[-1]
		fileName = lastCallStack[0]
		lineNum = lastCallStack[1]
		funcName = lastCallStack[2]
		exinfo = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
		self.__infoshow("ERROR!!!!! Python Exception!!!!!", exinfo)

	def __infoshow(self, msgtitle, msg):
		sl = StackLayout(size=(550, 550), orientation='bt-rl')
		butt = Button(text='Back', size_hint=(.20,.10))
		sl.add_widget(butt)
		lb = Label(text=msg, text_size=(300,400))
		sl.add_widget(lb)
		popup = Popup(title=msgtitle, content=sl, size_hint=(None, None), size=(600, 600))
		butt.on_release = popup.dismiss
		popup.open()

if __name__=="__main__":
	myapp = TestApp()
	myapp.run()
