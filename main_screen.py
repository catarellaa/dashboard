from tkinter import *
from tkinter import ttk

from month_calendar import month_calendar

def refresh_dashboard_data(iso_date_string):
    root.stage_title.config(text=f"Records for: {iso_date_string}")
    data = f". Sync complete for: {iso_date_string}\n"
    root.data_display.config(text=data)

root = Tk()
root.title("Dashboard")
root.geometry("900x900")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

sidebar = ttk.Frame(root, relief="solid", padding=10)
sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
lbl_menu = ttk.Label(sidebar, text="Dashboard", font=("Arial", 24, "bold"))
lbl_menu.pack(anchor="w", pady=10)

mainframe = ttk.Frame(sidebar, padding=(3, 3, 12, 12))
mainframe.pack(side="bottom", fill="x")
#ttk.Label(mainframe, text="Dashboard").pack()
ttk.Button(mainframe, text="Exit", command=root.destroy).pack(pady=5)

root.calendar_widget = month_calendar(sidebar, on_date_selected=refresh_dashboard_data)
root.calendar_widget.pack(fill="x", pady=20)

root.main_stage = ttk.Frame(root, relief="solid", padding=20)
root.main_stage.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
root.stage_title = ttk.Label(root.main_stage, text="Select a date...")
root.stage_title.pack(anchor="w", pady=10)
        
root.data_display = ttk.Label(root.main_stage, text="No date loaded.", justify="left")
root.data_display.pack(anchor="w", pady=10)

root.mainloop()