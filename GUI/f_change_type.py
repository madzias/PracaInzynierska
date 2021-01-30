from tkinter import *
from tkinter import messagebox
import os
import GUI.descriptions as desc
import GUI.components as comp
import scripts.np_change_type as np_ct

class Convert_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_convert)
        path = comp.open1file(self.parent, (("TXT", "*.txt"), ("CHT", "*.cht")))

        def run_np():
            start = True
            file = str(path.get())
            if not os.path.exists(file):
                messagebox.showerror("Error!", "File does not exist!")
                start = False
            if start:
                output, success, info = np_ct.change_type(file)
                if not success:
                    messagebox.showerror("Error!", info)
                else:
                    messagebox.showinfo("Success!", "Output file " + str(output) + " has been created")

        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=2, column=0, sticky=W+S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=2, column=2, sticky=S, padx=5, pady=5)