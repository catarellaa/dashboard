import datetime
import tkinter as tk
from tkinter import ttk
import threading

class day_glance(ttk.Frame):
    def __init__(self, parent, google_service=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.service = google_service
        self.selected_date = datetime.date.today()

        self._init_layout()

    def _init_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx = 10, pady = 5)

        self.previous_day_button = ttk.Button(self.header_frame, text="<", width=3)
        self.previous_day_button.pack(side=tk.LEFT)

        self.date_label = ttk.Label(self.header_frame, text="")
        self.date_label.pack(side=tk.LEFT, expand=True)

        self.next_day_button = ttk.Button(self.header_frame, text=">", width=3)
        self.next_day_button.pack(side=tk.RIGHT)

        self.content_frame = ttk.LabelFrame(self, text="day at a glance")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx = 10, pady = 5)

        self.glance_display = tk.Text(self.content_frame, wrap="word", height=15)
        self.glance_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.glance_display.insert("1.0", "select date")

    def update_date_display(self):
        refresh = self.selected_date.strftime("%A, %B, %d, %Y")
        self.date_label.config(text=refresh)

    def prev_month(self):
        self.selected_date -= datetime.timedelta(days=1)
        self.update_date_display()

    def next_month(self):
        self.selected_date += datetime.timedelta(days=1)
        self.update_date_display()


