from tkinter import *
from tkinter import ttk
import Pmw
from PyNite import FEModel3D

class App(Tk):
	def __init__(self):
		Tk.__init__(self)

		self.geometry("430x285")

		self.inputs = {
			"Nodes" : {},
			"Members" : {},
			"Supports" : {},
			"Loads" : {
				"Pload":{},
				"Dload":{}
			},
			"materials":{
				"concrete":{},
				"steel":{}
			},
			"sections":{}
		}
		Nodes = self.inputs["Nodes"]
		Members = self.inputs["Members"]
		Supports = self.inputs["Supports"]
		Ploads = self.inputs["Loads"]["Pload"]
		Dloads = self.inputs["Loads"]["Dload"]
		
		self.free = {
			"Fixed":True,
			"Free":False
		}

		self.releases = {
			"Start":(True,False),
			"End":(False,True),
			"Both":(True,True),
			"Unreleased":(False,False)
		}

		self.Nodes = self.inputs["Nodes"]
		self.Members = self.inputs["Members"]
		self.Supports = self.inputs["Supports"]
		self.Ploads = self.inputs["Loads"]["Pload"]
		self.Dloads = self.inputs["Loads"]["Dload"]
		
		#Menu widget
		self.menu = Menu(self,tearoff=False)
		self.config(menu=self.menu)
		
		self.run = Menu(self.menu,tearoff=False)
		self.run.add_command(label="analyze",command=self.analyze)
		self.menu.add_cascade(label="Run", menu=self.run)

		self.define = Menu(self.menu,tearoff=False)
		self.define.add_command(label="materials",command=self.materials)
		self.define.add_command(label="sections",command=self.sections)
		self.menu.add_cascade(label="Define", menu=self.define)

		self.help = Menu(self.menu,tearoff=False)
		self.help.add_command(label="About")
		self.menu.add_cascade(label="Help", menu=self.help)


		# NoteBook widget
		self.notebook = Pmw.NoteBook(self)
		self.p1 = self.notebook.add("Nodes")
		self.p2 = self.notebook.add("Members")
		self.p3 = self.notebook.add("Supports")
		self.p4 = self.notebook.add("Point load")
		self.p5 = self.notebook.add("Dist load")
		self.notebook.pack(fill="both",expand=True,padx=10,pady=10)
		
		# Nodes page attributes
		self.node_number = 1
		self.Nodes_widgets = [
			[
				None,
				Label(self.p1,text="X (m)"),
				Label(self.p1,text="Y (m)")
			]
		]
		
		# Members page attributes
		self.member_number = 1
		self.Members_widgets = [
			[
				None,
				Label(self.p2,text="Start"),
				Label(self.p2,text="End"),
				Label(self.p2,text="Release")
			]
		]
		
		# Supports page attributes
		self.support_number = 1
		self.Supports_widgets = [
			[
				None,
				Label(self.p3,text="Node"),
				Label(self.p3,text="Rx"),
				Label(self.p3,text="Ry"),
				Label(self.p3,text="Mz")
			]
		]
		
		# point_load page attributes
		self.Pload_number = 0
		self.Pload_widgets = [
			[
				None,
				Label(self.p4,text="Member"),
				Label(self.p4,text="Direction"),
				Label(self.p4,text="P (kN)"),
				Label(self.p4,text="X (m)")
			]
		]

		# dist_load page attributes
		self.Dload_number = 0
		self.Dload_widgets = [
			[
				None,
				Label(self.p5,text="Member"),
				Label(self.p5,text="Direction"),
				Label(self.p5,text="W1 (kN)"),
				Label(self.p5,text="W2 (kN)"),
				Label(self.p5,text="X1 (m)"),
				Label(self.p5,text="X2 (m)")
			]
		]
		
		#widgets of Nodes page
		self.add_node_row()
		self.deploy_widgets(self.Nodes_widgets)  
		self.add_node_button= ttk.Button(self.p1,text="add",command=self.add_node,width=7)
		self.add_node_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		
		# widgets of Members page
		self.add_member_row()
		self.deploy_widgets(self.Members_widgets)  
		self.add_member_button= ttk.Button(self.p2,text="add",command=self.add_member,width=7)
		self.add_member_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		
		# widgets of Supports page
		self.add_support_row()
		self.deploy_widgets(self.Supports_widgets)
		self.add_support_button= ttk.Button(self.p3,text="add",command=self.add_support,width=7)
		self.add_support_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		
		# widgets of point_load
		self.add_Pload_button= ttk.Button(self.p4,text="add",command=self.add_Pload,width=7)
		self.add_Pload_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		
		# widgets of dist_load
		self.add_Dload_button= ttk.Button(self.p5,text="add",command=self.add_Dload,width=7)
		self.add_Dload_button.place(relx=0.9,rely=0.9,anchor=CENTER)
	
	def deploy_widgets(self,widgets_list):
		for row,widgets in enumerate(widgets_list):
			for column,widget in enumerate(widgets):
				if row==0 and column==0:
					continue
				widget.grid(row=row,column=column)
        
	def add_node(self):
		self.node_number= self.node_number + 1
		self.add_node_row()
		self.deploy_widgets(self.Nodes_widgets)
	
	def add_member(self):
		self.member_number= self.member_number + 1
		self.add_member_row()
		self.deploy_widgets(self.Members_widgets)
	
	def add_support(self):
		self.support_number = self.support_number + 1
		self.add_support_row()
		self.deploy_widgets(self.Supports_widgets)
	
	def add_Pload(self):
		self.Pload_number= self.Pload_number + 1
		self.add_Pload_row()
		self.deploy_widgets(self.Pload_widgets)
		
	def add_Dload(self):
		self.Dload_number= self.Dload_number + 1
		self.add_Dload_row()
		self.deploy_widgets(self.Dload_widgets)
	
	def add_node_row(self):
		self.Nodes.update({
			f"N{self.node_number}":{
				"X":DoubleVar(),
				"Y":DoubleVar()
			}
		})
		self.Nodes_widgets.append([
			Label(self.p1,text=f"N{self.node_number}",width=4),
			ttk.Entry(self.p1,textvariable=self.Nodes[f"N{self.node_number}"]["X"],width=9),
			ttk.Entry(self.p1,textvariable=self.Nodes[f"N{self.node_number}"]["Y"],width=9)
		])
		self.update_nodes_list()
		self.update_members_list(self.Supports_widgets,self.Nodes)
  
	def add_member_row(self):
		self.Members.update({
			f"M{self.member_number}":{
				"start_node":StringVar(),
				"end_node":StringVar(),
				"release":StringVar(value="Unrelease")
			}
		})
		self.Members_widgets.append([
			Label(self.p2,text=f"M{self.member_number}",width=4),
			ttk.Combobox(self.p2,values=list(self.Nodes.keys()),textvariable=self.Members[f"M{self.member_number}"]["start_node"],width=6,state="readonly"),
			ttk.Combobox(self.p2,values=list(self.Nodes.keys()),textvariable=self.Members[f"M{self.member_number}"]["end_node"],width=6,state="readonly"),
			ttk.Combobox(self.p2,values=("Start","End","Both","Unrelease"),textvariable=self.Members[f"M{self.member_number}"]["release"],width=9,state="readonly")
		])
		self.update_members_list(self.Pload_widgets,self.Members)
	
	def add_support_row(self):
		self.Supports.update({
			f"S{self.support_number}":{
				"Node":StringVar(),
				"Rx":StringVar(value="Free"),
				"Ry":StringVar(value="Free"),
				"Mz":StringVar(value="Free")
			}
		})
		self.Supports_widgets.append([
	     	Label(self.p3,text=f"S{self.support_number}",width=4),
	     	ttk.Combobox(self.p3,values=list(self.Nodes.keys()),textvariable=self.Supports[f"S{self.support_number}"]["Node"],width=6,state="readonly"),
	     	ttk.Combobox(self.p3,values=("Fixed","Free"),textvariable=self.Supports[f"S{self.support_number}"]["Rx"],width=6,state="readonly"),
	     	ttk.Combobox(self.p3,values=("Fixed","Free"),textvariable=self.Supports[f"S{self.support_number}"]["Ry"],width=6,state="readonly"),
	     	ttk.Combobox(self.p3,values=("Fixed","Free"),textvariable=self.Supports[f"S{self.support_number}"]["Mz"],width=6,state="readonly")
	     ])
	
	def add_Pload_row(self):
		self.Ploads.update({
			f"PL{self.Pload_number}":{
				"Member":StringVar(),
				"Direction":StringVar(value="Fy"),
				"P":DoubleVar(),
				"X":DoubleVar()
			}
		})
		self.Pload_widgets.append([
			Label(self.p4,text=f"PL{self.Pload_number}",width=4),
			ttk.Combobox(self.p4,values=list(self.Members.keys()),textvariable=self.Ploads[f"PL{self.Pload_number}"]["Member"],width=6,state="readonly"),
			ttk.Combobox(self.p4,values=("Fy","Fx","Mz"),textvariable=self.Ploads[f"PL{self.Pload_number}"]["Direction"],width=6,state="readonly"),
			ttk.Entry(self.p4,textvariable=self.Ploads[f"PL{self.Pload_number}"]["P"],width=9),
			ttk.Entry(self.p4,textvariable=self.Ploads[f"PL{self.Pload_number}"]["X"],width=9)
		])
	
	def add_Dload_row(self):
		self.Dloads.update({
			f"DL{self.Dload_number}":{
				"Member":StringVar(),
				"Direction":StringVar(value="Fy"),
				"W1":DoubleVar(),
				"W2":DoubleVar(),
				"X1":DoubleVar(),
				"X2":DoubleVar()
			}
		})
		self.Dload_widgets.append([
			Label(self.p5,text=f"DL{self.Dload_number}",width=4),
			ttk.Combobox(self.p5,values=list(self.Members),textvariable=self.Dloads[f"DL{self.Dload_number}"]["Member"],width=6,state="readonly"),
			ttk.Combobox(self.p5,values=("Fx","Fy"),textvariable=self.Dloads[f"DL{self.Dload_number}"]["Direction"],width=6,state="readonly"),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number}"]["W1"],width=9),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number}"]["W2"],width=9),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number}"]["X1"],width=9),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number}"]["X2"],width=9)
		])

	def update_nodes_list(self):
		for i in range(1,len(self.Members_widgets)):
			for j in range(1,3):
				self.Members_widgets[i][j]["values"]=list(self.Nodes.keys())
	
	def update_members_list(self,widgets_list,var_dict):
		for i in range(1,len(widgets_list)):
			widgets_list[i][1]["values"]=list(var_dict.keys())

	def materials(self):
		material = Toplevel(self)
		material.geometry("400x260")
		material.grab_set()


		main_frame = Frame(material)
		main_frame.pack(padx=10,expand=1,fill="both")

		group_gen_frame = Pmw.Group(main_frame,tag_text="general")
		group_prop_frame = Pmw.Group(main_frame,tag_text="material properties")
		
		gen_frame = Frame(group_gen_frame.interior())
		prop_frame = Frame(group_prop_frame.interior())
		
		group_gen_frame.pack(expand=YES,fill="both",anchor=CENTER)
		group_prop_frame.pack(expand=YES,fill="both",anchor=CENTER)
		
		gen_frame.pack(padx=30,expand=YES,fill="x")
		prop_frame.pack(padx=30,expand=YES,fill="x")

		button_frame = Frame(main_frame)
		button_frame.pack(pady=10,fill="x")
		
		OK = ttk.Button(button_frame,text="OK",width=7)
		OK.pack()

		gen_widgets = (
			(Label(gen_frame,text="Material's name:"),ttk.Combobox(gen_frame,width=9)),
		)

		properties_widgets = (
			(Label(prop_frame,text="elasticity modulus:"),ttk.Entry(prop_frame,width=12)),
			(Label(prop_frame,text="shear modulus:"),ttk.Entry(prop_frame,width=12)),
			(Label(prop_frame,text="poisson modulus:"),ttk.Entry(prop_frame,width=12)),
			(Label(prop_frame,text="volumetric weight:"),ttk.Entry(prop_frame,width=12))
		)
		
		gen_frame.grid_columnconfigure(0,weight=1)
		gen_frame.grid_columnconfigure(1,weight=1)
		prop_frame.grid_columnconfigure(0,weight=1)
		prop_frame.grid_columnconfigure(1,weight=1)

		for i,j in enumerate(gen_widgets):
			j[0].grid(row=i,column=0,sticky="W")
			j[1].grid(row=i,column=1,sticky="E")

		for i,j in enumerate(properties_widgets):
			j[0].grid(row=i,column=0,sticky="W")
			j[1].grid(row=i,column=1,sticky="E")

	def sections(self):
		section = Toplevel(self)
		section.geometry("400x260")
		section.grab_set()


		main_frame = Frame(section)
		main_frame.pack(padx=10,expand=1,fill="both")

		group_gen_frame = Pmw.Group(main_frame,tag_text="general")
		group_prop_frame = Pmw.Group(main_frame,tag_text="section properties")
		
		gen_frame = Frame(group_gen_frame.interior())
		prop_frame = Frame(group_prop_frame.interior())
		
		group_gen_frame.pack(expand=YES,fill="both",anchor=CENTER)
		group_prop_frame.pack(expand=YES,fill="both",anchor=CENTER)
		
		gen_frame.pack(padx=30,expand=YES,fill="x")
		prop_frame.pack(padx=30,expand=YES,fill="x")

		button_frame = Frame(main_frame)
		button_frame.pack(pady=10,fill="x")

		OK = ttk.Button(button_frame,text="OK",width=7)
		OK.pack()

		gen_widgets = (
			(Label(gen_frame,text="Section's name:"),ttk.Combobox(gen_frame,width=9)),
		)

		properties_widgets = (
			(Label(prop_frame,text="Section's material:"),ttk.Combobox(prop_frame,width=9,state="readonly")),
			(Label(prop_frame,text="Moment of inertia:"),ttk.Entry(prop_frame,width=12)),
			(Label(prop_frame,text="Area of section:"),ttk.Entry(prop_frame,width=12)),
		)

		gen_frame.grid_columnconfigure(0,weight=1)
		gen_frame.grid_columnconfigure(1,weight=1)
		prop_frame.grid_columnconfigure(0,weight=1)
		prop_frame.grid_columnconfigure(1,weight=1)

		for i,j in enumerate(gen_widgets):
			j[0].grid(row=i,column=0,sticky="W")
			j[1].grid(row=i,column=1,sticky="E")

		for i,j in enumerate(properties_widgets):
			j[0].grid(row=i,column=0,sticky="W")
			j[1].grid(row=i,column=1,sticky="E")
		
	def analyze(self):
		model = FEModel3D()
		model.add_material("Steel",29000,11200,0.3,2.836e-4)
		
		for i,j in self.Nodes.items():
			model.add_node(i,j["X"].get(),j["Y"].get(),0)
		
		for i,j in self.Members.items():
			model.add_member(i,j["start_node"].get(),j["end_node"].get(),"Steel",10, 15, 25, 2)
			model.def_releases(i,Rzi=self.releases[j["release"].get()][0],Rzj=self.releases[j["release"].get()][1])
		
		for i in self.Supports.values():
			model.def_support(i["Node"].get(),self.free[i["Rx"].get()],self.free[i["Ry"].get()],1,1,1,self.free[i["Mz"].get()])
		
		for i in self.Ploads.values():
			model.add_member_pt_load(i["Member"].get(),i["Direction"].get(),i["P"].get(),i["X"].get())
		
		for i in self.Dloads.values():
			model.add_member_dist_load(i["Member"].get(),i["Direction"].get(),i["W1"].get(),i["W2"].get(),i["X1"].get(),i["X2"].get())
		
		model.analyze()
		
		for i in self.Members.keys():
			model.Members[i].plot_moment("Mz",n_points=1000)

if __name__ == "__main__":
	App = App()
	App.mainloop()