from tkinter import *
from tkinter import ttk

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
        p = float(entry_protein.get())
        c = float(entry_carb.get())
        f = float(entry_fat.get())
        root.macro_panel.update_goals(p, c, f)
        
    except ValueError:
         pass

root = Tk()
root.title("Dashboard")
root.geometry("1100x700")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

calendar_tab = ttk.Frame(notebook)
notebook.add(calendar_tab, text="  calendar  ")

############################################################

calendar_tab.grid_rowconfigure(0, weight=1)
calendar_tab.grid_columnconfigure(0, weight=1)
calendar_tab.grid_columnconfigure(1, weight=2)
calendar_tab.grid_columnconfigure(2, weight=2)

sidebar = ttk.Frame(calendar_tab, relief="solid", padding=10)
sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
lbl_menu = ttk.Label(sidebar, text="dashboard", font=("Courier", 24, "bold"))
lbl_menu.pack(anchor="w", pady=10)

root.calendar_widget = month_calendar(sidebar, on_date_selected=refresh_dashboard_data)
root.calendar_widget.pack(fill="x", pady=20)

mainframe = ttk.Frame(sidebar, padding=(3, 3, 12, 12))
mainframe.pack(side="bottom", fill="x")
ttk.Button(mainframe, text="exit app", command=root.destroy).pack(pady=5)

############################################################

root.main_stage = ttk.Frame(calendar_tab, relief="solid", padding=20)
root.main_stage.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
root.stage_title = ttk.Label(root.main_stage, text="select a date...")
root.stage_title.pack(anchor="w", pady=10)
        
root.data_display = Text(root.main_stage, wrap="word", width=40, height=25, font=("Courier", 11), bg="#f9f9f9", relief="flat")
root.data_display.pack(anchor="w", pady=10, fill="both", expand=True)
root.data_display.insert("end", "no date loaded.")

#############################################################

right_panel = ttk.Frame(calendar_tab, padding=10)
right_panel.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

goals_frame = ttk.LabelFrame(right_panel, text="update macro goals", padding=15)
goals_frame.pack(fill="x", padx=20, pady=15)

ttk.Label(goals_frame, text="protein (g):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_protein = ttk.Entry(goals_frame, width=12)
#entry_protein.insert(0, "120")
entry_protein.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(goals_frame, text="carbs (g):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_carb = ttk.Entry(goals_frame, width=12)
#entry_carb.insert(0, "200")
entry_carb.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(goals_frame, text="fats (g):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_fat = ttk.Entry(goals_frame, width=12)
#entry_fat.insert(0, "65")
entry_fat.grid(row=2, column=1, padx=5, pady=5)

btn_submit_goals = ttk.Button(goals_frame, text="submit changes", command=change_macro_goals)
btn_submit_goals.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 5))

root.macro_panel = macro_track(right_panel, protein=120, carb=200, fat=65)
root.macro_panel.pack(fill="both", expand=True, padx=5, pady=10)

root.mainloop()