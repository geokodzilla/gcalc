from tkinter import simpledialog
from tkinter.messagebox import showwarning
from tkinter import *


class UpdatePointDialog(Toplevel):
    
    """
    Klasa okna wyszukiwania umożliwiająca wyszukiwanie punktów na mapie
    """
    
    def __init__(self, parent, title = None, counter=1):

        Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.iconbitmap('./img/gcalc.ico')
        self.parent = parent
        self.counter = counter
        self.result = None
        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        Label(master, text="Nowy numer:").grid(row=0)
        self.sp = Entry(master)
        self.sp.grid(row=0, column=1)
        return self.sp

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Anuluj", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()
       
    # PRZYCISKI

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def apply(self):
        self.result =  self.sp.get()
