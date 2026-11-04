import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class month_calendar(ttk.Frame):
    def __init__(self, parent, on_date_selected=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.on_date_selected = on_date_selected

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.cal_system = calendar.TextCalendar(calendar.SUNDAY)

        self.create_widget()
        self.draw_month(self.current_year, self.current_month)


    def create_widget(self):
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady = 5, fill="x")

        ttk.Button(nav_frame, text="<", width=3, command=self.prev_month).pack(side="left", padx=5)
        self.month_year_label = ttk.Label(nav_frame)
        self.month_year_label.pack(side="left", expand=True)
        ttk.Button(nav_frame, text=">", width=3, command=self.next_month).pack(side="right", padx=5)

        header_frame = ttk.Frame(self)
        header_frame.pack(fill="x", padx=5)
        days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

        for col_idx, day_name in enumerate(days):
            label = ttk.Label(header_frame, text=day_name, width=4, anchor="center")
            label.grid(row=0, column=col_idx, sticky="nsew", pady=2)
            header_frame.columnconfigure(col_idx, weight=1)

        self.matrix_frame = ttk.Frame(self)
        self.matrix_frame.pack(expand=True, fill="both", padx = 5, pady = 2)

        self.day_buttons = []
        for r in range(5):
            self.matrix_frame.rowconfigure(r, weight = 1)
            row_buttons = []
            for c in range (7):
                self.matrix_frame.columnconfigure(c, weight = 1)
                button = tk.Button(
                    self.matrix_frame, text="", bg="#cf9a9a",
                    command = lambda row=r, col=c: self.day_click(row, col)
                )
                button.grid(row=r, column=c, sticky="nsew", padx = 1, pady = 1)
                row_buttons.append(button)
            self.day_buttons.append(row_buttons)

            
    def draw_month(self, year, month):
        self.month_year_label.config(text=f"{calendar.month_name[month][:3]} {year}")
        month_weeks = self.cal_system.monthdayscalendar(year, month)

        for row_idx in range (5):
            for col_idx in range(7):
                button = self.day_buttons[row_idx][col_idx]
                if row_idx < len(month_weeks):
                    day_num = month_weeks[row_idx][col_idx]
                else:
                    day_num = 0

                if day_num != 0:
                    button.config(text=str(day_num), state="normal", bg="#ffffff", fg="#333333")
                else:
                    button.config(text="", state="disabled", bg="#ffffff")


    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_month(self.current_year, self.current_month)

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_month(self.current_year, self.current_month)

    def day_click(self, row, col):
        day_text = self.day_buttons[row][col].cget("text")
        if day_text and self.on_date_selected:
            iso_date = f"{self.current_year}-{self.current_month:02d}-{int(day_text):02d}"
            self.on_date_selected(iso_date)




