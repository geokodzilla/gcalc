# -*- coding: utf-8 -*-
import datetime
import tkinter as tk
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter import filedialog, simpledialog
import sys
from map import Map
from status_bar import StatusBar
import os
from search_dialog import SDialog

class App:

    def __init__(self, root):
        self.root = root
        self.root.title(u'Obliczenia graficzne')
        
        # report creation - out directory and filepath
        self.out_path = os.path.join(os.getcwd(), 'out')
        if not os.path.exists(self.out_path):
            os.mkdir(self.out_path)
        self.filename = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt'
        self.file_path = os.path.join(self.out_path, self.filename)
        
        self.status_bar = StatusBar(self.root)
        self.map_canvas = Map(self.root, self.status_bar, self.file_path)
        self.make_widgets()
        self.last_searched = []
        self.root.iconbitmap('./img/gcalc.ico')
        
    def txt_report(self):
        with open(self.file_path, 'w') as outfile:
            for line in self.map_canvas.obliczone:
                wline = ' '.join(line) + '\n'
                outfile.writelines(wline)
            outfile.close()
        showinfo('INFO', 'Zapisano raport %s' % self.filename)
        
    def make_widgets(self):
        
        menu = tk.Menu(self.root)
        menu_obiekty = tk.Menu(menu, tearoff=0)
        menu_etykiety = tk.Menu(menu, tearoff=0)
        menu.add_command(label="Import txt", command=self.map_canvas.import_map)
        menu.add_command(label="Raport txt", command=self.txt_report)
        submenu_liniowe = tk.Menu(menu)
        submenu_liniowe.add_command(label="Linia Bazowa [LB]", command=self.map_canvas.linia_bazowa)
        submenu_liniowe.add_command(label="Miary ortogonalne [MO]", command=self.map_canvas.ortog)
        submenu_liniowe.add_command(label="Przecięcie prostych [PP]", command=self.map_canvas.przeciecie_prostych)
        submenu_liniowe.add_command(label="Szukaj", command=self.search)
        submenu_liniowe.add_command(label="Anuluj", command=self.map_canvas.clear)
        
        menu.add_cascade(label="Obliczenia", menu=submenu_liniowe)
        
        
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        StartButton = tk.Button(self.toolbar, text='LB', relief=tk.FLAT,
            command=self.map_canvas.linia_bazowa)
        StartButton.pack(side=tk.LEFT, padx=2, pady=2)
        CalcButton = tk.Button(self.toolbar, text='MO', relief=tk.FLAT,
            command=self.map_canvas.ortog)
        CalcButton.pack(side=tk.LEFT, padx=2, pady=2)
        CalcButton = tk.Button(self.toolbar, text='PP', relief=tk.FLAT,
            command=self.map_canvas.przeciecie_prostych)
        CalcButton.pack(side=tk.LEFT, padx=2, pady=2)
        SearchButton = tk.Button(self.toolbar, text='Szukaj', relief=tk.FLAT,
            command=self.search)
        SearchButton.pack(side=tk.LEFT, padx=2, pady=2)
        ClearButton = tk.Button(self.toolbar, text='Anuluj', relief=tk.FLAT,
            command=self.map_canvas.clear)
        ClearButton.pack(side=tk.LEFT, padx=2, pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.root.config(menu=menu)
        self.map_canvas.pack(fill='both', expand=1)
        self.status_bar.pack(side=tk.LEFT)
        
    def search(self):
        if len(self.last_searched) > 0:
            for elem in self.last_searched:
                i, c = elem
                self.map_canvas.itemconfigure(i, fill=c)
        d = SDialog(self.root, title='Szukaj')
        if d.result is not None:
          id = d.result
        else:
          id = ''
        try:
            for cid, pt in self.map_canvas.points.items():
                if pt.number == id:
                    self.last_searched.append((cid, self.map_canvas.itemcget(cid, 'fill')))
                    self.map_canvas.itemconfigure(cid, fill='red')
                    self.map_canvas.configure(scrollregion=self.map_canvas.bbox(cid))
        except KeyError:
            showwarning('UWAGA', 'Brak punktu o numerze %s' % id)
                  
   
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()