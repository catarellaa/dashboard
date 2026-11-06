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

    def fetch_events(self):
        self.glance_display.config(state="normal")
        self.glance_display.delete("1.0", tk.END)



    def _async_fetch_worker(self, date, thread_id):
        try:
            start_date = datetime.datetime.combine(date, datetime.time.min)
            end_date = datetime.datetime.combine(date, datetime.time.max)

            time_min = start_date.isoformat() + "Z"
            time_max = end_date.isoformat() + "Z"

            events_result = self.service.events().list(
                calendarId='primary',
                time_Min=time_min,
                time_Max=time_max,
                single_events = True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

        except Exception as e:
            self.after(0, self._safe_display_update, f"error fetching evens:\n{str(e)}", thread_id, is_error=True)


    def unchanged_render(self, data, thread_id, is_error = False):
        if thread_id != self.current_thread_id:
            return

        if is_error:
            self._write_to_display(data)
            return

        if not data:
            self._write_to_display("none")
            return

        output_lines = []
        for event in data:
            start_raw = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', '(No Title)')

            if 'T' in start_raw:
                clean = start_raw.split('+')[0].split('Z')[0]
                time_object = datetime.datetime.fromisoformat(clean)
                time_string = time_object.strftime("%I:%M %p")
            else:
                time_string = " "

            output_lines.append(f"• [{time_string}] {summary}")

        self._write_to_display("\n".join(output_lines))

    def _write_to_display(self, text):
        self.glance_display.config(state="normal")
        self.glance_display.delete("1.0", tk.END)
        self.glance_display.insert("1.0", text)
        self.glance_display.config(state="disabled")
        


