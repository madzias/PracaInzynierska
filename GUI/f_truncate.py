from tkinter import *
from tkinter import messagebox
import os
import GUI.descriptions as desc
import GUI.components as comp

import scripts.np_truncate_flatten as np_truncate


class TruncateTab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_truncate)
        files = comp.open1file(self.parent, (("PY", "*.py"), ("All files", "*.*")))

        def run_np():
            start = True
            file = str(files.get())
            trun = int(truncate.get())
            strun = int(sigma_truncate.get())
            flat = int(flatten.get())
            sflat = int(sigma_flatten.get())
            if new_device.get() != "":
                ndev = int(new_device.get())
            else:
                ndev = str(new_device.get())
            if not os.path.exists(file):
                messagebox.showerror("Error!", "File does not exist!")
                start = False
            if not 0 <= trun <= 100:
                messagebox.showerror("Error!", "The percent where the spheres will be cut must be between 0 and 100%")
                start = False
            if not strun >= 0:
                messagebox.showerror("Error!", "The standard deviation for sphere cut must be positive")
                start = False
            if not 0 <= flat <= 100:
                messagebox.showerror("Error!", "The percent of the nominal y-size of the spheres must be between 0 and 100%")
                start = False
            if not sflat >= 0:
                messagebox.showerror("Error!", "The standard deviation for sphere flatten must be positive")
                start = False
            if start:
                output, success, info = np_truncate.truncate_flatten(file, trun, strun, flat, sflat, ndev)
                if not success:
                    messagebox.showerror("Error!", info)
                else:
                    messagebox.showinfo("Success!", "Output file " + str(output) + " has been created")

        def clear_input():
            truncate.delete(0, END)
            truncate.insert(0, 0)
            sigma_truncate.delete(0, END)
            sigma_truncate.insert(0, 0)
            flatten.delete(0, END)
            flatten.insert(0, 0)
            sigma_flatten.delete(0, END)
            sigma_flatten.insert(0, 0)
            new_device.delete(0, END)
            new_device.insert(0, "")

        # Checkboxes
        frame_options = LabelFrame(self.parent, text="Settings", padx=10, pady=10)
        frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=3)
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(3, weight=1)

        t_desc = Label(frame_options, text="Spheres could be cut (truncated). 100% - full sphere, 50% - hemisphere, etc.")
        t_desc.grid(row=0, column=0, columnspan=2)
        tt_desc = Label(frame_options, text="Enter the percent where the spheres will be cut [0-100%]:")
        tt_desc.grid(row=1, column=0, sticky=W)
        truncate = Spinbox(frame_options, from_=0, to=100)
        truncate.grid(row=1, column=1, sticky=W)
        st_desc = Label(frame_options, text="Enter the standard deviation for sphere cut, or 0:")
        st_desc.grid(row=2, column=0, sticky=W)
        sigma_truncate = Spinbox(frame_options, from_=0, to=100)
        sigma_truncate.grid(row=2, column=1, sticky=W)

        f_desc = Label(frame_options, text="Spheres could be flattened. Y-size = 100% - full size, 50% - flatten by a half, etc.")
        f_desc.grid(row=4, column=0, columnspan=2)
        ff_desc = Label(frame_options, text="Enter the percent of the nominal y-size of the spheres [0-100%]:")
        ff_desc.grid(row=5, column=0, sticky=W)
        flatten = Spinbox(frame_options, from_=0, to=100)
        flatten.grid(row=5, column=1, sticky=W)
        sf_desc = Label(frame_options, text="Enter the standard deviation for sphere flatten, or 0:")
        sf_desc.grid(row=6, column=0, sticky=W)
        sigma_flatten = Spinbox(frame_options, from_=0, to=100)
        sigma_flatten.grid(row=6, column=1, sticky=W)
        space = Label(frame_options, text=" ")
        space.grid(row=7, column=0, sticky=W)
        nd_desc = Label(frame_options, text="Enter device number or leave empty to keep existing one:")
        nd_desc.grid(row=8, column=0, sticky=W)
        nd = StringVar(root)
        new_device = Spinbox(frame_options, from_=0, to=100, textvariable=nd)
        nd.set("")
        new_device.grid(row=8, column=1, sticky=W)

        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=3, column=0, sticky=W+S, padx=5, pady=5)

        b_clear = Button(self.parent, text="Clear", borderwidth=1, width=20, command=clear_input)
        b_clear.grid(row=3, column=1, sticky=S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=3, column=2, sticky=S, padx=5, pady=5)
