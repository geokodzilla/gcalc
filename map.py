import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter.messagebox import showinfo, showwarning
import os
import math as m
from point import Point
from calc import domiary, przeciecie
from dialog import WDialog

class Map(tk.Canvas):

    """
    
    """
   

    def __init__(self, root, sb, file_wcl):
        super().__init__(root, bg='white', width=1200, height=700)
        self.ratio, self.offset = 1, (0, 0)
        self.focus_set()
        self.bind('<MouseWheel>', self.zoomer)
        self.bind('<Button-4>', lambda e: self.zoomer(e, 1.2))
        self.bind('<Button-5>', lambda e: self.zoomer(e, 0.8))
        self.bind('<ButtonPress-2>', lambda e: self.scan_mark(e.x, e.y))
        self.bind('<B2-Motion>', lambda e: self.scan_dragto(e.x, e.y, gain=1))
        self.sb = sb # statusbar
        
        self.start_point = None
        self.end_point = None
        self.point_number = 1
        
        self.last_circle_id = None
        self.last_line_id = None
        
        self.points = {}
        self.lines = []
        self.obliczone = []
        
        
    def clear_point(self, id):
        if id is not None:
          self.itemconfigure(id, fill='black')
  
    def clear(self):
        self.clear_point(self.start_point.id)
        self.clear_point(self.end_point.id)
        self.start_point = None
        self.end_point = None
        self.delete(self.last_line_id)
        self.lines = []
        self.sb.clear()
        self.sb.set('Wskaż początek linii pomiarowej')
        self.bind("<Button-1>", self.grab_start_point_number)
        
        
    def grab_start_point_number(self, event):
        self.clear_point(self.start_point)
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        items = self.find_closest(x, y)
        self.start_point = self.points[items[0]]
        self.itemconfigure(items[0], fill='blue')
        self.sb.clear()
        self.sb.set('Wskaż koniec linii pomiarowej')
        self.bind("<Button-1>", self.grab_end_point_number)
        
        
    def grab_end_point_number(self, event):
        self.clear_point(self.end_point)
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        items = self.find_closest(x, y)
        self.end_point = self.points[items[0]]
        if self.start_point is not None and self.end_point is not None:
            self.lines.append((self.points[self.start_point.id], self.points[self.end_point.id]))
            self.last_line_id = self.create_line(self.to_canvas_coordinates(self.start_point.y, self.start_point.x),
                                                 self.to_canvas_coordinates(self.end_point.y, self.end_point.x), fill='red', dash=(2,4))
        self.itemconfigure(items[0], fill='blue')
        self.sb.clear()
              
    def to_canvas_coordinates(self, px, py):
        return px*self.ratio + self.offset[0], -py*self.ratio + self.offset[1]

    def to_geographical_coordinates(self, x, y):
        px, py = (x - self.offset[0])/self.ratio, (self.offset[1] - y)/self.ratio
        return px, py

    def import_map(self):
        self.delete('all')
        self.filepath = filedialog.askopenfilename(title='Import txt')
        self.draw_map()
        self.sb.set('Wczytano plik %s' % self.filepath)
    
    def draw_map(self):
        pt = [i.strip().split() for i in open(self.filepath)]
        for p in pt:
            number, x, y = p
            x = float(x)
            y = float(y)
            point = Point(number=number, x=x, y=y)
            t = self.create_text(self.to_canvas_coordinates(point.y, point.x), text=point.number, tags=('osnowa',), anchor=tk.NW)
            self.create_oval(self.to_canvas_coordinates(point.y, point.x), self.to_canvas_coordinates(point.y, point.x), stat=tk.DISABLED)
            point.set_id(t)
            self.points[t] = point
        self.configure(scrollregion=self.bbox('all'))
         
    def linia_bazowa(self):
        if self.start_point is not None and self.end_point is not None:
            self.clear_point(self.start_point.id)
            self.clear_point(self.end_point.id)
        self.bind("<Button-1>", self.grab_start_point_number)
        self.delete(self.last_line_id)
        self.sb.clear()
        self.sb.set('Wskaż początek linii pomiarowej')
        
    def ortog(self):
        self.lines = []
        if self.start_point is not None and self.end_point is not None:
            d = WDialog(self, title='Wprowadź dane', counter=self.point_number)
            res = d.result
            if res is not None:
                odcieta, rzedna, num = d.result
                sp = self.points[self.start_point.id]
                ep = self.points[self.end_point.id]
                nowy = domiary(num, sp, ep, odcieta, rzedna)
                t = self.create_text(self.to_canvas_coordinates(nowy.y, nowy.x), text=nowy.number, tags=('pikieta',), anchor=tk.NW, fill='orange')
                self.last_circle_id = self.create_oval(self.to_canvas_coordinates(nowy.y, nowy.x), self.to_canvas_coordinates(nowy.y, nowy.x), stat=tk.DISABLED)
                nowy.set_id(t)
                self.points[t] = nowy
                self.obliczone.append((sp, ep, nowy))
                self.point_number = num + 1
            else:
                self.clear_point(self.start_point.id)
                self.clear_point(self.end_point.id)
                self.sb.clear()
                self.sb.set('Wskaż początek linii pomiarowej')
                self.bind("<Button-1>", self.grab_start_point_number)
    
    def przeciecie_prostych(self):
        if len(self.lines) == 2:
            sp1, ep1 = self.lines[0]
            sp2, ep2 = self.lines[1]
            num = self.point_number
            nowy = przeciecie(num,sp1, ep1, sp2, ep2)
            self.delete(self.last_line_id)
            t = self.create_text(self.to_canvas_coordinates(nowy.y, nowy.x), text=nowy.number, tags=('pikieta',), anchor=tk.NW, fill='orange')
            self.last_circle_id = self.create_oval(self.to_canvas_coordinates(nowy.y, nowy.x), self.to_canvas_coordinates(nowy.y, nowy.x), stat=tk.DISABLED)
            nowy.set_id(t)
            self.points[t] = nowy
            self.obliczone.append((sp1, ep1, sp2, ep2, nowy))
            self.point_number = num + 1
            self.lines = []
        else:
            self.clear()
                
                   
    def zoomer(self, event, factor=None):
        if not factor:
            factor = 1.2 if event.delta > 0 else 0.8
        event.x, event.y = self.canvasx(event.x), self.canvasy(event.y)
        self.scale('all', event.x, event.y, factor, factor)
        self.configure(scrollregion=self.bbox('all'))
        self.ratio *= float(factor)
        self.offset = (
            self.offset[0]*factor + event.x*(1 - factor),
            self.offset[1]*factor + event.y*(1 - factor)
        )


if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.title('maPY')
    mapy = Map(root_window)
    root_window.mainloop()