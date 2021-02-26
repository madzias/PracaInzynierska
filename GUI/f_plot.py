from tkinter import *
from tkinter import messagebox
import os
import GUI.descriptions as desc
import GUI.components as comp

import scripts.np_plot as np_plot

class Plot_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_plot)
        files = comp.open1file(self.parent, (("TXT CHT", ".txt .cht"), ("All files", "*.*")))

        def run_np():
            start = True
            file = str(files.get())
            if not os.path.exists(file):
                messagebox.showerror("Error!", "File does not exist!")
                start = False
            if start:
                output, success, info, gamma = np_plot.plot(file)
                print("ttttttttttttttttt")
                # if success:
                #     messagebox.askyesno("Saving plot", "Do you want to save this plot?")
                # elif not success:
                #     messagebox.showerror("Error!", info)

        # def clear_input():
        #     gm.delete(0, END)
        #     gm.insert(0, 0.5)


        # Checkboxes
        # frame_options = LabelFrame(self.parent, text="Gamma", padx=10, pady=10) # pad od ramki do tego w środku
        # frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=3) # pad o ramki do brzegu okna
        # frame_options.columnconfigure(0, weight=1)
        # frame_options.rowconfigure(3, weight=1)
        #
        # g_desc = Label(frame_options, text="Enter gamma or leave existing one:")
        # g_desc.grid(row=8, column=0, sticky=W)
        # gamma = StringVar(root)
        # gm = Spinbox(frame_options, from_=0.0, to=1.0, increment=0.1, textvariable=gamma)
        # gamma.set(0.5)
        # gm.grid(row=8, column=1, sticky=W)

        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=3, column=0, sticky=W+S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=3, column=2, sticky=S, padx=5, pady=5)