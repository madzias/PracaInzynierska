from tkinter import *
import GUI.descriptions as desc
import GUI.components as comp
from scripts.np_change_plane import *

class Plane_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_plane)
        path = comp.open1file(self.parent, (("PY", "*.py"), ("All files", "*.*")))

        def run_np():
            print("ok" + path)
            #change_plane(path)

        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=2, column=0, sticky=W+S, padx=5, pady=5)

        b_clear = Button(self.parent, text="Clear", borderwidth=1, width=20)
        b_clear.grid(row=2, column=1, sticky=S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=2, column=2, sticky=S, padx=5, pady=5)