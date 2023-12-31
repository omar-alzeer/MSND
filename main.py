from tkinter import *
from tkinter import ttk
import Pmw
from PyNite import FEModel3D

class App(Tk):
	def __init__(self):
		Tk.__init__(self)

		self.geometry("430x585")
		self.title("MSND")

		self.inputs = {
			"Nodes" : {},
			"Members" : {},
			"Supports" : {},
			"Loads" : {
				"Pload":{},
				"Dload":{}
			},
			"Materials":{
				"concrete":{
					"E":3.2836e+7,
					"G":13681666.667,
					"P":0.2,
					"W":25
				},
				"steel":{
					"E":2.1e+8,
					"G":80769230.769,
					"P":0.3,
					"W":76.98
				}
			},
			"Sections":{
				"default":{
					"material":"concrete",
					"Iz":0.00208,
					"A":0.1
				}
			}
		}
		
		self.free = {
			"Fixed":True,
			"Free":False
		}

		self.releases = {
			"Start":(True,False),
			"End":(False,True),
			"Both":(True,True),
			"Unrelease":(False,False)
		}

		self.Nodes = self.inputs["Nodes"]
		self.Members = self.inputs["Members"]
		self.Supports = self.inputs["Supports"]
		self.Ploads = self.inputs["Loads"]["Pload"]
		self.Dloads = self.inputs["Loads"]["Dload"]
		self.Materials = self.inputs["Materials"]
		self.Sections = self.inputs["Sections"]
		
		self.nodes_id = {}
		self.members_id = {}
		self.nodes_var = []
		self.nome={}
		#Menu widget
		self.menu = Menu(self,tearoff=False)
		self.config(menu=self.menu)
		
		self.run = Menu(self.menu,tearoff=False)
		self.run.add_command(label="Bending",command=lambda : self.analyze("BM"))
		self.run.add_command(label="Shear",command=lambda : self.analyze("SF"))
		self.run.add_command(label="Normal",command=lambda : self.analyze("NF"))
		self.run.add_command(label="Deflection",command=lambda : self.analyze("D"))
		self.run.add_command(label="Reactions",command=lambda : self.analyze("R"))
		self.menu.add_cascade(label="Run", menu=self.run)

		self.define = Menu(self.menu,tearoff=False)
		self.define.add_command(label="materials",command=self.materials)
		self.define.add_command(label="sections",command=self.sections)
		self.menu.add_cascade(label="Define", menu=self.define)

		self.help = Menu(self.menu,tearoff=False)
		self.help.add_command(label="About")
		self.menu.add_cascade(label="Help", menu=self.help)
		
		#Canvas
		self.board = Canvas(self,height=300,width=100,bg="white",relief=SOLID,borderwidth=1)
		self.board.pack(fill="both",expand=True,padx=(10,5),pady=10)
		
		# NoteBook widget
		self.notebook = Pmw.NoteBook(self)
		self.p1 = self.notebook.add("Nodes")
		self.p2 = self.notebook.add("Members")
		self.p3 = self.notebook.add("Supports")
		self.p4 = self.notebook.add("Point load")
		self.p5 = self.notebook.add("Dist load")
		self.notebook.pack()
		
		# Nodes page attributes
		self.node_number = [0]
		self.Nodes_widgets = [
			[
				None,
				Label(self.p1,text="X (m)"),
				Label(self.p1,text="Y (m)")
			]
		]
		
		# Members page attributes
		self.member_number = [0]
		self.Members_widgets = [
			[
				None,
				Label(self.p2,text="Start"),
				Label(self.p2,text="End"),
				Label(self.p2,text="Release"),
				Label(self.p2,text="Section"),
				Label(self.p2,text="I-mod")
			]
		]
		
		# Supports page attributes
		self.support_number = [0]
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
		self.Pload_number = [0]
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
		self.Dload_number = [0]
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
		self.add_node_button= ttk.Button(self.p1,text="add",command=self.add_node,width=7)
		self.del_node_button= ttk.Button(self.p1,text="delete",command=lambda:self.delete_widgets_row(self.Nodes_widgets,2,self.node_number,self.Nodes),width=7)
		self.add_node_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		self.del_node_button.place(relx=0.75,rely=0.9,anchor=CENTER)
		self.add_node_row()
		self.deploy_widgets(self.Nodes_widgets)  
		
		# widgets of Members page
		self.add_member_button= ttk.Button(self.p2,text="add",command=self.add_member,width=7)
		self.del_member_button= ttk.Button(self.p2,text="delete",command=lambda:self.delete_widgets_row(self.Members_widgets,2,self.member_number,self.Members),width=7)
		self.add_member_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		self.del_member_button.place(relx=0.75,rely=0.9,anchor=CENTER)
		self.add_member_row()
		self.deploy_widgets(self.Members_widgets)  
		
		# widgets of Supports page
		self.add_support_button= ttk.Button(self.p3,text="add",command=self.add_support,width=7)
		self.del_support_button= ttk.Button(self.p3,text="delete",command=lambda:self.delete_widgets_row(self.Supports_widgets,2,self.support_number,self.Supports),width=7)
		self.add_support_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		self.del_support_button.place(relx=0.75,rely=0.9,anchor=CENTER)
		self.add_support_row()
		self.deploy_widgets(self.Supports_widgets)
		
		# widgets of point_load
		self.add_Pload_button= ttk.Button(self.p4,text="add",command=self.add_Pload,width=7)
		self.del_Pload_button= ttk.Button(self.p4,text="delete",command=lambda:self.delete_widgets_row(self.Pload_widgets,1,self.Pload_number,self.Ploads),width=7)
		self.add_Pload_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		self.del_Pload_button.place(relx=0.75,rely=0.9,anchor=CENTER)
		
		# widgets of dist_load
		self.add_Dload_button= ttk.Button(self.p5,text="add",command=self.add_Dload,width=7)
		self.del_Dload_button= ttk.Button(self.p5,text="delete",command=lambda:self.delete_widgets_row(self.Dload_widgets,1,self.Dload_number,self.Dloads),width=7)
		self.add_Dload_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		self.del_Dload_button.place(relx=0.75,rely=0.9,anchor=CENTER)
		
	def draw_node(self,*args,name,varx,vary):
		if name in self.nodes_id:
			self.board.delete(self.nodes_id[name])
		if name in self.nome:
			for i in self.nome[name]:
				self.draw_member("Node",name=i,start=None,end=None)
		
		try:		
			self.board.create_oval(varx.get(),vary.get(),varx.get()+7,vary.get()+7,fill="red")
		except TclError:
			return
		self.nodes_id.update({
			name:self.board.find_all()[-1]
		})
	
	def draw_member(self,*args,name,start,end):
		if args[0] == "Node":
			self.board.delete(self.members_id[name])
			self.Members[name]["start_node"].set("")
			self.Members[name]["end_node"].set("")
			return
		if name in self.members_id:
			self.board.delete(self.members_id[name])
		try:
			sx = self.Nodes[start.get()]["X"].get()
			sy = self.Nodes[start.get()]["Y"].get()
			ex = self.Nodes[end.get()]["X"].get()
			ey = self.Nodes[end.get()]["Y"].get()
		except KeyError:
			return
		
		self.board.create_line(sx+4,sy+4,ex+4,ey+4,width=3,fill="blue")
		
		self.members_id.update({
			name:self.board.find_all()[-1]
		})
		
		if start.get() in self.nome:
			self.nome[start.get()].append(name)
		else:
			self.nome.update({
				start.get():[name]
			})
		
		if end.get() in self.nome:
			self.nome[end.get()].append(name)
		else:
			self.nome.update({
				end.get():[name]
			})
		
		for i in list(self.nodes_id.values()):
			self.board.tag_raise(i)
				
	def deploy_widgets(self,widgets_list):
		for row,widgets in enumerate(widgets_list):
			for column,widget in enumerate(widgets):
				if row==0 and column==0:
					continue
				widget.grid(row=row,column=column)
        
	def add_node(self):
		self.add_node_row()
		self.deploy_widgets(self.Nodes_widgets)
	
	def add_member(self):
		self.add_member_row()
		self.deploy_widgets(self.Members_widgets)
	
	def add_support(self):
		self.add_support_row()
		self.deploy_widgets(self.Supports_widgets)
	
	def add_Pload(self):
		self.add_Pload_row()
		self.deploy_widgets(self.Pload_widgets)
		
	def add_Dload(self):
		self.add_Dload_row()
		self.deploy_widgets(self.Dload_widgets)
	
	def add_node_row(self):
		self.node_number.append(self.node_number[-1]+1)
		name = f"N{self.node_number[-1]}"
		
		self.Nodes.update({
			name:{
				"X":DoubleVar(),
				"Y":DoubleVar()
			}
		})
		
		varx = self.Nodes[name]["X"]
		vary = self.Nodes[name]["Y"]
		
		varx.trace("w",lambda *_,name=name,varx=varx,vary=vary: self.draw_node(*_,name=name,varx=varx,vary=vary))
		vary.trace("w",lambda *_,name=name,varx=varx,vary=vary: self.draw_node(*_,name=name,varx=varx,vary=vary))
		self.Nodes_widgets.append([
			Label(self.p1,text=name,width=4),
			ttk.Entry(self.p1,textvariable=varx,width=9),
			ttk.Entry(self.p1,textvariable=vary,width=9)
		])
		self.nodes_var.append(varx._name)
		self.nodes_var.append(vary._name)
		self.update_nodes_list()
		self.update_members_list(self.Supports_widgets,self.Nodes,1)
  
	def add_member_row(self):
		self.member_number.append(self.member_number[-1]+1)
		name = f"M{self.member_number[-1]}"
		
		self.Members.update({
			f"M{self.member_number[-1]}":{
				"start_node":StringVar(),
				"end_node":StringVar(),
				"release":StringVar(value="Unrelease"),
				"section":StringVar(value="default"),
				"modifier":IntVar(value=1)
			}
		})
		
		start = self.Members[name]["start_node"]
		end = self.Members[name]["end_node"]
		
		start.trace("w",lambda *_,name=name,start=start,end=end: self.draw_member(*_,name=name,start=start,end=end))
		end.trace("w",lambda *_,name=name,start=start,end=end: self.draw_member(*_,name=name,start=start,end=end))
		
		self.Members_widgets.append([
			Label(self.p2,text=name,width=4),
			ttk.Combobox(self.p2,values=list(self.Nodes.keys()),textvariable=start,width=6,state="readonly"),
			ttk.Combobox(self.p2,values=list(self.Nodes.keys()),textvariable=end,width=6,state="readonly"),
			ttk.Combobox(self.p2,values=("Start","End","Both","Unrelease"),textvariable=self.Members[name]["release"],width=9,state="readonly"),
			ttk.Combobox(self.p2,values=list(self.Sections.keys()),textvariable=self.Members[name]["section"],width=6,state="readonly"),
			ttk.Entry(self.p2,textvariable=self.Members[name]["modifier"],width=9)
		])
		self.update_members_list(self.Pload_widgets,self.Members,1)
		self.update_members_list(self.Dload_widgets,self.Members,1)
	
	def add_support_row(self):
		self.support_number.append(self.support_number[-1]+1)
		self.Supports.update({
			f"S{self.support_number[-1]}":{
				"Node":StringVar(),
				"Rx":StringVar(value="Fixed"),
				"Ry":StringVar(value="Fixed"),
				"Mz":StringVar(value="Fixed")
			}
		})
		self.Supports_widgets.append([
	     	Label(self.p3,text=f"S{self.support_number[-1]}",width=4),
	     	ttk.Combobox(self.p3,values=list(self.Nodes.keys()),textvariable=self.Supports[f"S{self.support_number[-1]}"]["Node"],width=6,state="readonly"),
	     	ttk.Combobox(self.p3,values=("Fixed","Free"),textvariable=self.Supports[f"S{self.support_number[-1]}"]["Rx"],width=6,state="readonly"),
	     	ttk.Combobox(self.p3,values=("Fixed","Free"),textvariable=self.Supports[f"S{self.support_number[-1]}"]["Ry"],width=6,state="readonly"),
	     	ttk.Combobox(self.p3,values=("Fixed","Free"),textvariable=self.Supports[f"S{self.support_number[-1]}"]["Mz"],width=6,state="readonly")
	     ])
	
	def add_Pload_row(self):
		self.Pload_number.append(self.Pload_number[-1]+1)
		self.Ploads.update({
			f"PL{self.Pload_number[-1]}":{
				"Member":StringVar(),
				"Direction":StringVar(value="Fy"),
				"P":DoubleVar(),
				"X":DoubleVar()
			}
		})
		self.Pload_widgets.append([
			Label(self.p4,text=f"PL{self.Pload_number[-1]}",width=4),
			ttk.Combobox(self.p4,values=list(self.Members.keys()),textvariable=self.Ploads[f"PL{self.Pload_number[-1]}"]["Member"],width=6,state="readonly"),
			ttk.Combobox(self.p4,values=("Fy","Fx","Mz"),textvariable=self.Ploads[f"PL{self.Pload_number[-1]}"]["Direction"],width=6,state="readonly"),
			ttk.Entry(self.p4,textvariable=self.Ploads[f"PL{self.Pload_number[-1]}"]["P"],width=9),
			ttk.Entry(self.p4,textvariable=self.Ploads[f"PL{self.Pload_number[-1]}"]["X"],width=9)
		])
	
	def add_Dload_row(self):
		self.Dload_number.append(self.Dload_number[-1]+1)
		self.Dloads.update({
			f"DL{self.Dload_number[-1]}":{
				"Member":StringVar(),
				"Direction":StringVar(value="Fy"),
				"W1":DoubleVar(),
				"W2":DoubleVar(),
				"X1":DoubleVar(),
				"X2":DoubleVar()
			}
		})
		self.Dload_widgets.append([
			Label(self.p5,text=f"DL{self.Dload_number[-1]}",width=4),
			ttk.Combobox(self.p5,values=list(self.Members),textvariable=self.Dloads[f"DL{self.Dload_number[-1]}"]["Member"],width=6,state="readonly"),
			ttk.Combobox(self.p5,values=("Fx","Fy"),textvariable=self.Dloads[f"DL{self.Dload_number[-1]}"]["Direction"],width=6,state="readonly"),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number[-1]}"]["W1"],width=9),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number[-1]}"]["W2"],width=9),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number[-1]}"]["X1"],width=9),
			ttk.Entry(self.p5,textvariable=self.Dloads[f"DL{self.Dload_number[-1]}"]["X2"],width=9)
		])

	def delete_widgets_row(self,widgets_list,list_num,widget_number,input):
		if len(widgets_list) > list_num:
			for i in widgets_list[-1]:
				i.destroy()
			widget_number.pop()
			widgets_list.pop()
			input.popitem()

			if len(widgets_list) == 1:
				for i in widgets_list[-1]:
					if i == None : continue
					i.grid_remove()

	def update_nodes_list(self):
		for i in range(1,len(self.Members_widgets)):
			for j in range(1,3):
				self.Members_widgets[i][j]["values"]=list(self.Nodes.keys())
	
	def update_members_list(self,widgets_list,var_dict,widget_num):
		for i in range(1,len(widgets_list)):
			widgets_list[i][widget_num]["values"]=list(var_dict.keys())

	def materials(self):
		def materials_ok():
			self.Materials.update({
				gen_widgets[0][1].get():{
					"E":properties_widgets[0][1].get(),
					"G":properties_widgets[1][1].get(),
					"P":properties_widgets[2][1].get(),
					"W":properties_widgets[3][1].get()
				}
			})
			gen_widgets[0][1]["values"] = list(self.Materials.keys())
		
		def materials_set(event):
			for i,j in enumerate(properties_widgets):
				j[1].delete(0,END)
				j[1].insert(0,list(self.Materials[gen_widgets[0][1].get()].values())[i])
				
			
		material = Toplevel(self)
		material.geometry("400x260")
		material.title("Materials")
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
		
		OK = ttk.Button(button_frame,text="OK",width=7,command=materials_ok)
		OK.pack()

		gen_widgets = (
			(Label(gen_frame,text="Material's name:"),ttk.Combobox(gen_frame,width=9,values=list(self.Materials.keys()))),
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
			
		gen_widgets[0][1].bind("<<ComboboxSelected>>",materials_set)
	
	def sections(self):
		def sections_ok():
			self.Sections.update({
				gen_widgets[0][1].get():{
					"material":properties_widgets[0][1].get(),
					"Iz":properties_widgets[1][1].get(),
					"A":properties_widgets[2][1].get()
				}
			})
			gen_widgets[0][1]["values"] = list(self.Sections.keys())
			self.update_members_list(self.Members_widgets,self.Sections,4)
		
		def sections_set(event):
			for i,j in enumerate(properties_widgets):
				j[1].delete(0,END)
				j[1].insert(0,list(self.Sections[gen_widgets[0][1].get()].values())[i])
		
		section = Toplevel(self)
		section.geometry("400x260")
		section.title("Sections")
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

		OK = ttk.Button(button_frame,text="OK",width=7,command=sections_ok)
		OK.pack()

		gen_widgets = (
			(Label(gen_frame,text="Section's name:"),ttk.Combobox(gen_frame,values=list(self.Sections.keys()),width=9)),
		)

		properties_widgets = (
			(Label(prop_frame,text="Section's material:"),ttk.Combobox(prop_frame,width=9,values=list(self.Materials.keys()))),
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
			
		gen_widgets[0][1].bind("<<ComboboxSelected>>",sections_set)
	
	def reactions(self,nodes,model):
		reaction = Toplevel(self)
		reaction.title("Reactions")
		reaction.grab_set()
		
		widgets = [
			[
				None,
				Label(reaction,text="Rx"),
				Label(reaction,text="Ry"),
				Label(reaction,text="Mz")
			]
		]
		
		for i in nodes:
			widgets.append([
				Label(reaction,text=i,width=4),
				Label(reaction,text=round(model.Nodes[i].RxnFX["Combo 1"],3),bg="white",borderwidth=1,relief="solid",width=9),
				Label(reaction,text=round(model.Nodes[i].RxnFY["Combo 1"],3),bg="white",borderwidth=1,relief="solid",width=9),
				Label(reaction,text=round(model.Nodes[i].RxnMZ["Combo 1"],3),bg="white",borderwidth=1,relief="solid",width=9)
			])
		self.deploy_widgets(widgets)
		
	def analyze(self,internal_force):
		model = FEModel3D()
		
		for name,j in self.Materials.items():
			model.add_material(
				name,
				float(j["E"]),
				float(j["G"]),
				float(j["P"]),
				float(j["W"]))
		
		for name,j in self.Nodes.items():
			model.add_node(
				name,
				j["X"].get(),
				j["Y"].get(),0)
			
		for i,j in self.Members.items():
			model.add_member(
				i,
				j["start_node"].get(),
				j["end_node"].get(),
				self.Sections[j["section"].get()]["material"],1,
				j["modifier"].get()*float(self.Sections[j["section"].get()]["Iz"]),1,
				float(self.Sections[j["section"].get()]["A"]))
				
			model.def_releases(
				i,
				Rzi=self.releases[j["release"].get()][0],
				Rzj=self.releases[j["release"].get()][1])
		
		for i in self.Supports.values():
			model.def_support(
				i["Node"].get(),
				self.free[i["Rx"].get()],
				self.free[i["Ry"].get()],1,1,1,
				self.free[i["Mz"].get()])
		
		for i in self.Ploads.values():
			model.add_member_pt_load(
				i["Member"].get(),
				i["Direction"].get(),
				i["P"].get(),i["X"].get())
				
		for i in self.Dloads.values():			  
			model.add_member_dist_load(		     
				i["Member"].get(),				 
				i["Direction"].get(),
				i["W1"].get(),i["W2"].get(),
				i["X1"].get(),i["X2"].get())
		
		model.analyze()
		
		if internal_force == "BM":
			for i in self.Members.keys():
				model.Members[i].plot_moment("Mz",n_points=1000)
				
		elif internal_force == "SF":
			for i in self.Members.keys():
				model.Members[i].plot_shear("Fy",n_points=1000)
		
		elif internal_force == "NF":
			for i in self.Members.keys():
				model.Members[i].plot_axial(n_points=1000)
		
		elif internal_force == "D":
			for i in self.Members.keys():
				model.Members[i].plot_deflection("dy",n_points=1000)
		
		elif internal_force == "R":
			self.reactions(self.Nodes.keys(),model)

if __name__ == "__main__":
	App = App()
	App.mainloop()