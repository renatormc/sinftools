import os
from pathlib import Path
from subprocess import Popen


def find_chrome():
    possible_locations = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    ]
    for location in possible_locations:
        if os.path.exists(location):
            return location


def find_firefox():
    possible_locations = [
        "C:/Program Files/Mozilla Firefox/firefox.exe"
    ]
    for location in possible_locations:
        if os.path.exists(location):
            return location


def open_in_browser(url, order=['chrome', 'firefox', 'other'], file_path=False):
    if file_path:
        url = Path(os.path.abspath(url)).as_uri()
    for browser in order:
        if browser == 'chrome':
            path = find_chrome()
            if path:
                Popen(f"\"{path}\" {url}")
                return
        if browser == 'firefox':
            path = find_firefox()
            if path:
                Popen(f"\"{path}\" {url}")
                return
        os.system(f"start {url}")
