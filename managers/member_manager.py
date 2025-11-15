from __future__ import annotations
from tkinter import Label
from tkinter import ttk
from tkinter import StringVar, IntVar


class MemberManager:
    """Manages member-related operations and data"""
    
    def __init__(self, app: App):
        self.app = app
        self.member_number = [0]
        self.members_widgets = [
            [None, Label(app.p2, text="Start"), Label(app.p2, text="End"), 
             Label(app.p2, text="Release"), Label(app.p2, text="Section"), 
             Label(app.p2, text="I-mod")]
        ]
        
    def add_member_row(self):
        self.member_number.append(self.member_number[-1] + 1)
        name = f"M{self.member_number[-1]}"
        
        self.app.Members.update({
            name: {
                "start_node": StringVar(),
                "end_node": StringVar(),
                "release": StringVar(value="Unrelease"),
                "section": StringVar(value="default"),
                "modifier": IntVar(value=1)
            }
        })
        
        start = self.app.Members[name]["start_node"]
        end = self.app.Members[name]["end_node"]
        
        start.trace("w", lambda *_, name=name, start=start, end=end: self.app.canvas_manager.draw_member(name, start, end))
        end.trace("w", lambda *_, name=name, start=start, end=end: self.app.canvas_manager.draw_member(name, start, end))
        
        self.members_widgets.append([
            Label(self.app.p2, text=name, width=4),
            ttk.Combobox(self.app.p2, values=list(self.app.Nodes.keys()), 
                        textvariable=start, width=6, state="readonly"),
            ttk.Combobox(self.app.p2, values=list(self.app.Nodes.keys()), 
                        textvariable=end, width=6, state="readonly"),
            ttk.Combobox(self.app.p2, values=("Start", "End", "Both", "Unrelease"), 
                        textvariable=self.app.Members[name]["release"], width=9, state="readonly"),
            ttk.Combobox(self.app.p2, values=list(self.app.Sections.keys()), 
                        textvariable=self.app.Members[name]["section"], width=6, state="readonly"),
            ttk.Entry(self.app.p2, textvariable=self.app.Members[name]["modifier"], width=9)
        ])
        
        self.app.update_members_list(self.app.loads_manager.pload_widgets, self.app.Members, 1)
        self.app.update_members_list(self.app.loads_manager.dload_widgets, self.app.Members, 1)