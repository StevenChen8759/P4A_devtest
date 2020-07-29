SRC         := ./src
REQUIREMENT := python3,kivy,jnius,numpy
PERMISSION  := BLUETOOTH_ADMIN, BLUETOOTH, ACCESS_FINE_LOCATION
BOOTSTRAP   := sdl2
ARCH        := arm64-v8a
ANDROAPI    := 29
PKGNAME     := example.kivy.stch
APPNAME     := Kivy_p4a_Test
DISTNAME    := STCH_Kivy_Test
VERSION     := 0.0.2

KEYSTORE := stch.keystore
KSALIAS  := stch
KSPASSWD :=

all: apk sign install

.PHONY: clean

#--------------------------------------------------------------------------------

apk:
	p4a apk --private $(SRC) --requirements=$(REQUIREMENT) \
        --permission=BLUETOOTH_ADMIN  --permission=BLUETOOTH --permission=ACCESS_FINE_LOCATION \
        --bootstrap=$(BOOTSTRAP) --arch=$(ARCH) --android_api=$(ANDROAPI) \
        --package=$(PKGNAME) --name=$(APPNAME) --dist_name=$(DISTNAME) \
        --release --version $(VERSION)

sign:
	@[ -z $(KSPASSWD) ] && (echo "Please input keystore password via KSPASSWD variable" ; \
        echo "After KSPASSWD is set, please input make sign to finish whole task..." ; exit 1) || continue
	jarsigner -verbose -keystore $(KEYSTORE) -signedjar $(DISTNAME)_v$(VERSION).apk $(DISTNAME)__$(ARCH)-release-unsigned-$(VERSION)-.apk $(KSALIAS) -storepass $(KSPASSWD)
	@echo "Auto remove unsigned apk file..."
	rm -f $(DISTNAME)__$(ARCH)-release-unsigned-$(VERSION)-.apk

install:
	@echo "Install Apk to the Android device via adb, Please ensure the connection of the device"
	adb install $(DISTNAME)-v$(VERSION).apk

#--------------------------------------------------------------------------------

clean:
	rm *.apk
