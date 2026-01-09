

import tkinter as tk
from tkinter import ttk
import time
import json
import os

LOG_FILE = "logs.json"

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch Logger")

        self.running = False
        self.start_time = None
        self.elapsed_time = 0
        self.logged_times = []

        self.load_logs()

        # Time display
        self.time_label = ttk.Label(root, text="00:00:00", font=("Helvetica", 40))
        self.time_label.pack(pady=10)

        # Buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack()

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(self.button_frame, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.log_button = ttk.Button(self.button_frame, text="Log", command=self.log_time)
        self.log_button.grid(row=0, column=2, padx=5)

        # Total time display
        self.total_label = ttk.Label(root, text="", font=("Helvetica", 20))
        self.total_label.pack(pady=5)

        # Log list
        self.log_listbox = tk.Listbox(root, height=8, font=("Courier", 12))
        self.log_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load previous log entries
        for seconds in self.logged_times:
            self.log_listbox.insert(tk.END, self.format_time(seconds))

        self.update_total()
        self.update_clock()

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def log_time(self):
        if self.running:
            self.stop()

        if self.elapsed_time > 0:
            self.logged_times.append(self.elapsed_time)
            self.log_listbox.insert(tk.END, self.format_time(self.elapsed_time))
            self.save_logs()

        self.elapsed_time = 0
        self.start_time = None
        self.update_total()

    def update_total(self):
        total_seconds = sum(self.logged_times)
        self.total_label.config(text=f"Total: {self.format_time(total_seconds)}")

    def update_clock(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        self.time_label.config(text=self.format_time(self.elapsed_time))
        self.root.after(100, self.update_clock)

    def save_logs(self):
        try:
            with open(LOG_FILE, 'w') as f:
                json.dump(self.logged_times, f)
        except Exception as e:
            print("Error saving logs:", e)

    def load_logs(self):
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r') as f:
                    self.logged_times = json.load(f)
            except Exception as e:
                print("Error loading logs:", e)
                self.logged_times = []
        else:
            self.logged_times = []

    @staticmethod
    def format_time(seconds):
        minutes, sec = divmod(int(seconds), 60)
        hrs, min = divmod(minutes, 60)
        return f"{hrs:02d}:{min:02d}:{sec:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()

