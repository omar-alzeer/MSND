from Pynite import FEModel3D
from tkinter import ttk
from tkinter import *
import Pmw

from managers.node_manager import NodeManager
from managers.member_manager import MemberManager
from managers.supports_manager import SupportsManager
from managers.loads_manager import LoadsManager
from managers.canvas_manager import CanvasManager
from dialogs.material_dialog import MaterialDialog
from dialogs.section_dialog import SectionDialog


class App(Tk):
    """Main application class"""
    
    def __init__(self):
        super().__init__()
        self.geometry("1050x600")
        self.title("MSND")
        
        self._initialize_data()
        self._create_widgets()
        self._setup_managers()
        
    def _initialize_data(self):
        """Initialize application data structures"""
        self.Nodes = {}
        self.Members = {}
        self.Supports = {}
        self.Ploads = {}
        self.Dloads = {}
        self.Materials = {
            "concrete": {
                "E": 3.2836e+7,
                "G": 13681666.667,
                "P": 0.2,
                "W": 25
            },
            "steel": {
                "E": 2.1e+8,
                "G": 80769230.769,
                "P": 0.3,
                "W": 76.98
            }
        }
        self.Sections = {
            "default": {
                "material": "concrete",
                "Iz": 0.00208,
                "A": 0.1
            }
        }
        
        self.free = {
            "Fixed": True,
            "Free": False
        }
        self.releases = {
            "Start": (True, False),
            "End": (False, True),
            "Both": (True, True),
            "Unrelease": (False, False)
        }
        
    def _create_widgets(self):
        """Create the main UI widgets"""
        self._create_menu()
        self._create_canvas()
        self._create_notebook()
        
    def _create_menu(self):
        """Create the application menu"""
        self.menu = Menu(self, tearoff=False)
        self.config(menu=self.menu)
        
        # Run menu
        self.run = Menu(self.menu, tearoff=False)
        for label, command in [("Bending", "BM"), ("Shear", "SF"), ("Normal", "NF"), ("Deflection", "D"), ("Reactions", "R")]:
            self.run.add_command(label=label, command=lambda cmd=command: self.analyze(cmd))
        self.menu.add_cascade(label="Run", menu=self.run)

        # Define menu
        self.define = Menu(self.menu, tearoff=False)
        self.define.add_command(label="materials", command=self.materials_dialog)
        self.define.add_command(label="sections", command=self.sections_dialog)
        self.menu.add_cascade(label="Define", menu=self.define)

        # Help menu
        self.help = Menu(self.menu, tearoff=False)
        self.help.add_command(label="About")
        self.menu.add_cascade(label="Help", menu=self.help)
        
    def _create_canvas(self):
        """Create the drawing canvas"""
        self.board = Canvas(self, height=600, width=600, bg="white", relief=SOLID, borderwidth=1)
        self.board.pack(side=LEFT, padx=(10, 0), pady=10)
        
    def _create_notebook(self):
        """Create the notebook with tabs"""
        self.notebook = Pmw.NoteBook(self)
        self.p1 = self.notebook.add("Nodes")
        self.p2 = self.notebook.add("Members")
        self.p3 = self.notebook.add("Supports")
        self.p4 = self.notebook.add("Point load")
        self.p5 = self.notebook.add("Dist load")
        self.notebook.pack(side=LEFT,fill="both",expand=True,padx=(10,10),pady=10)
        
    def _setup_managers(self):
        """Initialize all the manager classes"""
        self.canvas_manager = CanvasManager(self)
        self.node_manager = NodeManager(self)
        self.member_manager = MemberManager(self)
        self.supports_manager = SupportsManager(self)
        self.loads_manager = LoadsManager(self)
        self.material_dialog = MaterialDialog(self)
        self.section_dialog = SectionDialog(self)
        
        self._setup_ui_buttons()
        self._create_mouse_bind()
        
    def _setup_ui_buttons(self):
        """Setup UI buttons for all tabs"""
        self._create_page_buttons(self.p1, self.add_node, self.delete_node) 
        self._create_page_buttons(self.p2, self.add_member, self.delete_member)
        self._create_page_buttons(self.p3, self.add_support, self.delete_support)
        self._create_page_buttons(self.p4, self.add_pload, self.delete_pload)
        self._create_page_buttons(self.p5, self.add_dload, self.delete_dload)
        
        # Deploy initial widgets
        self.node_manager.add_node_row()
        self.member_manager.add_member_row()
        self.supports_manager.add_support_row()
        self.deploy_widgets(self.node_manager.nodes_widgets)
        self.deploy_widgets(self.member_manager.members_widgets)
        self.deploy_widgets(self.supports_manager.supports_widgets)
        
    def _create_page_buttons(self, parent, add_command, delete_command):
        """Create add/delete buttons for a page"""
        add_button = ttk.Button(parent, text="add", command=add_command, width=7)
        del_button = ttk.Button(parent, text="delete", command=delete_command, width=7)
        add_button.place(relx=0.9, rely=0.9, anchor=CENTER)
        del_button.place(relx=0.75, rely=0.9, anchor=CENTER)

    def _create_mouse_bind(self):
        self.board.bind("<Button-1>",self.canvas_manager.start_pan)
        self.board.bind("<B1-Motion>",self.canvas_manager.move_screen)
        self.board.bind("<Button-4>",lambda *_,zoom_status="in":self.canvas_manager.zoom(*_,zoom_status))
        self.board.bind("<Button-5>",lambda *_,zoom_status="out":self.canvas_manager.zoom(*_,zoom_status))
        
    # UI action methods
    def add_node(self):
        self.node_manager.add_node_row()
        self.deploy_widgets(self.node_manager.nodes_widgets)
    
    def add_member(self):
        self.member_manager.add_member_row()
        self.deploy_widgets(self.member_manager.members_widgets)
    
    def add_support(self):
        self.supports_manager.add_support_row()
        self.deploy_widgets(self.supports_manager.supports_widgets)
    
    def add_pload(self):
        self.loads_manager.add_pload_row()
        self.deploy_widgets(self.loads_manager.pload_widgets)
        
    def add_dload(self):
        self.loads_manager.add_dload_row()
        self.deploy_widgets(self.loads_manager.dload_widgets)
        
    def delete_node(self):
        self._delete_widgets_row(self.node_manager.nodes_widgets, 2, 
                               self.node_manager.node_number, self.Nodes)
    
    def delete_member(self):
        self._delete_widgets_row(self.member_manager.members_widgets, 2,
                               self.member_manager.member_number, self.Members)
    
    def delete_support(self):
        self._delete_widgets_row(self.supports_manager.supports_widgets, 2,
                               self.supports_manager.support_number, self.Supports)
    
    def delete_pload(self):
        self._delete_widgets_row(self.loads_manager.pload_widgets, 1,
                               self.loads_manager.pload_number, self.loads_manager.ploads)
    
    def delete_dload(self):
        self._delete_widgets_row(self.loads_manager.dload_widgets, 1,
                               self.loads_manager.dload_number, self.loads_manager.dloads)
    
    def deploy_widgets(self, widgets_list):
        """Deploy widgets to the grid"""
        for row, widgets in enumerate(widgets_list):
            for column, widget in enumerate(widgets):
                if row == 0 and column == 0:
                    continue
                widget.grid(row=row, column=column)
        
    def _delete_widgets_row(self, widgets_list, list_num, widget_number, input_dict):
        """Delete a row of widgets"""
        if len(widgets_list) > list_num:
            for widget in widgets_list[-1]:
                widget.destroy()
            widget_number.pop()
            widgets_list.pop()
            input_dict.popitem()

            if len(widgets_list) == 1:
                for widget in widgets_list[-1]:
                    if widget is None:
                        continue
                    widget.grid_remove()

    def update_nodes_list(self):
        """Update node lists in member widgets"""
        for i in range(1, len(self.member_manager.members_widgets)):
            for j in range(1, 3):
                self.member_manager.members_widgets[i][j]["values"] = list(self.Nodes.keys())
    
    def update_members_list(self, widgets_list, var_dict, widget_num):
        """Update member lists in various widgets"""
        for i in range(1, len(widgets_list)):
            widgets_list[i][widget_num]["values"] = list(var_dict.keys())

    def materials_dialog(self):
        """Show materials dialog"""
        self.material_dialog.show()
    
    def sections_dialog(self):
        """Show sections dialog"""
        self.section_dialog.show()
    
    def analyze(self, internal_force):
        """Perform structural analysis"""
        model = FEModel3D()
        
        # Add materials
        for name, props in self.Materials.items():
            model.add_material(name, float(props["E"]), float(props["G"]), 
                             float(props["P"]), float(props["W"]))
        
        # Add nodes
        for name, node in self.Nodes.items():
            model.add_node(name, node["X"].get(), node["Y"].get(), 0)
            
        # Add members
        for name, member in self.Members.items():
            section = self.Sections[member["section"].get()]
            model.add_member(
                name,
                member["start_node"].get(),
                member["end_node"].get(),
                section["material"], 1,
                member["modifier"].get() * float(section["Iz"]), 1,
                float(section["A"])
            )
                
            release = self.releases[member["release"].get()]
            model.def_releases(name, Rzi=release[0], Rzj=release[1])
        
        # Add supports
        for support in self.Supports.values():
            model.def_support(
                support["Node"].get(),
                self.free[support["Rx"].get()],
                self.free[support["Ry"].get()], 1, 1, 1,
                self.free[support["Mz"].get()]
            )
        
        # Add point loads
        for pload in self.Ploads.values():
            model.add_member_pt_load(
                pload["Member"].get(),
                pload["Direction"].get(),
                pload["P"].get(), pload["X"].get()
            )
                
        # Add distributed loads
        for dload in self.Dloads.values():              
            model.add_member_dist_load(         
                dload["Member"].get(),             
                dload["Direction"].get(),
                dload["W1"].get(), dload["W2"].get(),
                dload["X1"].get(), dload["X2"].get()
            )
        
        model.analyze()
        
        # Plot results based on requested internal force
        plot_actions = {
            "BM": lambda m: m.plot_moment("Mz", n_points=1000),
            "SF": lambda m: m.plot_shear("Fy", n_points=1000),
            "NF": lambda m: m.plot_axial(n_points=1000),
            "D": lambda m: m.plot_deflection("dy", n_points=1000),
            "R": lambda: self._show_reactions(model)
        }
        
        action = plot_actions.get(internal_force)
        if action:
            if internal_force == "R":
                action()
            else:
                for member_name in self.Members.keys():
                    action(model.Members[member_name])
    
    def _show_reactions(self, model):
        """Show reaction forces in a new window"""
        reaction = Toplevel(self)
        reaction.title("Reactions")
        reaction.grab_set()
        
        widgets = [
            [None, Label(reaction, text="Rx"), Label(reaction, text="Ry"), 
             Label(reaction, text="Mz")]
        ]
        
        for node_name in self.Nodes.keys():
            node = model.Nodes[node_name]
            widgets.append([
                Label(reaction, text=node_name, width=4),
                Label(reaction, text=round(node.RxnFX["Combo 1"], 3), bg="white",
                     borderwidth=1, relief="solid", width=9),
                Label(reaction, text=round(node.RxnFY["Combo 1"], 3), bg="white",
                     borderwidth=1, relief="solid", width=9),
                Label(reaction, text=round(node.RxnMZ["Combo 1"], 3), bg="white",
                     borderwidth=1, relief="solid", width=9)
            ])
        self.deploy_widgets(widgets)