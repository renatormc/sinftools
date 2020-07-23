import re
import sys
import os
import string

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient

device, serialno = ViewClient.connectToDeviceOrExit()

ViewClient.sleep(2)

vc = ViewClient(device, serialno)
textViews = vc.findViewsWithAttribute("class", "android.widget.TextView")

def dropDownMenu(device,numberOfTimes):
    for i in range(0,numberOfTimes):
        device.press('KEYCODE_DPAD_DOWN')

dropDownMenu(device, 1)