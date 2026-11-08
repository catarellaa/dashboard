from tkinter import *
from tkinter import ttk, simpledialog

from month_calendar import month_calendar
from macro_track import macro_track

def refresh_dashboard_data(iso_date_string):
    root.stage_title.config(text=f"Records for: {iso_date_string}")

    events = root.calendar_widget.generate_daily_tasks(iso_date_string)

    root.data_display.delete("1.0", "end")

    if not events:
        root.data_display.insert("end", "no events found for this day.\n")
    else:
        root.data_display.insert("end", "")

        for event in events:
            start_info = event["start"].get("dateTime", event["start"].get("date"))
            
            if "T" in start_info:
                time_part = start_info.split("T")[1][:5]
                display_time = f"[{time_part}]"
            else:
                display_time = "[all day]"
                
            summary = event.get("summary", "(no title)")
            root.data_display.insert("end", f"{display_time} {summary}\n")

def change_macro_goals():
    try:
        p = simpledialog.askfloat("protein goal", "enter new protein goal in grams: ", initialvalue=root.macro_panel.protein)
        if p is None: return
        c = simpledialog.askfloat("carb goal", "enter new carb goal in grams: ", initialvalue=root.macro_panel.carb)
        if c is None: return
        f = simpledialog.askfloat("fat goal", "enter new fat goal in grams: ", initialvalue=root.macro_panel.fat)
        if f is None: return

        root.macro_panel.update_goals(p, c, f)
        
    except ValueError:
         pass

root = Tk()
root.title("Dashboard")
root.geometry("900x900")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

sidebar = ttk.Frame(root, relief="solid", padding=10)
sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
lbl_menu = ttk.Label(sidebar, text="Dashboard", font=("Courier", 24, "bold"))
lbl_menu.pack(anchor="w", pady=10)

mainframe = ttk.Frame(sidebar, padding=(3, 3, 12, 12))
mainframe.pack(side="bottom", fill="x")
#ttk.Label(mainframe, text="Dashboard").pack()
#ttk.Button(mainframe, text="change goals", command=change_macro_goals().pack(pady=5))
btn_goals = ttk.Button(mainframe, text="change goals", command=change_macro_goals)
btn_goals.pack(pady=5)
ttk.Button(mainframe, text="Exit", command=root.destroy).pack(pady=5)

root.calendar_widget = month_calendar(sidebar, on_date_selected=refresh_dashboard_data)
root.calendar_widget.pack(fill="x", pady=20)

root.main_stage = ttk.Frame(root, relief="solid", padding=20)
root.main_stage.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
root.stage_title = ttk.Label(root.main_stage, text="Select a date...")
root.stage_title.pack(anchor="w", pady=10)

root.macro_panel = macro_track(root.main_stage, protein=120, carb=200, fat=65)
root.macro_panel.pack(fill="x", side="bottom", pady=10)
        
root.data_display = Text(root.main_stage, wrap="word", width=50, height=30, font=("Courier", 11), bg="#f9f9f9", relief="flat")
root.data_display.pack(anchor="w", pady=10, fill="both", expand=True)
root.data_display.insert("end", "no date loaded.")

root.mainloop()