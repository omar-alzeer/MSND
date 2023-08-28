from tkinter import *
import Pmw
import json

class App(Tk):
	def __init__(self):
		Tk.__init__(self)
		
		self.inputs = {"Nodes" : {},"Members" : {},"Supports" : {},"Loads" : {}}

		# NoteBook widget
		self.notebook = Pmw.NoteBook(self)
		self.p1 = self.notebook.add("Nodes")
		self.p2 = self.notebook.add("Members")
		self.p3 = self.notebook.add("Supports")
		self.p4 = self.notebook.add("Loads")
		self.notebook.pack(padx=10,pady=10)

		# Nodes page attributes
		self.node_number = 1
		self.Nodes = self.inputs["Nodes"]
		self.Nodes_widgets = [
			[
				None,
				Label(self.p1,text="X"),
				Label(self.p1,text="Y")
			]
		]
		
		# Members page attributes
		self.member_number = 1
		self.Members_widgets = [
			[
				None,
				Label(self.p2,text="Start Node"),
				Label(self.p2,text="End Node")
			]
		]
		
		#widgets of Nodes page
		self.add_node_row()
		self.deploy_widgets(self.Nodes_widgets)	
		self.add_node_button= Button(self.p1,text="add",command=self.add_node)
		self.add_node_button.place(relx=0.9,rely=0.9,anchor=CENTER)
		
		# widgets of Members page
		self.add_member_row()
		self.deploy_widgets(self.Members_widgets)	
		self.add_member_button= Button(self.p2,text="add",command=self.add_member)
		self.add_member_button.place(relx=0.9,rely=0.9,anchor=CENTER)

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
	
	def add_node_row(self):
		self.inputs["Nodes"].update({
			f"N{self.node_number}":{
				"X":StringVar(),
				"Y":StringVar()
			}
		})	
		self.Nodes_widgets.append([
			Label(self.p1,text=f"N{self.node_number}",width=4),
			Entry(self.p1,textvariable=self.Nodes[f"N{self.node_number}"]["X"]),
			Entry(self.p1,textvariable=self.Nodes[f"N{self.node_number}"]["Y"])
		])
		self.update_members()
	
	def add_member_row(self):	
		self.Members_widgets.append([
			Label(self.p2,text=f"M{self.member_number}",width=4),
			Pmw.ComboBox(self.p2,scrolledlist_items=list(self.Nodes.keys())),
			Pmw.ComboBox(self.p2,scrolledlist_items=list(self.Nodes.keys()))
		])
	
	def update_members(self):
		if len(self.Members_widgets) > 1:
			for i in range(1,len(self.Members_widgets)):
				for j in range(1,len(self.Members_widgets[i])):
					self.Members_widgets[i].pop()
				
		for i in range(1,len(self.Members_widgets)):
			for j in range(1,3):
				self.Members_widgets[i].append(Pmw.ComboBox(self.p2,scrolledlist_items=list(self.Nodes.keys())))	
		self.deploy_widgets(self.Members_widgets)
	

if __name__ == '__main__':
	App = App()
	App.mainloop()