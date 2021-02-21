from tkinter import *
from tkinter import messagebox
import os
import GUI.descriptions as desc
import GUI.components as comp

import scripts.np_database as np_database

class Database_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_database)
        files = comp.open2files(self.parent, (("CSV", ".csv"), ("All files", "*.*")), True)

        def run_np():
            start = True
            file1 = str(files[0].get())
            file2 = str(files[1].get())
            min = min_var.get()
            max = max_var.get()
            mat = mat_var.get()
            if not os.path.exists(file1):
                messagebox.showerror("Error!", "First file does not exist!")
                start = False
            if not os.path.exists(file2):
                messagebox.showerror("Error!", "Second file does not exist!")
                start = False
            if start:
                output = np_database.make_database(file1, file2, min, max, mat)
                messagebox.showinfo("Success!", "Output file " + str(output) + " has been created")

        def clear_input():
            min_var.set(0.25)
            max_var.set(1.45)
            mat_var.set("")


        # Checkboxes
        frame_options = LabelFrame(self.parent, text="Lambda validity range", padx=10, pady=10) # pad od ramki do tego w środku
        frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=3) # pad o ramki do brzegu okna
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(3, weight=1)

        description = Label(frame_options, text="Modify lambda validity range or leave default values", justify=LEFT)
        description.grid(row=0, column=0, columnspan=4, sticky=W)
        min_desc = Label(frame_options, text="Minimum wavelength (um):")
        min_desc.grid(row=1, column=0, sticky=W)
        min_var = StringVar(root)
        min_var.set("0.25")
        minimum = Spinbox(frame_options, from_=0, to=100, increment=0.01, textvariable=min_var)
        minimum.grid(row=1, column=1, sticky=W)
        max_desc = Label(frame_options, text="Maximum wavelength (um):")
        max_desc.grid(row=2, column=0, sticky=W)
        max_var = StringVar(root)
        max_var.set("1.45")
        maximum = Spinbox(frame_options, from_=0, to=100, increment=0.01, textvariable=max_var)
        maximum.grid(row=2, column=1, sticky=W)

        material_options = LabelFrame(self.parent, text="Material", padx=10, pady=10) # pad od ramki do tego w środku
        material_options.grid(row=3, column=0, padx=5, pady=5, sticky=E+W, columnspan=3) # pad o ramki do brzegu okna
        material_options.columnconfigure(0, weight=1)
        material_options.rowconfigure(0, weight=1)

        mat_desc = Label(material_options, text="Enter material name: ")
        mat_desc.grid(row=0, column=0, sticky=W)
        mat_var = StringVar(root)
        material = Entry(material_options, textvariable=mat_var)
        material.grid(row=0, column=2, sticky=W)

        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=4, column=0, sticky=W+S, padx=5, pady=5)

        b_clear = Button(self.parent, text="Clear", borderwidth=1, width=20,command=clear_input)
        b_clear.grid(row=4, column=1, sticky=S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=4, column=2, sticky=S, padx=5, pady=5)