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
| Android version | 10                |
| CPU             | `Qualcomm Kyro 260` |
| CPU Arch.       | `ARM64-v8a` |


## Develop Environment Buildup
*    First of all, install dependency kit in Ubuntu.
```shell
$ sudo apt-get install openjdk-8-jdk libffi-dev openssl zlib1g unzip autoconf automake libtool cmake python3 python3-pip adb
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
*    After virtual environment is started up, install dependency kit.
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
        *    Please note that `sdkmanager --list` should NOT contain any ==Java Exception==.
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
        *    You can choose your tool version for customization.
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

#    Manual for make commands
*    For the convenience of testing your App on the Android platform, I have written a `Makefile` to simplify the complex development process.

#    Build-up your first APP

# Reference
*    https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/
*    https://medium.com/@k1992313/python-for-android-%E8%B8%A9%E9%9B%B7%E5%BF%83%E5%BE%97-f07ac9c106ac
*    https://stackoverflow.com/questions/60440509/android-command-line-tools-sdkmanager-always-shows-warning-could-not-create-se
*    https://python-for-android.readthedocs.io/en/latest/quickstart/#installing-android-sdk
*    https://stackoverflow.com/questions/3997748/how-can-i-create-a-keystore
*    https://kknews.cc/zh-tw/tech/yxlvj.html
*    https://stackoverflow.com/questions/36740840/jarsigner-please-specify-alias-name-but-i-did
