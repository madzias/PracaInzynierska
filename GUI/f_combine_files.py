from tkinter import *
from tkinter import messagebox
import os
import GUI.descriptions as desc
import GUI.components as comp

import scripts.np_combine_files as np_combine

class Combine_tab(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        comp.about(self.parent, desc.about_combine)
        files = comp.open2files(self.parent, (("TXT CHT", ".txt .cht"), ("All files", "*.*")))

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
            if not os.path.exists(file2):
                messagebox.showerror("Error!", "Second file does not exist!")
                start = False
            if file1 == file2:
                messagebox.showerror("Error!", "Selected files are the same!")
                start = False
            if start == True:
                r = np_combine.CombineFiles(file1, file2)
            if s_var.get() == 1 and start == True:
                output, success, info = r.subtructing()
                if success:
                    final_s_output.append("Subtruction result saved as " + output)
                else:
                    final_e_output.append(info)
                    start = False
            if u_var.get() == 1 and start == True:
                output, success, info = r.unpolarize()
                if success:
                    final_s_output.append("Unpolarization result saved as " + output)
                else:
                    final_e_output.append(info)
                    start = False

            if a_var.get() == 1 and start == True:
                output, success, info = r.absorbance()
                if success:
                    final_s_output.append("Absorbance calucaltion saved as " + output)
                else:
                    final_e_output.append(info)
                    start = False

            if t_var.get() == 1 and start == True:
                output, success, info = r.transmitance()
                if success:
                    final_s_output.append("Transmitance calucaltion saved as " + output)
                else:
                    final_e_output.append(info)
                    start = False

            msg = ""
            if start == False:
                for i in final_e_output:
                    msg = msg + i + "\n"
                messagebox.showerror("Error!", msg)
            else:
                for i in final_s_output:
                    msg = msg + i + "\n"
                messagebox.showinfo("Success!", msg)

        # Checkboxes
        frame_options = LabelFrame(self.parent, text="Choose options", padx=10, pady=10) # pad od ramki do tego w środku
        frame_options.grid(row=2, column=0, padx=5, pady=5, sticky=E+W, columnspan=3) # pad o ramki do brzegu okna
        frame_options.columnconfigure(0, weight=1)
        frame_options.rowconfigure(0, weight=1)

        s_var = IntVar()
        s = Checkbutton(frame_options, text="Subtruct", variable=s_var, onvalue=1, offvalue=0)
        s.grid(row=0, column=0, sticky=W)

        u_var = IntVar()
        u = Checkbutton(frame_options, text="Unpolarize", variable=u_var, onvalue=1, offvalue=0)
        u.grid(row=1, column=0, sticky=W)

        a_var = IntVar()
        a = Checkbutton(frame_options, text="Calculate absorbance", variable=a_var, onvalue=1, offvalue=0)
        a.grid(row=0, column=1, sticky=W)

        t_var = IntVar()
        t = Checkbutton(frame_options, text="Calculate transmitance", variable=t_var, onvalue=1, offvalue=0)
        t.grid(row=1, column=1, sticky=W)


        # Buttons
        b_close = Button(self.parent, text="Close", borderwidth=1, width=20, command=root.destroy)
        b_close.grid(row=3, column=0, sticky=W+S, padx=5, pady=5)

        b_run = Button(self.parent, text="Run", borderwidth=1, width=20, command=run_np)
        b_run.grid(row=3, column=2, sticky=S, padx=5, pady=5)