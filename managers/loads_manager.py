from __future__ import annotations
from tkinter import Label
from tkinter import ttk
from tkinter import StringVar, DoubleVar


class LoadsManager:
    """Manages load-related operations and data"""
    
    def __init__(self, app: App):
        self.app = app
        self.ploads = {}
        self.dloads = {}
        self.pload_number = [0]
        self.dload_number = [0]
        
        self.pload_widgets = [
            [None, Label(app.p4, text="Member"), Label(app.p4, text="Direction"), 
             Label(app.p4, text="P (kN)"), Label(app.p4, text="X (m)")]
        ]
        
        self.dload_widgets = [
            [None, Label(app.p5, text="Member"), Label(app.p5, text="Direction"), 
             Label(app.p5, text="W1 (kN)"), Label(app.p5, text="W2 (kN)"), 
             Label(app.p5, text="X1 (m)"), Label(app.p5, text="X2 (m)")]
        ]
        
    def add_pload_row(self):
        self.pload_number.append(self.pload_number[-1] + 1)
        name = f"PL{self.pload_number[-1]}"
        
        self.ploads.update({
            name: {
                "Member": StringVar(),
                "Direction": StringVar(value="Fy"),
                "P": DoubleVar(),
                "X": DoubleVar()
            }
        })
        
        self.pload_widgets.append([
            Label(self.app.p4, text=name, width=4),
            ttk.Combobox(self.app.p4, values=list(self.app.Members.keys()), 
                        textvariable=self.ploads[name]["Member"], width=6, state="readonly"),
            ttk.Combobox(self.app.p4, values=("Fy", "Fx", "Mz"), 
                        textvariable=self.ploads[name]["Direction"], width=6, state="readonly"),
            ttk.Entry(self.app.p4, textvariable=self.ploads[name]["P"], width=9),
            ttk.Entry(self.app.p4, textvariable=self.ploads[name]["X"], width=9)
        ])
        
    def add_dload_row(self):
        self.dload_number.append(self.dload_number[-1] + 1)
        name = f"DL{self.dload_number[-1]}"
        
        self.dloads.update({
            name: {
                "Member": StringVar(),
                "Direction": StringVar(value="Fy"),
                "W1": DoubleVar(),
                "W2": DoubleVar(),
                "X1": DoubleVar(),
                "X2": DoubleVar()
            }
        })
        
        self.dload_widgets.append([
            Label(self.app.p5, text=name, width=4),
            ttk.Combobox(self.app.p5, values=list(self.app.Members), 
                        textvariable=self.dloads[name]["Member"], width=6, state="readonly"),
            ttk.Combobox(self.app.p5, values=("Fx", "Fy"), 
                        textvariable=self.dloads[name]["Direction"], width=6, state="readonly"),
            ttk.Entry(self.app.p5, textvariable=self.dloads[name]["W1"], width=9),
            ttk.Entry(self.app.p5, textvariable=self.dloads[name]["W2"], width=9),
            ttk.Entry(self.app.p5, textvariable=self.dloads[name]["X1"], width=9),
            ttk.Entry(self.app.p5, textvariable=self.dloads[name]["X2"], width=9)
        ])