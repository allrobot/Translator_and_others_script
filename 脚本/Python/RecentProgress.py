from datetime import datetime

import ctypes
import psutil
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

MAX_PATH = 260

def get_window_text(hwnd):
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buff = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buff, length)
    return buff.value

def get_active_window():
    return user32.GetForegroundWindow()

def get_process_id_of_window(hwnd):
    pid = ctypes.c_ulong()
    threadid = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value

last_hwnd = None

while True:
    hwnd = get_active_window()
    if hwnd != last_hwnd:
        last_hwnd = hwnd
        pid = get_process_id_of_window(hwnd)
        try:
            # 使用psutil获取进程的exe路径
            if pid !=0:
                p = psutil.Process(pid)
                print(f'{str(datetime.now())[:-7]} 当前窗口句柄的执行路径: '+p.exe())
        except psutil.NoSuchProcess:
            pass
    time.sleep(0.01)
