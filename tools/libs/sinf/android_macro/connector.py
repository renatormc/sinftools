from sinf.android_macro.android_connector import AndroidConnector
import time
import cv2
import os
from sinf.android_macro.rectangle import Rectangle
import numpy as np
import shutil


class Connector:
    def __init__(self):
        self.android_connector = AndroidConnector()
        self.threshold = 0.99
        self.image_folder = None
        self.image_map = {}

    def set_image_folder(self, folder):
        self.image_folder = folder

    def set_image_map(self, map):
        self.image_map = map

    def load_images(self):
        self.images = {}
        for filename in os.listdir(self.image_folder):
            img = cv2.imread(os.path.join(self.image_folder, filename))
            self.images[filename] = img

    def find_template(self, template, file_=None):
        file_ = file_ or self.android_connector.captureScreen()['filename']
        img = cv2.imread(file_)
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= self.threshold)
        recs = []
        for pt in zip(*loc[::-1]):
            rec = Rectangle()
            rec.setX(pt[0])
            rec.setY(pt[1])
            rec.setW(w)
            rec.setH(h)
            recs.append(rec)
        return recs

    def __get_image(self, value):
        number = value if isinstance(value, int) else self.image_map[value]
        return self.images[f"{number}.png"]

    def find_and_tap(self, value, sleep=None, wait=True, max_wait=20):
        values = value if isinstance(value, list) else [value]
        start_time = time.time()
        if sleep:
            time.sleep(sleep)
        while True:
            file_ = self.android_connector.captureScreen()['filename']
            for v in values:
                recs = self.find_template(self.__get_image(v), file_)
                if recs:
                    self.android_connector.tap(recs[0].center_x, recs[0].center_y)
                    return True
            if not wait:
                break
            if (time.time() - start_time) >= max_wait:
                raise Exception(f"Tela {value} não encontrada.")

    def find_or_pass(self, value, other=[], sleep=None, max_wait=20):
        values = value if isinstance(value, list) else [value]
        if sleep:
            time.sleep(sleep)
        start_time = time.time()
        while True:
            for v in values:
                file_ = self.android_connector.captureScreen()['filename']
                recs = self.find_template(
                    self.__get_image(v), file_=file_)
                if recs:
                    self.android_connector.tap(recs[0].center_x, recs[0].center_y)
                    return True
            others = other if isinstance(other, list) else [other]
            for other in others:
                recs = self.find_template(
                    self.__get_image(other), file_=file_)
                if recs:
                    return
            if (time.time() - start_time) >= max_wait:
                return
    
    def save_screen(self, path):
        file_ = self.android_connector.captureScreen()['filename']
        if file_:
            shutil.copy(file_, path)

    def wait_screens(self, values, sleep=None, max_wait=20):
        if sleep:
            time.sleep(sleep)
        start_time = time.time()
        while True:
            file_ = self.android_connector.captureScreen()['filename']
            for value in values:
                recs = self.find_template(
                    self.__get_image(value), file_=file_)
                if recs:
                    return value
            if (time.time() - start_time) >= max_wait:
                break

    def wait_screen(self, value, sleep=None):
        if sleep:
            time.sleep(sleep)
        while True:
            recs = self.find_template(self.__get_image(value))
            if recs:
                return True

    def assert_screen(self, value, sleep=None, max_wait=20):
        values = value if isinstance(value, list) else [value]
        if sleep:
            time.sleep(sleep)
        start_time = time.time()
        while True:
            file_ = self.android_connector.captureScreen()['filename']
            for value in values:
                recs = self.find_template(self.__get_image(value), file_)
                if recs:
                    return True
            if (time.time() - start_time) >= max_wait:
                raise Exception(f"Tela {value} não encontrada.")

    def check_screen(self, value, sleep=None):
        if sleep:
            time.sleep(sleep)
        recs = self.find_template(self.__get_image(value))
        if recs:
            return True
        return False

    def exec(self, cmd, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(cmd)

    def sleep(self, value):
        time.sleep(value)

    def tap(self, x, y, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(f"adb shell input tap {x} {y}")

    def escape(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec("adb shell input keyevent 111")

    def arrow_down(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec("adb shell input keyevent 20")

    def arrow_up(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(f"adb shell input keyevent 19")

    def enter(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(f"adb shell input keyevent 66")

    def delete(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(f"adb shell input keyevent 67")

    def page_up(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(f"adb shell input keyevent 92")
    
    def back(self, sleep=None):
        if sleep:
            time.sleep(sleep)
        self.android_connector.comExec(f"adb shell input keyevent 4")
