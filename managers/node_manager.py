from __future__ import annotations
from tkinter import Label
from tkinter import ttk
from tkinter import DoubleVar, StringVar


class NodeManager:
    """Manages node-related operations and data"""
    
    def __init__(self, app: App):
        self.app = app
        self.node_number = [0]
        self.nodes_widgets = [
            [None, Label(app.p1, text="X (m)"), Label(app.p1, text="Y (m)")]
        ]
        
    def add_node_row(self):
        self.node_number.append(self.node_number[-1] + 1)
        name = f"N{self.node_number[-1]}"
        
        self.app.Nodes.update({
            name: {
                "X": DoubleVar(),
                "Y": DoubleVar()
            }
        })
        
        varx = self.app.Nodes[name]["X"]
        vary = self.app.Nodes[name]["Y"]
        
        varx.trace("w", lambda *_, name=name, varx=varx, vary=vary: self.app.canvas_manager.draw_node(name, varx, vary))
        vary.trace("w", lambda *_, name=name, varx=varx, vary=vary: self.app.canvas_manager.draw_node(name, varx, vary))
        
        self.nodes_widgets.append([
            Label(self.app.p1, text=name, width=4),
            ttk.Entry(self.app.p1, textvariable=varx, width=9),
            ttk.Entry(self.app.p1, textvariable=vary, width=9)
        ])
        
        self.app.update_nodes_list()
        self.app.update_members_list(self.app.supports_manager.supports_widgets, self.app.Nodes, 1)