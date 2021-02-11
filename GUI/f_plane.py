from tkinter import *
from tkinter import messagebox
import GUI.descriptions as desc
import GUI.components as comp
from scripts.np_change_plane import *

class Plane_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_plane)
        file = comp.open1file(self.parent, (("PY", "*.py"), ("All files", "*.*")))

        def run_np():
            start = True
            file1 = str(file.get())
            proj = project_var.get()
            devi = device_var.get()
            laye = layer_var.get()
            base = baseline_var.get()
            orie = orientation_var.get()
            reve = reverse_var.get()
            maxi = maximum_var.get()
            success = False
            info = ""
            output = ""
            if not os.path.exists(file1):
                messagebox.showerror("Error!", "First file does not exist!")
                start = False
            if start:
                output, success, info = change_plane(file1, proj, devi, laye, base, orie, reve, maxi)
                if success:
                    messagebox.showinfo("Success!", "Output file " + str(output) + " has been created")
                else:
                    messagebox.showerror("Error!", info)


        def clear_input():
            project_var.set("1")
            device_var.set("2")
            layer_var.set("1")
            baseline_var.set("0.5")
            orientation_var.set("True")
            reverse_var.set("False")
            maximum_var.set("1.285")

        # Settings
        frame_options = LabelFrame(self.parent, text="Settings: ", padx=10, pady=10) # pad od ramki do tego w środku
        frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=5) # pad o ramki do brzegu okna
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(3, weight=1)

        frame_options.grid_columnconfigure(4, minsize=140)
        descr = Label(frame_options, text="Change settings or leave default values")
        descr.grid(row=0, column=1, columnspan=2)

        project_desc = Label(frame_options, text="Project number")
        project_desc.grid(row=1, column=1, sticky=W)
        project_var = StringVar(root)
        project_var.set("1")
        project = Spinbox(frame_options, from_=0, to=100, textvariable=project_var)
        project.grid(row=1, column=2, sticky=W)

        device_desc = Label(frame_options, text="Device number")
        device_desc.grid(row=2, column=1, sticky=W)
        device_var = StringVar(root)
        device_var.set("2")
        device = Spinbox(frame_options, from_=0, to=100, textvariable=device_var)
        device.grid(row=2, column=2, sticky=W)

        layer_desc = Label(frame_options, text="NP layer index")
        layer_desc.grid(row=3, column=1, sticky=W)
        layer_var = StringVar(root)
        layer_var.set("1")
        layer = Spinbox(frame_options, from_=0, to=100, textvariable=layer_var)
        layer.grid(row=3, column=2, sticky=W)

        baseline_desc = Label(frame_options, text="NP baseline")
        baseline_desc.grid(row=4, column=1, sticky=W)
        baseline_var = StringVar(root)
        baseline_var.set("0.5")
        baseline = Spinbox(frame_options, from_=0, to=100, increment=0.1, textvariable=baseline_var)
        baseline.grid(row=4, column=2, sticky=W)

        orientation_desc = Label(frame_options, text="Set orientation ZX")
        orientation_desc.grid(row=5, column=1, sticky=W)
        orientation_var = StringVar(root)
        orientation_var.set("True")
        orientation = Spinbox(frame_options, values=("True", "False"), wrap=True, textvariable=orientation_var)
        orientation.grid(row=5, column=2, sticky=W)

        reverse_desc = Label(frame_options, text="Reversing x values")
        reverse_desc.grid(row=6, column=1, sticky=W)
        reverse_var = StringVar(root)
        reverse_var.set("False")
        reverse = Spinbox(frame_options, values=("False", "True"), wrap=True, textvariable=reverse_var)
        reverse.grid(row=6, column=2, sticky=W)


        maximum_desc = Label(frame_options, text="Maximum x value for reversing")
        maximum_desc.grid(row=7, column=1, sticky=W)
        maximum_var = StringVar(root)
        maximum_var.set("1.285")
        maximum = Spinbox(frame_options, from_=0, to=100, increment=0.001, textvariable=maximum_var)
        maximum.grid(row=7, column=2, sticky=W)

        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=3, column=0, sticky=W+S, padx=5, pady=5)

        b_clear = Button(self.parent, text="Clear", borderwidth=1, width=20, command=clear_input)
        b_clear.grid(row=3, column=1, sticky=S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=3, column=2, sticky=S, padx=5, pady=5)