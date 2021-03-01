from tkinter import *
from tkinter import messagebox
import os
import numpy as np
import GUI.descriptions as desc
import GUI.components as comp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import scripts.np_maximum as np_max


class MaximumTab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.fig = Figure(figsize=(6, 6))
        comp.about(self.parent, desc.about_max)
        dirs = comp.opendir(self.parent)

        # New window for plot
        def plot_window(data):
            new_window = Toplevel(self.parent)
            new_window.title("OSA - OmniSim Analizer | Plot")
            new_window.geometry("600x645")
            new_window.iconbitmap(r'..\wasp.ico')
            new_window.columnconfigure(0, weight=1)

            var_list = data["var_list"]
            xmax_list = data["xmax_list"]

            c = self.fig.add_subplot()
            c.plot(data["var_list"], data["xmax_list"], ".")
            if data["do_linear_regression"]:
                # Linear regression
                a, b = np.polyfit(var_list, xmax_list, 1)
                xmax_reg = [a*i+b for i in var_list]
                c.plot(var_list, xmax_reg)
            c.set_title(data["plot_title"])
            c.set_ylabel(data["plot_y_label"])
            c.set_xlabel(data["plot_x_label"])

            canvas = FigureCanvasTkAgg(self.fig, master=new_window)
            canvas.get_tk_widget().grid(row=0, column=0)
            canvas.draw()

            def save_plot():
                self.fig.savefig(data["plot_path"])
                messagebox.showinfo("Success!", "Plot has been saved as " + str(data["plot_path"]))

            b_save = Button(new_window, text="Save plot", borderwidth=1, width=20, command=save_plot)
            b_save.grid(row=4, column=0, sticky=W+S, padx=5, pady=5)

        def run_np():
            start = True
            dir1 = str(dirs.get())
            min_v = min_var.get()
            max_v = max_var.get()
            lb_v = lb_var.get()
            success = False
            info = []
            output = ""
            if not os.path.exists(dir1):
                messagebox.showerror("Error!", "Directory does not exist!")
                start = False
            if float(min_v) > float(max_v):
                messagebox.showerror("Error!", "Minimum has to be smaller than maximum!")
                start = False
            if start:
                output, success, info, plot_info, plot_data = np_max.abs_maxima(dir1, min_v, max_v, lb_v)
                if success:
                    messagebox.showinfo("Success!", "Output file " + str(output) + " has been created")
                    if plot_data["do_plot"]:
                        plot_window(plot_data)
                    else:
                        messagebox.showinfo("Information", plot_info)
                else:
                    for i in info:
                        messagebox.showerror("Error!", i)

        def clear_input():
            minimum.delete(0, END)
            minimum.insert(0, "301")
            maximum.delete(0, END)
            maximum.insert(0, "699")
            lb_var.set("")

        # Settings
        frame_options = LabelFrame(self.parent, text="Choose options", padx=10, pady=10)
        frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=3)
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(0, weight=1)

        description = Label(frame_options, text="Program looks for maximum in the [min, max] range. "
                                                "\nModify below settings or leave the default values.", justify=LEFT)
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

        frame_options = LabelFrame(self.parent, text="Label", padx=10, pady=10)
        frame_options.grid(row=3, column=0, padx=5, pady=5, sticky=E+W, columnspan=3)
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(0, weight=1)

        description = Label(frame_options, text="Program will get variable name from the first file. "
                                                "\nYou can enter variable name in case program won't find it.", justify=LEFT)
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
