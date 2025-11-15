from __future__ import annotations
from tkinter import *
from tkinter import ttk
import Pmw


class SectionDialog:
    """Dialog for managing sections"""
    
    def __init__(self, app: App):
        self.app = app
        
    def show(self):
        section = Toplevel(self.app)
        section.geometry("400x260")
        section.title("Sections")
        section.grab_set()

        main_frame = Frame(section)
        main_frame.pack(padx=10, expand=1, fill="both")

        group_gen_frame = Pmw.Group(main_frame, tag_text="general")
        group_prop_frame = Pmw.Group(main_frame, tag_text="section properties")
        
        gen_frame = Frame(group_gen_frame.interior())
        prop_frame = Frame(group_prop_frame.interior())
        
        group_gen_frame.pack(expand=YES, fill="both", anchor=CENTER)
        group_prop_frame.pack(expand=YES, fill="both", anchor=CENTER)
        
        gen_frame.pack(padx=30, expand=YES, fill="x")
        prop_frame.pack(padx=30, expand=YES, fill="x")

        button_frame = Frame(main_frame)
        button_frame.pack(pady=10, fill="x")

        OK = ttk.Button(button_frame, text="OK", width=7, 
                       command=lambda: self._on_ok(gen_widgets, properties_widgets))
        OK.pack()

        gen_widgets = (
            (Label(gen_frame, text="Section's name:"), 
             ttk.Combobox(gen_frame, values=list(self.app.Sections.keys()), width=9)),
        )

        properties_widgets = (
            (Label(prop_frame, text="Section's material:"), 
             ttk.Combobox(prop_frame, width=9, values=list(self.app.materials.keys()))),
            (Label(prop_frame, text="Moment of inertia:"), 
             ttk.Entry(prop_frame, width=12)),
            (Label(prop_frame, text="Area of section:"), 
             ttk.Entry(prop_frame, width=12)),
        )

        gen_frame.grid_columnconfigure(0, weight=1)
        gen_frame.grid_columnconfigure(1, weight=1)
        prop_frame.grid_columnconfigure(0, weight=1)
        prop_frame.grid_columnconfigure(1, weight=1)

        for i, j in enumerate(gen_widgets):
            j[0].grid(row=i, column=0, sticky="W")
            j[1].grid(row=i, column=1, sticky="E")

        for i, j in enumerate(properties_widgets):
            j[0].grid(row=i, column=0, sticky="W")
            j[1].grid(row=i, column=1, sticky="E")
            
        gen_widgets[0][1].bind("<<ComboboxSelected>>", 
                              lambda e: self._on_section_selected(e, gen_widgets, properties_widgets))
    
    def _on_section_selected(self, event, gen_widgets, properties_widgets):
        """Populate fields when a section is selected"""
        section_name = gen_widgets[0][1].get()
        section_data = self.app.Sections[section_name]
        
        for i, prop_widget in enumerate(properties_widgets):
            prop_widget[1].delete(0, END)
            prop_widget[1].insert(0, list(section_data.values())[i])
    
    def _on_ok(self, gen_widgets, properties_widgets):
        """Save section data when OK is clicked"""
        section_name = gen_widgets[0][1].get()
        self.app.Sections[section_name] = {
            "material": properties_widgets[0][1].get(),
            "Iz": properties_widgets[1][1].get(),
            "A": properties_widgets[2][1].get()
        }
        gen_widgets[0][1]["values"] = list(self.app.Sections.keys())
        self.app.update_members_list(self.app.member_manager.members_widgets, self.app.Sections, 4)