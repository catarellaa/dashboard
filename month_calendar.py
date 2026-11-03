import calendar
from datetime import datetime
import tkinter as tk
from tkinter import ttk

class month_calendar(tk.Tk):
    def init(self):
        super().init()
        self.title("month calendar")
        self.geometry("450x350")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.cal_system = calendar.TextCalendar(calendar.SUNDAY)

        self.create_widget()


    def create_widget(self):
        self.matrix_frame = ttk.Frame(self)
        self.matrix_frame.place(x = 10, y = 10)

        header_frame = ttk.Frame(self)
        days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]





    #def month_config(self, year, month):


