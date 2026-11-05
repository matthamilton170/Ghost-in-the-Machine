from pynput import keyboard, mouse
from storage import EventWriter

writer = EventWriter("C:\\dev\\ghost-data\\events.csv")


def on_press(key):
    writer.log("key_down")

def on_release(key):
    writer.log("key_up")

def on_click(x, y, button, pressed):
    if pressed:
        writer.log("mouse_down")
    else:
        writer.log("mouse_up")

k_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
m_listener = mouse.Listener(on_click=on_click)


writer.start()
k_listener.start()
m_listener.start()

try:
    k_listener.join()
except KeyboardInterrupt:
    print("Stopping...")
    k_listener.stop()
    m_listener.stop()
    writer.stop()
