from tkinter import *
from tkinter import ttk

from GUI.f_plane import *
from GUI.f_truncate import *
from GUI.f_change_type import *
from GUI.f_combine_files import *
from GUI.f_maximum import *
from GUI.f_plot import *

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, height=42, width=42)
        my_notebook = ttk.Notebook(parent)
        my_notebook.grid(row=0, column=0, sticky=W+E)
        my_notebook.rowconfigure(0, weight=1)
        my_notebook.columnconfigure(1, weight=1)

        #fr_database = Frame(my_notebook, width=600, height=600)
        fr_plane = Frame(my_notebook)
        fr_truncate = Frame(my_notebook)
        fr_convert = Frame(my_notebook)
        fr_combine = Frame(my_notebook)
        fr_max = Frame(my_notebook)
        fr_plot = Frame(my_notebook)

        # #fr_database.pack(fill="both", expand=1)
        fr_plane.grid(row=1, column=0, columnspan=3)
        fr_plane.rowconfigure(0, weight=0)
        fr_plane.columnconfigure(0, weight=1)

        fr_truncate.grid(row=1, column=0, columnspan=3)
        fr_truncate.rowconfigure(0, weight=0)
        fr_truncate.columnconfigure(0, weight=1)

        fr_convert.grid(row=1, column=0, columnspan=3)
        fr_convert.rowconfigure(0, weight=0)
        fr_convert.columnconfigure(0, weight=1)

        fr_combine.grid(row=1, column=0, columnspan=3)
        fr_combine.rowconfigure(0, weight=0)
        fr_combine.columnconfigure(0, weight=1)

        fr_max.grid(row=1, column=0, columnspan=3)
        fr_max.rowconfigure(0, weight=0)
        fr_max.columnconfigure(0, weight=1)

        fr_plot.grid(row=1, column=0, columnspan=3)
        fr_plot.rowconfigure(0, weight=0)
        fr_plot.columnconfigure(0, weight=1)

        #my_notebook.add(fr_database, text="Database")
        my_notebook.add(fr_plane, text="Plane")
        my_notebook.add(fr_truncate, text="Truncate")
        my_notebook.add(fr_convert, text="Convert")
        my_notebook.add(fr_combine, text="Combine files")
        my_notebook.add(fr_max, text="Maximum")
        my_notebook.add(fr_plot, text="Plot")

        my_notebook.grid(row=0, column=0)
        my_notebook.rowconfigure(1, weight=1)
        my_notebook.columnconfigure(1, weight=1)

        Plane_tab(fr_plane, parent)
        Truncate_tab(fr_truncate, parent)
        Convert_tab(fr_convert, parent)
        Combine_tab(fr_combine, parent)
        Maximum_tab(fr_max, parent)
        Plot_tab(fr_plot, parent)

if __name__ == "__main__":
    root = Tk()
    root.title("OSA - OmniSim Analizer")
    root.iconbitmap(r'..\wasp.ico')
    root.geometry("600x620")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    MainApplication(root).grid()
    root.mainloop()


