# Python for Android Development HowTo
###### tags: `Python-for-Android` `Python` `Android` `Kivy`

----

## Introduction and Background
*    In convenience of porting already complete Python function/program to Android platform, we can use Python-for-Android to deploy Python program without Java programming.
*    We utilize Kivy, an open source Python module, to design our UI or Android service. 

## Environment for PC and testing Android platform
*    PC environment information

| Env. Info  | Content       |
| ------- | ------------- |
| Host OS | `Windows 8.1` |
| Guest OS | `Ubuntu 18.04 LTS` |
|  Virutal Machine       |     `VMWare Workstation Player 15`   |
|    CPU     |  `Intel Core i5-5200`  |
| CPU Arch.     |   `x86_64`            |

*    Android platform environment information

| Env. Info       | Content           |
| --------------- | ----------------- |
| Android version | `10`                |
| CPU             | `Qualcomm Kyro 260` |
| CPU Arch.       | `ARM64-v8a` |


## Develop Environment Buildup
*    First of all, install dependency kit in Ubuntu.
```shell
$ sudo apt-get install openjdk-8-jdk libffi-dev openssl zlib1g unzip autoconf automake libtool cmake python3 python3-pip python3-dev adb libglib2.0-dev
```
*    After installation finished, install Python module `virtualenv`
```shell
$ pip3 install virtualenv
```

*    Create a Python virtual environment via `virtualenv`
        *    This step is optional but suggested.
