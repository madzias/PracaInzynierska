from tkinter import *
from tkinter import messagebox
import os
import GUI.descriptions as desc
import GUI.components as comp

import scripts.np_combine_files as np_combine

class Maximum_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_max)
        files = comp.opendir(self.parent)

        def run_np():
            start = True
            file1 = str(files[0].get())
            file2 = str(files[1].get())
            final_s_output = []
            final_e_output = []
            success = False
            info = ""
            output = ""
            if not os.path.exists(file1):
                messagebox.showerror("Error!", "First file does not exist!")
                start = False

        def clear_input():
            minimum.delete(0, END)
            minimum.insert(0, "301")
            maximum.delete(0, END)
            maximum.insert(0, "699")
            lb_var.set("")

        # Checkboxes
        frame_options = LabelFrame(self.parent, text="Choose options", padx=10, pady=10) # pad od ramki do tego w środku
        frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=3) # pad o ramki do brzegu okna
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(0, weight=1)

        description = Label(frame_options, text="Program looks for maximum in the [min, max] range. \nModify below settings or leave the default values.", justify=LEFT)
        description.grid(row=0, column=0, columnspan=4, sticky=W)
        min_desc = Label(frame_options, text="Minimum: ")
        min_desc.grid(row=1, column=0, sticky=W)
        min_var = StringVar(root)
        min_var.set("301")
        minimum = Spinbox(frame_options, from_=0, to=10000, textvariable=min_var)
        minimum.grid(row=1, column=1, sticky=W)
        max_desc = Label(frame_options, text="Maximum:")
        max_desc.grid(row=2, column=0, sticky=W)
        max_var = StringVar(root)
        max_var.set("699")
        maximum = Spinbox(frame_options, from_=0, to=10000, textvariable=max_var)
        maximum.grid(row=2, column=1, sticky=W)

        frame_options = LabelFrame(self.parent, text="Label", padx=10, pady=10) # pad od ramki do tego w środku
        frame_options.grid(row=3, column=0, padx=5, pady=5, sticky=E+W, columnspan=3) # pad o ramki do brzegu okna
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(0, weight=1)

        description = Label(frame_options, text="Program will get variable name from the first file. \nYou can enter variable name in case program won't find it.", justify=LEFT)
        description.grid(row=0, column=0, columnspan=4, sticky=W)
        lb_desc = Label(frame_options, text="Variable name: ")
        lb_desc.grid(row=1, column=0, sticky=W)
        lb_var = StringVar(root)
        lb_var.set("")
        label = Entry(frame_options, textvariable=lb_var)
        label.grid(row=1, column=1, sticky=W)

        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=4, column=0, sticky=W+S, padx=5, pady=5)

        b_clear = Button(self.parent, text="Clear", borderwidth=1, width=20, command=clear_input)
        b_clear.grid(row=4, column=1, sticky=S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=4, column=2, sticky=S, padx=5, pady=5)