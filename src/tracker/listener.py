import os
from pynput import keyboard, mouse
from storage import EventWriter
import time
from datetime import datetime

LOCK_PATH = r"C:\dev\ghost-data\events.lock"
os.makedirs(os.path.dirname(LOCK_PATH), exist_ok=True)
try:
    lock_file = open(LOCK_PATH, "x")
except FileExistsError:
    print("Logger is already running (or crashed earlier). Lock file:", LOCK_PATH)
    raise SystemExit(1)
lock_file.write(str(os.getpid()))
lock_file.close()



def on_press(key):
    writer.log("key_down")

def on_release(key):
    writer.log("key_up")

def on_click(x, y, button, pressed):
    if pressed:
        writer.log("mouse_down", x, y)
    else:
        writer.log("mouse_up", x, y)

MOVE_INTERVAL = 0.02  
last_move_time = 0.0
def on_move(x, y):
    global last_move_time
    current_time = time.time()
    if current_time - last_move_time >= MOVE_INTERVAL:
        last_move_time = current_time
        writer.log("mouse_move",x,y)



writer = None
k_listener = None
m_listener = None

stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
try: 
    try:
        writer = EventWriter(rf"C:\dev\ghost-data\events_{stamp}.csv")
        k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        m_listener = mouse.Listener(on_click=on_click, on_move=on_move)
        writer.start()
        k_listener.start()
        m_listener.start()
        while k_listener.is_alive() and writer.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if k_listener is not None and k_listener.is_alive():
            k_listener.stop()
        if m_listener is not None and m_listener.is_alive():
            m_listener.stop()
        if writer is not None and writer.is_alive():
            writer.stop()
finally:
    os.remove(LOCK_PATH)