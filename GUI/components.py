from tkinter import *
from tkinter import filedialog
from pathlib import Path


# Display 'about' in GUI
def about(tab, description):
    frame_about = LabelFrame(tab, text="About", padx=10, pady=10)
    frame_about.grid(row=0, column=0, padx=5, pady=5, sticky=E+W+N, columnspan=3)
    frame_about.columnconfigure(0, weight=1)
    frame_about.rowconfigure(0, weight=1)

    msg1 = Label(frame_about, text=description, borderwidth=1, justify=LEFT, wraplength=560)
    msg1.grid(row=0, column=0, sticky=W)
    msg1.columnconfigure(0, weight=1)
    msg1.rowconfigure(0, weight=1)


# Open 1 file
def open1file(tab, file_type):
    frame_files = LabelFrame(tab, text="Select file", padx=10, pady=10)
    frame_files.grid(row=1, column=0, padx=5, pady=5, sticky=N+W+E, columnspan=3)
    frame_files.columnconfigure(0, weight=1)
    frame_files.rowconfigure(1, weight=1)

    path_1 = Entry(frame_files, borderwidth=1)
    path_1.grid(row=0, column=0, sticky=W+E)
    path_1.columnconfigure(0, weight=1)
    path_1.rowconfigure(0, weight=1)

    p1 = StringVar()

    def browsefunc():
        filename = filedialog.askopenfilename(initialdir=str(Path.home()), title="Select a file", filetypes=file_type)
        path_1.delete(0, END)
        path_1.insert(END, filename)
        p1.set(filename)

    b1 = Button(frame_files, text="Open", command=lambda: browsefunc(), borderwidth=1)
    b1.grid(row=0, column=2)
    return p1


# Open 2 files
def open2files(tab, file_type, *csv):
    frame_files = LabelFrame(tab, text="Select files", padx=10, pady=10)
    frame_files.grid(row=1, column=0, padx=5, pady=5, sticky=N+W+E, columnspan=3)
    frame_files.columnconfigure(0, weight=1)
    frame_files.rowconfigure(1, weight=1)

    p1 = StringVar()

    def browsefunc1():
        filename = filedialog.askopenfilename(initialdir=str(Path.home()), title="Select a file", filetypes=file_type)
        path_1.delete(0, END)
        path_1.insert(END, filename)
        p1.set(filename)

    if csv:
        path1_label = Label(frame_files, text="Select CSV file containing the Re(n): ", padx=10, pady=5)
        path1_label.grid(row=0, column=0, sticky=W)
        path1_label.columnconfigure(0, weight=1)
        path1_label.rowconfigure(0, weight=1)

    path_1 = Entry(frame_files, borderwidth=1)
    path_1.grid(row=1, column=0, sticky=W+E)
    path_1.columnconfigure(0, weight=1)
    path_1.rowconfigure(0, weight=1)

    b1 = Button(frame_files, text="Open", command=lambda: browsefunc1(), borderwidth=1)
    b1.grid(row=1, column=2)

    p2 = StringVar()

    def browsefunc2():
        filename = filedialog.askopenfilename(initialdir=str(Path.home()), title="Select a file", filetypes=file_type)
        path_2.delete(0, END)
        path_2.insert(END, filename)
        p2.set(filename)

    if csv:
        path2_label = Label(frame_files, text="Select CSV file containing the Im(n): ", padx=10, pady=5)
        path2_label.grid(row=2, column=0, sticky=W)
        path2_label.columnconfigure(0, weight=1)
        path2_label.rowconfigure(0, weight=1)

    path_2 = Entry(frame_files, borderwidth=1)
    path_2.grid(row=3, column=0, sticky=W+E)
    path_2.columnconfigure(0, weight=1)
    path_2.rowconfigure(0, weight=1)

    b2 = Button(frame_files, text="Open", command=lambda: browsefunc2(), borderwidth=1)
    b2.grid(row=3, column=2)

    return [p1, p2]


# Open directory
def opendir(tab):
    frame_files = LabelFrame(tab, text="Select directory", padx=10, pady=10)
    frame_files.grid(row=1, column=0, padx=5, pady=5, sticky=N+W+E, columnspan=3)
    frame_files.columnconfigure(0, weight=1)
    frame_files.rowconfigure(1, weight=1)

    path_1 = Entry(frame_files, borderwidth=1)
    path_1.grid(row=0, column=0, sticky=W+E)
    path_1.columnconfigure(0, weight=1)
    path_1.rowconfigure(0, weight=1)

    p1 = StringVar()

    def browsefunc():
        filename = filedialog.askdirectory(initialdir=str(Path.home()), title="Select a folder")
        path_1.delete(0, END)
        path_1.insert(END, filename)
        p1.set(filename)

    b1 = Button(frame_files, text="Open", command=lambda: browsefunc(), borderwidth=1)
    b1.grid(row=0, column=2)
    return p1
