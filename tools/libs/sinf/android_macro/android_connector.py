import subprocess
import os
import cv2
import numpy as np
import time
script_dir = os.path.dirname(os.path.realpath(__file__))

class AndroidConnector:
    def __init__(self):
        self.names = ("screen1.png", "screen2.png")
        self.temp_mobile = "/data/local/tmp"
        self.temp_folder = os.path.join(script_dir, "temp")
        if not os.path.exists(self.temp_folder):
            os.mkdir(self.temp_folder)
        self.flag = True
        self.count = 0
        for name in self.names:
            file_ = os.path.join(self.temp_folder, name)
            if os.path.exists(file_):
                os.remove(file_)
    
    def isRepeated(self):
        if self.count > 1:
            img_current = cv2.imread(os.path.join(self.temp_folder, self.lastName()), 0)
            img_previous = cv2.imread(os.path.join(self.temp_folder, self.previousName()), 0)
            err = mse(img_current, img_previous)
            if err < 5:
                return True
        return False

    def nextName(self):
        self.flag = not self.flag
        return self.names[int(self.flag)]

    def lastName(self):
        return self.names[int(self.flag)]

    def previousName(self):
        return self.names[int(not self.flag)]

    def comExec(self, cmd):
        result = subprocess.check_output(cmd, shell=True)
        return result.decode("utf8")

    def testConnenction(self):
        return self.comExec("devices")

    def captureScreen(self, check_repeated=False):
        self.comExec(f"adb shell screencap {self.temp_mobile}/screen.png")
        name = self.nextName()
        file_ = os.path.join(self.temp_folder, name)
        file_mobile = f"{self.temp_mobile}/screen.png"
        result = self.comExec(f"adb pull {file_mobile} {file_}")
        self.count += 1
        if check_repeated:
            repeated = self.isRepeated()
        else:
            repeated = None
        return {
            "filename": file_,
            "repeated": repeated
        }

    def setScreenSize(self, w, h):
        self.screen_size_w  = w
        self.screen_size_h = h

    def tap(self, x, y):
        self.comExec(f"adb shell input tap {x} {y}")

    def escape(self):
        self.comExec(f"sdb shell input keyevent 111")

    def arrowDown(self):
        self.comExec(f"adb shell input keyevent 20")

    def arrowUp(self):
        self.comExec(f"adb shell input keyevent 19")

    def enter(self):
        self.comExec(f"adb shell input keyevent 66")
    
    def delete(self):
        self.comExec(f"adb shell input keyevent 67")

    def pageUp(self):
        self.comExec(f"adb shell input keyevent 92")

    def enterFirstChat(self):
        self.comExec(f"adb shell input keyevent 20")
        self.comExec(f"adb shell input keyevent 60")


    def roll(self, y0, yf, xm, time=2000):
        cmd = f"adb shell input swipe  {xm} {y0} {xm} {yf} {time}"
        self.comExec(cmd)

    def tapOutPopup(self, y):
        xm = int(self.screen_size_w / 2)
        self.tap(xm, y)


