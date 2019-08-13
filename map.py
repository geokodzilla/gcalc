import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter.messagebox import showinfo, showwarning
import os
import math as m
from point import Point
from calc import domiary, przeciecie
from dialog import WDialog
from update_point_dialog import UpdatePointDialog


class Map(tk.Canvas):

    """
    Klasa będąca reprezentacją mapy dziedzicząca z bazowej klasy canvas
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
        """
        Przywracanie konfiguracji bazowej punktu
        """
        if id is not None:
          self.itemconfigure(id, fill='black')
  
    def clear(self):
        """
        Anulowanie aktualnie realizowanej akcji
        """
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
        """
        Metoda umożliwia wskazanie początku linii bazowej
        Jedna linia bazowa umożliwa obliczenie miar ortogonalnych
        Wskazanie dwóch po kolei umożliwia wyznaczenie ich przecięcia
        """
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
        """
        Metoda umożliwia wskazanie końca linii bazowej
        """
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
        """
        metoda konwertuje współrzędne geodezyjne na współrzędne obiektu canvas
        """
        return px*self.ratio + self.offset[0], -py*self.ratio + self.offset[1]

    def to_geographical_coordinates(self, x, y):
        """
        metoda konwertuje współrzędne obiektu canvas na współrzędne geodezyjne
        """
        px, py = (x - self.offset[0])/self.ratio, (self.offset[1] - y)/self.ratio
        return px, py

    def import_map(self):
        """
        Metoda wczytująca dane z pliku
        """
        self.delete('all')
        self.filepath = filedialog.askopenfilename(title='Import txt')
        self.draw_map()
        self.sb.set('Wczytano plik %s' % self.filepath)
    
    def draw_map(self):
        """
        Metoda odpowiedzialna za rysowanie wczytywanych punktów
        """
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
        """
        Metoda inicjująca wskazywanie linii bazowej
        """
        if self.start_point is not None and self.end_point is not None:
            self.clear_point(self.start_point.id)
            self.clear_point(self.end_point.id)
        self.bind("<Button-1>", self.grab_start_point_number)
        self.delete(self.last_line_id)
        self.sb.clear()
        self.sb.set('Wskaż początek linii pomiarowej')
        
        
    def update_point_shortcut(self):
        self.bind("<Button-1>", self.update_point)
        self.sb.clear()
        self.sb.set('Wskaż punkt - zmiana numeru')
        
    def update_point(self, event):
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        items = self.find_closest(x, y)
        point = self.points[items[0]]
        tags = self.gettags(items[0])
        fill = self.itemcget(items[0], 'fill')
        d = UpdatePointDialog(self, title='Nowy numer')
        if d.result is not None:
          new_number = d.result
          self.delete(items[0])
          del self.points[items[0]]
          point.change_number(new_number)
          t = self.create_text(self.to_canvas_coordinates(point.y, point.x), text=point.number, tags=tags, anchor=tk.NW, fill=fill)
          point.set_id(t)
          self.points[t] = point
          self.obliczone_update(items[0], point)
          
          
    def obliczone_update(self, id, new_point):
        if len(self.obliczone) > 0:
            for nr, row in enumerate(self.obliczone):
                for index, k in enumerate(row[1]):
                    if id == k:
                        self.obliczone[nr][0][index+1] = str(new_point)
                        self.obliczone[nr][1][index] = new_point.id
          
    def ortog(self):
        """
        Metoda do obliczania miar ortogonalnych na podstawie elementów wskazanych przez
        użytkownika na mapie
        """
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
                self.obliczone.append((['MO', str(sp), str(ep), str(nowy), str(odcieta), str(rzedna)], [sp.id, ep.id, nowy.id]))
                self.point_number = num + 1
            else:
                self.clear_point(self.start_point.id)
                self.clear_point(self.end_point.id)
                self.sb.clear()
                self.sb.set('Wskaż początek linii pomiarowej')
                self.bind("<Button-1>", self.grab_start_point_number)
    
    def przeciecie_prostych(self):
        """
        Metoda do obliczania przecięcia prostych na podstawie elementów
        wskazanych przez użytkownika
        """
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
            self.obliczone.append((['PP', str(sp1), str(ep1), str(sp2), str(ep2), str(nowy)], [sp1.id, ep1.id, sp2.id, ep2.id, nowy.id]))
            self.point_number = num + 1
            self.lines = []
        else:
            self.clear()
                
                   
    def zoomer(self, event, factor=None):
        """
        Metoda obsługująca powiększanie i pomniejszanie zakresu mapy
        """
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