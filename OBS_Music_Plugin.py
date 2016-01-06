# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import string
import psutil
import ctypes
from ctypes import wintypes
import win32con
import win32api
import win32gui
import win32process

title = ""

def enumWindowsProc(hwnd, lParam):
    global title
    if (lParam is None) or ((lParam is not None) and (win32process.GetWindowThreadProcessId(hwnd)[1] == lParam)):
        text = win32gui.GetWindowText(hwnd)
        if text:
            wStyle = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
            if wStyle & win32con.WS_VISIBLE:
                print("%08X - %s" % (hwnd, text))
                title = text

def enumProcWnds(pid=None):
    win32gui.EnumWindows(enumWindowsProc, pid)

def getProcName(procName):
    for proc in psutil.process_iter():
        if proc.name() == procName:
            pid = str(proc)
            rig = pid.split('=',3)
            pid = rig[1]
            rig = pid.split(',',2)
            pid = rig[0]
            return int(pid)

def main(args):
    while(1):
        pid = getProcName(args[0])
        enumProcWnds(pid)
        #print title
        fi = open("MusicTitle.txt","wb")
        title2 = "Now playing: " + title
        title2 = title2.decode('gbk')
        fi.write(title2.encode('utf-8'))
        fi.close()
        time.sleep(2.0)

if __name__ == "__main__":
    main(sys.argv[1:])