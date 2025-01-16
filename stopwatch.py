import tkinter as tk
from tkinter import messagebox
import time
import threading
import json

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0

        self.load_state()

        self.label = tk.Label(root, text=self.format_time(), font=("Helvetica", 48))
        self.label.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(side="left")

        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side="left")

        self.update_display()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def format_time(self):
        hours, rem = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def update_display(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        self.label.config(text=self.format_time())
        self.root.after(100, self.update_display)

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def stop(self):
        if self.running:
            self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.label.config(text=self.format_time())

    def load_state(self):
        try:
            with open("stopwatch_state.json", "r") as f:
                data = json.load(f)
                self.elapsed_time = data.get("elapsed_time", 0)
                self.running = data.get("running", False)
                if self.running:
                    self.start_time = time.time() - self.elapsed_time
        except FileNotFoundError:
            pass

    def save_state(self):
        data = {
            "elapsed_time": self.elapsed_time,
            "running": self.running
        }
        with open("stopwatch_state.json", "w") as f:
            json.dump(data, f)

    def on_close(self):
        self.save_state()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
