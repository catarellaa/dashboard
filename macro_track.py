import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class macro_track(ttk.LabelFrame):


    def __init__(self, parent, protein, carb, fat, **kwargs,):
        super().__init__(parent, text="macro tracking", padding=15, **kwargs)

        self.protein_percent = DoubleVar(value=0.0)
        self.carb_percent = DoubleVar(value=0.0)
        self.fat_percent = DoubleVar(value=0.0)

        self.protein = float(protein)
        self.fat = float(fat)
        self.carb = float(carb)

        self._build_macro_rows()


    def _build_macro_rows(self):
        self.columnconfigure(0, weight=1) 
        self.columnconfigure(1, weight=2)  
        self.columnconfigure(2, weight=6) 
        self.columnconfigure(3, weight=1)  

        self.macros_config = [
            {"name": "Protein", "var": self.protein_percent, "row": 0, "goal": self.protein},
            {"name": "Carbs", "var": self.carb_percent, "row": 1, "goal": self.carb},
            {"name": "Fats", "var": self.fat_percent, "row": 2, "goal": self.fat}
        ]

        self.entries = {}
        self.status_boxes = {}

        for idx, item in enumerate(self.macros_config):
            m_name = item["name"]
            row_idx = item["row"]
            ctrl_var = item["var"]
            
            lbl = ttk.Label(self, text=f"{m_name} (g):", font=("Courier", 10, "bold"))
            lbl.grid(row=row_idx, column=0, sticky="w", padx=5, pady=8)
            
            entry_box = ttk.Entry(self, width=8)
            entry_box.grid(row=row_idx, column=1, sticky="w", padx=5, pady=8)
            entry_box.insert(0, "0")
            self.entries[m_name] = entry_box
            
            prog_bar = ttk.Progressbar(
                self, orient="horizontal", mode="determinate", maximum=100, variable=ctrl_var
            )
            prog_bar.grid(row=row_idx, column=2, sticky="ew", padx=10, pady=8)
            
            status_box = ttk.Entry(self, width=14, font=("Courier", 9, "bold"))
            status_box.grid(row=row_idx, column=3, sticky="e", padx=5, pady=8)
            status_box.insert(0, f"0.0% of {int(item['goal'])}g")
            status_box.config(state="readonly")
            self.status_boxes[m_name] = status_box
            
            entry_box.bind(
                "<KeyRelease>",
                lambda event, n=m_name, v=ctrl_var, i=idx: self._recalculate_macro_progress(n, v, i)
            )

    def _recalculate_macro_progress(self, name, progress_var, config_idx):
        target_goal = float(self.macros_config[config_idx]["goal"])
        input_widget = self.entries[name]
        status_widget = self.status_boxes[name]
        raw_input = input_widget.get().strip()

        if not raw_input:
            progress_var.set(0.0)
            self._update_readonly_box(status_widget, 0.0, target_goal)
            return

        try:
            current_grams = float(raw_input)
            if current_grams < 0:
                raise ValueError()

            calculated_pct = (current_grams / target_goal) * 100.0 if target_goal > 0 else 0.0
            
            progress_var.set(min(calculated_pct, 100.0))
            
            self._update_readonly_box(status_widget, calculated_pct, target_goal)

        except ValueError:
            progress_var.set(0.0)
            self._update_readonly_box(status_widget, 0.0, target_goal, error=True)

    def update_goals(self, n_protein, n_carb, n_fat):
        self.protein = float(n_protein)
        self.carb = float(n_carb)
        self.fat = float(n_fat)

        self.macros_config[0]["goal"] = self.protein
        self.macros_config[1]["goal"] = self.carb
        self.macros_config[2]["goal"] = self.fat

        for idx, item in enumerate(self.macros_config):
            self._recalculate_macro_progress(item["name"], item["var"], idx)

    def _update_readonly_box(self, widget, percent, goal, error=False):
        widget.config(state="normal")
        widget.delete(0, END)
        if error:
            widget.insert(0, "Invalid Input")
        else:
            widget.insert(0, f"{percent:.1f}% of {int(goal)}g")
        widget.config(state="readonly")