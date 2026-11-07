import queue
import threading
import time
import os
import csv

HEARTBEAT_INTERVAL = 60 

class EventWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.event_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def start(self):
        self.thread.start()

    def log(self, event_type, x=None, y=None):
        self.event_queue.put((time.time(), event_type, x, y))

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def is_alive(self):
        return self.thread.is_alive()

    def _run(self):
        needs_header = (
            not os.path.exists(self.file_path)
            or os.path.getsize(self.file_path) == 0
        )
        with open(self.file_path, 'a', newline="") as f:
            csv_writer = csv.writer(f)
            if needs_header:
                csv_writer.writerow(["timestamp", "event_type", "x", "y"])
            last_flush = time.time()
            last_heartbeat = time.time()
            while not (self.stop_event.is_set() and self.event_queue.empty()):
                now = time.time()
                if now - last_flush >= 1:
                    f.flush()
                    last_flush = now
                if now - last_heartbeat >= HEARTBEAT_INTERVAL:
                    csv_writer.writerow([now, "heartbeat", None, None])
                    last_heartbeat = now
                try:
                    timestamp, event_type, x, y = self.event_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                csv_writer.writerow([timestamp, event_type, x, y])    