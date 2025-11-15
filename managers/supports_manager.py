from __future__ import annotations
from tkinter import Label
from tkinter import ttk
from tkinter import StringVar, IntVar


class SupportsManager:
    """Manages support-related operations and data"""
    
    def __init__(self, app: App):
        self.app = app
        self.support_number = [0]
        self.supports_widgets = [
            [
                None, 
                Label(app.p3, text="Node"), 
                Label(app.p3, text="Rx"), 
                Label(app.p3, text="Ry"),
                Label(app.p3, text="Mz"),
                Label(app.p3, text="θ")
            ]
        ]
        
    def add_support_row(self):
        self.support_number.append(self.support_number[-1] + 1)
        name = f"S{self.support_number[-1]}"
        
        self.app.Supports.update({
            name: {
                "Node": StringVar(),
                "Rx": StringVar(value="Fixed"),
                "Ry": StringVar(value="Fixed"),
                "Mz": StringVar(value="Fixed"),
                "theta":IntVar()
            }
        })

        var_name = self.app.Supports[name]["Node"]
        var_Rx = self.app.Supports[name]["Rx"]
        var_Ry = self.app.Supports[name]["Ry"]
        var_Mz = self.app.Supports[name]["Mz"]
        theta = self.app.Supports[name]["theta"]

        var_name.trace("w",lambda *_,name=name,theta=theta: self.app.canvas_manager.draw_support(name, theta))
        var_Rx.trace("w",lambda *_,name=name,theta=theta: self.app.canvas_manager.draw_support(name, theta))
        var_Ry.trace("w",lambda *_,name=name,theta=theta: self.app.canvas_manager.draw_support(name, theta))
        var_Mz.trace("w",lambda *_,name=name,theta=theta: self.app.canvas_manager.draw_support(name, theta))
        theta.trace("w",lambda *_,name=name,theta=theta: self.app.canvas_manager.draw_support(name, theta))
        
        self.supports_widgets.append([
            Label(self.app.p3, text=name, width=4),
            ttk.Combobox(self.app.p3, values=list(self.app.Nodes.keys()), 
                        textvariable=var_name, width=6, state="readonly"),
            ttk.Combobox(self.app.p3, values=("Fixed", "Free"), 
                        textvariable=var_Rx, width=6, state="readonly"),
            ttk.Combobox(self.app.p3, values=("Fixed", "Free"), 
                        textvariable=var_Ry, width=6, state="readonly"),
            ttk.Combobox(self.app.p3, values=("Fixed", "Free"), 
                        textvariable=var_Mz, width=6, state="readonly"),
            ttk.Entry(self.app.p3,textvariable=theta,width=9)
        ])