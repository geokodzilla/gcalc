import tkinter as tk

class StatusBar(tk.Frame):
    
    """
    Klasa paska statusu programu zrealizowan z wykorzystaniem etykiety
    obsługuje dwie metody ustawjącą status oraz czyszczącą
    """
    
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()