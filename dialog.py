from tkinter import simpledialog
from tkinter.messagebox import showwarning
from tkinter import *


class WDialog(Toplevel):
    
    """
    Klasa okna do obliczeń miar ortogonalnych, użytkownik może podać numer punktu
    oraz odciętą i rzędną do punktu
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

    #
    # construction hooks

    def body(self, master):
        Label(master, text="Numer punktu: ").grid(row=0)
        Label(master, text="Odcięta: ").grid(row=1)
        Label(master, text="Rzędna: ").grid(row=2)
        self.numer = Entry(master)
        self.odcieta = Entry(master)
        self.rzedna = Entry(master)
        self.numer.grid(row=0, column=1)
        self.odcieta.grid(row=1, column=1)
        self.rzedna.grid(row=2, column=1)
        self.numer.insert(0, str(self.counter))
        return self.odcieta # initial focus

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Anuluj", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        try:
            self.odci = float(self.odcieta.get())
            self.rzed = float(self.rzedna.get())
            self.num = int(self.numer.get())
            return 1
        except ValueError:
            showwarning(
                "Błąd danych",
                "Źle wpisano dane"
            )
            return 0

    def apply(self):
        self.result =  (self.odci, self.rzed, self.num)
