from __future__ import annotations
import math


class CanvasManager:
    """Manages canvas drawing operations"""
    
    def __init__(self, app: App):
        self.app = app
        self.nodes_members = {}
        self.nodes_supports = {}
        self.scales = []
        self.var_scale = 1
        
    def draw_node(self, name, varx, vary):
        if name in self.app.Nodes:
            self.app.board.delete(name)
        
        # to delete members after changing nodes position
        if name in self.nodes_members:
            n = self.nodes_members[name]
            for i in range(len(n)):
                start = self.app.Members[n[i]]["start_node"]
                end = self.app.Members[n[i]]["end_node"]
                start.set(start.get())
                end.set(end.get())
                
        if name in self.nodes_supports:
            self.app.Supports[self.nodes_supports[name]]["Node"].set(name)
            
        try:        
            self.app.board.create_oval(varx.get(),vary.get(),varx.get()+8,vary.get()+8,fill="red",tags=name)
        except TclError:
            return

        for i in self.scales:
            self.app.board.scale(name,i[0],i[1],i[2],i[3])
    
    def draw_member(self, name, start, end):
        if name in self.app.Members:
            self.app.board.delete(name)
        try:
            sx = self.app.Nodes[start.get()]["X"].get()
            sy = self.app.Nodes[start.get()]["Y"].get()
            ex = self.app.Nodes[end.get()]["X"].get()
            ey = self.app.Nodes[end.get()]["Y"].get()
        except:
            return
        
        self.app.board.create_line(sx+4,sy+4,ex+4,ey+4,width=3,fill="blue",tags=name) # number 4 is to makke "start,end" in center of node
        
        self._update_member_nodes(name, start_node, end_node)
        self._raise_nodes_above_members()

    def draw_support(self,*args,name,theta):

        def draw_roller_support(name,x,y):
            self.app.board.create_line(x.get()+4,y.get()+4,x.get()+20,y.get()+20,width=3,fill="#11da11",tags=name)
            self.app.board.create_line(x.get()+4,y.get()+4,x.get()-12,y.get()+20,width=3,fill="#11da11",tags=name)
            self.app.board.create_line(x.get()+20,y.get()+20,x.get()-12,y.get()+20,width=3,fill="#11da11",tags=name)
            self.app.board.create_line(x.get()+20,y.get()+25,x.get()-12,y.get()+25,width=3,fill="#11da11",tags=name)

        def draw_pinned_support(name,x,y):
            self.app.board.create_line(x.get()+4,y.get()+4,x.get()+20,y.get()+20,width=3,fill="#11da11",tags=name)
            self.app.board.create_line(x.get()+4,y.get()+4,x.get()-12,y.get()+20,width=3,fill="#11da11",tags=name)
            self.app.board.create_line(x.get()+20,y.get()+20,x.get()-12,y.get()+20,width=3,fill="#11da11",tags=name)
            for i in range(-12,20,7):
                self.app.board.create_line(x.get()+i,y.get()+20,x.get()+(i-4),y.get()+28,width=3,fill="#11da11",tags=name)

        def draw_fixed_support(name,x,y):
            self.app.board.create_line(x.get()-12,y.get()+4,x.get()+20,y.get()+4,width=3,fill="#11da11",tags=name)
            for i in range(-12,20,7):
                self.app.board.create_line(x.get()+i,y.get()+4,x.get()+(i-4),y.get()+12,width=3,fill="#11da11",tags=name)
        
        x = self.app.Nodes[self.app.Supports[name]["Node"].get()]["X"]
        y = self.app.Nodes[self.app.Supports[name]["Node"].get()]["Y"]
        Rx = self.app.Supports[name]["Rx"].get()
        Ry = self.app.Supports[name]["Ry"].get()
        Mz = self.app.Supports[name]["Mz"].get()

        if name in self.app.Supports:
            self.app.board.delete(name)
            
        try:        
            if Rx=="Fixed" and Ry=="Fixed" and Mz=="Fixed":
                draw_fixed_support(name,x,y)
            elif Rx=="Free" and Ry=="Fixed" and Mz=="Free":
                draw_roller_support(name,x,y)
            elif Rx=="Fixed" and Ry=="Free" and Mz=="Free":
                draw_roller_support(name,x,y)
            elif Rx=="Fixed" and Ry=="Fixed" and Mz=="Free":
                draw_pinned_support(name,x,y)

            self.rotate(name,x.get()+4,y.get()+4,theta.get())
            self.nodes_supports.update({
                self.app.Supports[name]["Node"].get():name
            })

        except TclError:
            return

        for i in self.scales:
            self.app.board.scale(name,i[0],i[1],i[2],i[3])

    def start_pan(self, e):
        self.app.board.scan_mark(e.x, e.y)

    def move_screen(self, e):
        self.app.board.scan_dragto(e.x, e.y, gain=1)

    def zoom(self,e,zoom_status):
        x = self.app.board.canvasx(e.x)
        y = self.app.board.canvasy(e.y)

        if zoom_status=="in":
            self.app.board.scale("all", x, y, 11/10, 11/10)
            self.scales.append((x,y, 11/10, 11/10))
            self.var_scale *= 11/10
            

        elif zoom_status=="out":
            self.app.board.scale("all", x, y, 10/11, 10/11)
            self.scales.append((x,y, 10/11, 10/11))
            self.var_scale *= 10/11
            
    def rotate(self, tag, cx, cy, degrees):
        """Rotate all shapes with the given tag around point (cx, cy)."""
        radians = math.radians(degrees)
        cos_theta = math.cos(radians)
        sin_theta = math.sin(radians)
    
        def rotate_point(px, py):
            # Translate to origin
            x_translated = px - cx
            y_translated = py - cy
            
            # Rotate
            x_rotated = x_translated * cos_theta - y_translated * sin_theta
            y_rotated = x_translated * sin_theta + y_translated * cos_theta
            
            # Translate back
            return (x_rotated + cx, y_rotated + cy)
    
        items = self.app.board.find_withtag(tag)
        for item in items:
            coords = self.app.board.coords(item)
            new_coords = []
            for i in range(0, len(coords), 2):
                px, py = coords[i], coords[i+1]
                rx, ry = rotate_point(px, py)
                new_coords.extend([rx, ry])
            self.app.board.coords(item, *new_coords)
    
    def _update_member_nodes(self, member, start_node, end_node):
        """Update the member_nodes dictionary to track connections"""
        for node in [start_node, end_node]:
            if node in self.nodes_members:
                if member not in self.nodes_members[node]:
                    self.nodes_members[node].append(member)
            else:
                self.nodes_members[node] = [member]
    
    def _raise_nodes_above_members(self):
        """Ensure nodes are displayed above members"""
        for node in self.app.Nodes.values():
            self.app.board.tag_raise(node)