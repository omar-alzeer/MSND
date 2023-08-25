from tkinter import *
import Pmw

class App(Tk):
	def __init__(self):
		Tk.__init__(self)

		self.inputs = {
			"Nodes" : {
				"N1" : [[StringVar(),StringVar()]]
			},
			"Members" : {
				"Member1" : []
			},
			"Supports" : {
				"Support1" : []
			},
			"Loads" : {
				"Load1" : []
			} 
		}

		self.widgets = {
			"Nodes":{
				"Lables":[1],
				"Entries":[[StringVar(),StringVar()]]
			}
		}

		# NoteBook widget
		self.notebook = Pmw.NoteBook(self)
		self.p1 = self.notebook.add("Nodes")
		self.p1 = self.notebook.add("Members")
		self.p1 = self.notebook.add("Supports")
		self.p1 = self.notebook.add("Loads")
		self.notebook.pack(padx=10,pady=10)

		# Nodes widgets
		for i in self.widgets:
			

	def add_node(self):
		pass


if __name__ == '__main__':
	App = App()
	App.mainloop()