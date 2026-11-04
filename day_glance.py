import datetime
import tkinter as tk
from tkinter import ttk
import threading

class day_glance(ttk.Frame):
    def __init__(self, parent, google_service=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.service = google_service
        self.selected_date = datetime.date.day()

        self._init_layout()

    def _init_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx = 10, pady = 5)

        self.previous_day_button = ttk.Button(self.header_frame, text="<", width=3)
        self.previous_day_button.pack(side=tk.LEFT)

        self.next_day_button = ttk.Button(self.header_frame, text=">", width=3)
        self.next_day_button.pack(side=tk.RIGHT)
