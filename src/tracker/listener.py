from pynput import keyboard, mouse
import time



def on_press(key):
    print(time.time(), "Key down")

def on_release(key):
    print(time.time(), "Key up")

def on_click(x, y, button, pressed):
    if pressed:
        print(time.time(), "Mouse button down")
    else:
        print(time.time(), "Mouse button up")

k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
m_listener = mouse.Listener(on_click=on_click)

k_listener.start()
m_listener.start()

try:
    k_listener.join()
except KeyboardInterrupt:
    print("Stopping...")
    k_listener.stop()
    m_listener.stop()