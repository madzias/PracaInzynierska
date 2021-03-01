from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import matplotlib as mpl
from matplotlib import colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import GUI.descriptions as desc
import GUI.components as comp

import scripts.np_plot as np_plot


class PlotTab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.gamma = StringVar()
        self.fig = Figure()
        comp.about(self.parent, desc.about_plot)
        files = comp.open1file(self.parent, (("TXT CHT", ".txt .cht"), ("All files", "*.*")))

        # New window for plot
        def plot_window(plt_type, data):
            new_window = Toplevel(self.parent)
            new_window.title("OSA - OmniSim Analizer | Plot")
            new_window.geometry("600x600")
            new_window.iconbitmap(r'..\wasp.ico')
            new_window.columnconfigure(0, weight=1)

            def draw_plot():
                gamma = float(self.gamma.get())
                b = self.fig.add_subplot()
                norm = mpl.colors.PowerNorm(gamma=gamma)
                xtable = data["xtable"]
                ytable = data["ytable"]
                ztable = data["ztable"]
                extent_data = (round(ytable[0], 1), round(ytable[-1], 1), round(xtable[0], 1), round(xtable[-1], 1))
                img = b.imshow(ztable, origin="lower", norm=norm, cmap='hot', extent=extent_data, interpolation='nearest', aspect='equal')
                b.set_title(data["plot_title"])
                b.set_ylabel(data["plot_y_label"])
                a.set_xlabel(data["plot_x_label"])
                self.fig.colorbar(img).set_label(data["plot_z_label"])

                canvas = FigureCanvasTkAgg(self.fig, master=new_window)
                canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)
                canvas.draw()

            if plt_type == "1D":
                a = self.fig.add_subplot()
                a.plot(data["x"], data["y"])
                a.set_title(data["plot_title"])
                a.set_ylabel(data["plot_y_label"])
                a.set_xlabel(data["plot_x_label"])

                canvas1d = FigureCanvasTkAgg(self.fig, master=new_window)
                canvas1d.get_tk_widget().grid(row=0, column=0)
                canvas1d.draw()

            else:
                self.gamma.set('0.50')
                g_label = Label(new_window, text="Set gamma:")
                g_label.grid(row=0, column=0)
                slider = ttk.Scale(new_window, from_=0.01, to=1, orient=HORIZONTAL, command=lambda g: self.gamma.set('%0.2f' % float(g)), length=300)
                slider.grid(row=1, column=0, padx=5, pady=5)
                slider.set('0.5')
                ttk.Label(new_window, textvariable=self.gamma).grid(row=1, column=1, padx=20)
                b_refresh = Button(new_window, text="Refresh", borderwidth=1, width=20, command=draw_plot)
                b_refresh.grid(row=1, column=2, sticky=E, padx=5, pady=5)
                draw_plot()

            def save_plot():
                self.fig.savefig(data["output_path"])
                messagebox.showinfo("Success!", "Plot has been saved as " + str(data["output_path"]))

            # Buttons and slider
            b_save = Button(new_window, text="Save plot", borderwidth=1, width=20, command=save_plot)
            b_save.grid(row=4, column=0, sticky=W+S, padx=5, pady=5)

        def run_np():
            start = True
            file = str(files.get())
            if not os.path.exists(file):
                messagebox.showerror("Error!", "File does not exist!")
                start = False
            if start:
                plt_type, plot_data = np_plot.plot(file)
                plot_window(plt_type, plot_data)

        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=3, column=0, sticky=W+S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=3, column=2, sticky=S, padx=5, pady=5)
