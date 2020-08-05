#--------------------------------------------------------------------------------
# p4a parameter
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

#--------------------------------------------------------------------------------
# jarsigner parameter
KEYSTORE := stch.keystore
KSALIAS  := stch
KSPASSWD :=

#--------------------------------------------------------------------------------
# default action and settings
all: apk sign

deploy: apk sign install

.PHONY: clean

#--------------------------------------------------------------------------------
# apk packing, signing, and installing

apk:
	p4a apk --private $(SRC) --requirements=$(REQUIREMENT) \
        $(patsubst %,--permission=% ,$(PERMISSION))\
        --service=StchService:serv.py \
        --bootstrap=$(BOOTSTRAP) --arch=$(ARCH) --android_api=$(ANDROAPI) \
        --package=$(PKGNAME) --name=$(APPNAME) --dist_name=$(DISTNAME) \
        --release --version $(VERSION)

sign:
ifdef KSPASSWD
	jarsigner -verbose -keystore $(KEYSTORE) -signedjar $(DISTNAME)_v$(VERSION).apk \
                  $(DISTNAME)__$(ARCH)-release-unsigned-$(VERSION)-.apk $(KSALIAS) -storepass $(KSPASSWD)
else
	jarsigner -verbose -keystore $(KEYSTORE) -signedjar $(DISTNAME)_v$(VERSION).apk \
                  $(DISTNAME)__$(ARCH)-release-unsigned-$(VERSION)-.apk $(KSALIAS)
endif
	@echo "Auto remove unsigned apk file, file name: $(DISTNAME)__$(ARCH)-release-unsigned-$(VERSION)-.apk"
	@rm -f $(DISTNAME)__$(ARCH)-release-unsigned-$(VERSION)-.apk

install: devcn
	@echo "Install Apk to the Android device via adb, Please ensure the connection of the device"
	adb install $(DISTNAME)_v$(VERSION).apk

# App interface layout viewup
layout:
	python3 scripts/layout.py

# App runtime testing
run:
	python3 src/main.py

#--------------------------------------------------------------------------------
# adb manipulation

# device list
devlist:
	adb devices

# device connect
devcn: devlist

# device reconnect
devrc: devdc devlist

# device disconnect
devdc:
	adb kill-server

#--------------------------------------------------------------------------------

clean:
	rm *.apk src/*.pyc