```shell
$ mkdir <your_project_name>
$ cd <your_project_name>
$ python3 -m venv <project_env_name>
$ echo \#\!bin/bash >> venv_init
$ echo -e "\nsource <project_env_name>/bin/activate" >> venv_init
$ echo \#\!bin/bash >> venv_exit
$ echo -e "\ndeactivate" >> venv_exit
```
*    Virtual environment start up and exit
```shell
$ source venv_init  # Start up
$ source venv_exit  # Exit environment
```
*    *After virtual environment is started up*, install dependency kit.
```shell
$ pip3 install virtualenv cython kivy python-for-android buildozer
$ p4a
usage: p4a [-h] [-v]
           {recommendations,recipes,bootstraps,clean_all,clean-all,clean_dists,clean-dists,clean_bootstrap_builds,clean-bootstrap-builds,clean_builds,clean-builds,clean,clean_recipe_build,clean-recipe-build,clean_download_cache,clean-download-cache,export_dist,export-dist,aar,apk,create,archs,distributions,dists,delete_dist,delete-dist,sdk_tools,sdk-tools,adb,logcat,build_status,build-status}
           ...

A packaging tool for turning Python scripts and apps into Android APKs
...
```
*    Then, we will install **Android cmd develop kit**.
        *    Please download command line tool from [Android Official](https://developer.android.com/studio#downloads).
        *    Please note that `sdkmanager --list` should NOT contain any **Java Exception**.
```shell
$ cd ~/
$ mkdir Android ; cd Android
$ unzip cmdtool*   # Please move your downloaded .zip file to here manually
$ mkdir cmdline-tools ; mv tools cmdline-tools
$ ln -s ./cmdline-tools/tools tools # for solving bug for Android cmd tools
$ export PATH="$HOME/Android/cmdline-tools/tools/bin:$HOME/Android/cmdline-tools/tools:$PATH“
$ sdkmanager --list
...

Available Packages:
  Path                                | Version      | Description                                                         
  -------                             | -------      | -------   
  add-ons;addon-google_apis-google-15 | 3            | Google APIs                                                         
  add-ons;addon-google_apis-google-16 | 4            | Google APIs                                                         
  add-ons;addon-google_apis-google-17 | 4            | Google APIs                                           
  add-ons;addon-google_apis-google-18 | 4            | Google APIs

...
```
*    After Android SDK manager is ready, we install Android tools for development and `p4a` usage.
        *    Necessary Tools: `platforms` `build-tools` `ndk`
        *    You can choose your tool version for customization. Don`t forget to change the correspond version of the tools.
        
```shell
$ sdkmanager "platforms;android-27"
$ sdkmanager "build-tools;28.0.2"
$ sdkmanager "ndk;20.1.5948944“
$ export ANDROIDSDK="$HOME/Android"
$ export ANDROIDNDK="$HOME/Android/ndk/20.1.5948944"
```
*    Add this two environment variable into script venv_init, to prevent missing export.
```shell
$ echo -e "export ANDROIDSDK="$HOME/Android"" >> venv_init
$ echo -e "export ANDROIDNDK="$HOME/Android/ndk/20.1.5948944"" >> venv_init
$ echo -e "unset ANDROIDSDK" >> venv_exit
$ echo -e "unset ANDROIDNDK" >> venv_exit
```
*    All of the environment buildup has finished. Try your first Python-for-Android App with Kivy !

#    Run your first APP on Android platform via P4A and Kivy
*    In very early testing step, I try this code for flow testing.
```Python
from kivy.app import App
from kivy.uix.label import Label

class HelloApp(App):
    def build(self):
        return Label(text="Hello Kivy, Hello Steven")
        
if __name__ == '__main__':
    myapp = HelloApp()
    myapp.run()
```
*    The directory for the source code is suggested to put in directory *src*, such as the example downward:
![dir_ex](https://i.imgur.com/AmiGSDB.png)
*    Test if the APP runs on PC environment with UI output.
```shell
$ python3 src/main.py
```
![exec_res](https://i.imgur.com/XC6vfwV.png)

*    Then, type the p4a command to generate apk file
        *    Don`t forget to change related parameter to fit CPU arch, Android version...etc.
        *    You can change package name, APP name, dist name and APP version in your favorite.
        *    First time packing apks takes about 30 to 60 minutes. Please wait paitently.
        
```shell
p4a apk --private ./src --requirements=python3,kivy \
        --bootstrap=sdl2 --arch=arm64-v8a --android_api=29 \
        --package=example.kivy.stch --name=Kivy_p4a_Test --dist_name=STCH_Kivy_Test \
        --release --version 0.0.2
```
![unsign_apk](https://i.imgur.com/wZBOg6Y.png)

*    After packing apk, p4a will output unsigned apk. Developer must sign it by jarsigner with keystore.

```shell
$ jarsigner -verbose -keystore <your_ks_name>.keystore -signedjar <signed_apk_filename><unsigned_apk_filename> <alias_name of the keystore> -storepass <passwd_of_keystore>
```

*    In first time signing apk, you should generate a keystore file before signing.
```shell
$ keytool -genkey -v -keystore <your_ks_name>.keystore -alias <ks_alias_name> -keyalg RSA -keysize 2048 -validity 10000
```
*    After signing the apk, the generated apk can be installed into Android platform.

![packed_apk](https://i.imgur.com/b225hY7.png)
*    APK can be instsalled via two methods
        *    Move apk file to Android platform and  install
        *    Install via adb command 
*    You should get the permission to allow install unauthorized apk if you want to install the apk via file moving. 
*    If you want to install apk via adb, you should open USB debugging and Android developor option.

```shell
$ adb install *.apk
...
Success
```

*    After installation finished, you can open the App and view up your first testing APP!

![exec_pic](https://i.imgur.com/PzfRMwx.png)


#    Manual for make commands
*    For the convenience of testing your App on the Android platform, I have written a `Makefile` to simplify the complex development process.


### `p4a` parameters
*    `p4a` APK packing tool includes lots of parameter, developer should input it while packing APK in every time.
*    So, I write a target `apk` in the Makefile to bring these parameters into the `p4a` automatically.
*    Guide for each parameter

| Parameter   | Description                              |
| ----------- | ---------------------------------------- |
| SRC         | Directory for the python source file     |
| REQUIREMENT | Required python module for runtime usage |
| PERMISSION  | APK permission input                     |
| BOOTSTRAP   | Bootstrap frontend framework name  |
| ARCH        | CPU architecture of the target platform  |
| ANDROAPI    | Android platform API version             |
| PKGNAME     | Packge Name of the APP                   |
| APPNAME     | APP name shown on the Android APP list |
| DISTNAME    | Distro Name (Output APK file name prefix)  |
| VERSION     | APP version No. |
*    Note of the parameter input:
        *    For multiple `REQUIREMENT` input, please divide each module with `,`
        *    For multiple `PERMISSION` input, please divide each permission with `WHITE_SPACE`
*    Example Input
```make
# p4a parameter example
SRC         := ./src
REQUIREMENT := python3,kivy,jnius,numpy,android
PERMISSION  := BLUETOOTH_ADMIN BLUETOOTH ACCESS_FINE_LOCATION FOREGROUND_SERVICE RECEIVE_BOOT_COMPLETED
BOOTSTRAP   := sdl2
ARCH        := arm64-v8a
ANDROAPI    := 29
PKGNAME     := example.kivy.stch
APPNAME     := Kivy_p4a_Test
DISTNAME    := STCH_Kivy_Test
VERSION     := 0.0.2
```

### `jarsigner` parameters
*    For the `jarsigner` parameter, please view up the guide downward:

| Parameter | Description        |
| --------- | ------------------ |
| KEYSTORE  | Keystore file name |
| KSALIAS   | Alias of Keystore file     |
| KSPASSWD  | Password of Keystore file  |
*    Note of the parameter input:
        *    If you do not set the `KSPASSWD` in Makefile or bring this parameter with cmd, you will need to input password of keystore by hand during apk singing.
*    Example input
```make
# jarsigner parameter example
KEYSTORE := stch.keystore
KSALIAS  := stch
KSPASSWD :=
```

### Introduction and example of the target

*    `all`: run apk packing and signing
        *    You cna input your keystore password here
```make
$ make KSPASSWD=xxxx
```
*    `deploy`: run apk packing, signing and installing
        *    Developer should connect to Android platform via `adb` first
```make
$ make deploy KSPASSWD=xxxx
```
*    `clean`: remove generated output *.apk and *.pyc file
```make
$ make clean
```
*    `layout`: run basic script to look-up the layout of UI
```make
$ make layout
```
*    `run`: execute `./src/main.py` for function testing.
        *    It may fail to run because of the execution platform is not Android.
```make
$ make run
```
*    `devlist`: list connected Android devices.
```make
$ make devlist
```
*    `devcn`: connect to Android device
```make
$ make devcn
```
*    `devrc`: reconnect the Android device
```make
$ make devrc
```
*    `devdc`: disconnect the Android device
```make
$ make devdc
```
# Bluetooth Scan Function Testing
*    With `pyjnius` module, we can access Java class `BluetoothAdapter` in Python code.
*    In my testing APP layout, I plan two buttons function related to bluetooth.
        *    Left button for getting bluetooth status.
        *    Right button for start bluetooth scanning.
*    Callback for the implementation of two functions
        *    Getting Status: [getbthstat](https://github.com/StevenChen8759/P4A_devtest/blob/b9237e183e0333f74127400c2b0f98e00f812231/src/main.py#L59)
        *    Getting Status: [scanbthdevs](https://github.com/StevenChen8759/P4A_devtest/blob/b9237e183e0333f74127400c2b0f98e00f812231/src/main.py#L73)

*    Don`t forget to add permission downward in the [Makefile](https://github.com/StevenChen8759/P4A_devtest/blob/b9237e183e0333f74127400c2b0f98e00f812231/Makefile#L5) to get related bluetooth function permission
        *    BLUETOOTH
        *    BLUETOOTH_ADMIN
        *    ACCESS_FINE_LOCATION
*    Run `make deploy` to look-up the result on your Android platform!

# Android Service in Python-for-Android
*    Two methods to add service into the APK:
        *    Via Service Folder
        *    Via Arbitrary service scripts
###    Service Folder
*    With this method, developer should put the service python code in `service\main.py`.

![Serv_folder](https://i.imgur.com/9dNZFip.png)

*    Then, add service launch function call in the button_click event callback in `./src/main.py`:
```python=91
android.start_service(title='Stch', description='Steven Chen Socket Testing...')
```

*    After service is launched, you can use `logcat` command in `adb shell` to view-up service runtime output by `print()`.
```python
# Content in the Python Service (./src/service/main.py)
print("Hello world from Android Background Service...")
```
![logcat_res](https://i.imgur.com/3dEH735.png)


###    Arbitary Service Script
*    This method allows user add their service scripts (one or more) with specific name.
*    Service with different name can assign different Python file as the function of the service.
        *    Developer should declare it in `p4a` input, including service name and correspond python file.
        *    It is suggested that the all alphas in `p4a` service name declaration is lowercase.

```Makefile=32
p4a apk --private $(SRC) --requirements=$(REQUIREMENT) \
$(patsubst %,--permission=% ,$(PERMISSION))\

--service=stchservice:serv.py --service=testserv:test.py\

--bootstrap=$(BOOTSTRAP) --arch=$(ARCH) --android_api=$(ANDROAPI) \
--package=$(PKGNAME) --name=$(APPNAME) --dist_name=$(DISTNAME) \
--release --version $(VERSION)
```
![file_dis](https://i.imgur.com/6GKbbXD.png)

*    For launching service `stchservice` and `testserv`, developer should access this activity via `Pyjnius` module.
        *    Service Class Name: `autoclass('<PKGNAME>.Service<ServiceName>')`
        *    Cooperate with `org.kivy.android.PythonActivity`

*    Example of service launching code in the callback of button clicked.
        *    Please note that the first alpha of <ServiceName> in `<PKGNAME>.Service<ServiceName>` should be uppercase, and the other alpha should be lowercase.
```python=92
service = autoclass('example.kivy.stch.ServiceTestserv')
mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
serv = autoclass('example.kivy.stch.ServiceStchservice')
mact = autoclass('org.kivy.android.PythonActivity').mActivity
argument = ''
service.start(mActivity, argument)
serv.start(mact, argument)
```

*    After deploying the APP, look-up service runtime output via `logcat` in `adb shell`

![Run_testserv](https://i.imgur.com/YyFsEFI.png)

![run_stchservice](https://i.imgur.com/KJIqs0Q.png)

*    If you want to make service restart automatically, you can set `AutoRestartService` via `mActivity` API:
```python
from jnius import autoclass
PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)
```

# Reference
*    https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/
*    https://medium.com/@k1992313/python-for-android-%E8%B8%A9%E9%9B%B7%E5%BF%83%E5%BE%97-f07ac9c106ac
*    https://stackoverflow.com/questions/60440509/android-command-line-tools-sdkmanager-always-shows-warning-could-not-create-se
*    https://python-for-android.readthedocs.io/en/latest/quickstart/#installing-android-sdk
*    https://stackoverflow.com/questions/3997748/how-can-i-create-a-keystore
*    https://kknews.cc/zh-tw/tech/yxlvj.html
*    https://stackoverflow.com/questions/36740840/jarsigner-please-specify-alias-name-but-i-did
*    https://python-for-android.readthedocs.io/en/latest/services/
