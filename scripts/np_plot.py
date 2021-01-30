import matplotlib as mpl
import matplotlib.pyplot as plt
import os, re
from scripts.np_read_file import ReadFile

def plot(path, in_gamma):
    '''
    Plots data from the .cht file and saves it as the png file.

    Input:
           .cht file from Omnisim.
           Shortcut: np [...] gamma
    Output:
           .png graphics file with a plot.
    '''

    output_path = ""
    success = True
    info = ""

    # Read data from input file
    v = ReadFile(path)
    v.run_read_file()

    # Output filename
    pre, ext = os.path.splitext(path)
    output_path = pre + ".png"

    # Graph and font size
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 15
    fig_size[1] = 9
    plt.rcParams["figure.figsize"] = fig_size
    plt.rcParams.update({'font.size': 22})

    xtable = []
    ytable = []

    # The main part - plots
    if v.graph == "1D":
        # 1D data

        # Plot title
        plot_title = v.title
        plot_title = plot_title.replace("In positive flux relative to Out positive flux from FDTD", "Absorbance ")
        # Keep the space (hack ;) )!

        # x label
        x_unit = v.x_unit
        if v.x_unit[0] == "/":
            x_unit = "(" + v.x_unit[1:] + ")"
        x_unit = x_unit.replace("um","µm")
        plot_x_label = v.x_label + " " + x_unit
        # plot_x_label = plot_x_label.replace(" /fs"," (fs)")
        # plot_x_label = plot_x_label.replace(" /um"," (µm)")

        # y label
        y_unit = v.y_unit
        if v.y_unit[0] == "/":
            y_unit = "(" + v.y_unit[1:] + ")"
        y_unit = y_unit.replace("um","µm")
        plot_y_label = v.y_label + " " + y_unit
        # plot_y_label = plot_y_label.replace("/V/m","(V/m)")
        # plot_y_label = plot_y_label.replace("/A/m","(A/m)")
        # plot_y_label = plot_y_label.replace("/J/m","(J/m)")
        # plot_y_label = plot_y_label.replace(" /W/m"," (W/m)")
        # plot_y_label = plot_y_label.replace(" /W/um"," (W/µm)")
        # plot_y_label = plot_y_label.replace(" /W"," (W)")

        # Read data
        x = []
        y = []
        for m in v.mesurements:
            x.append(float(m[0]))
            if "Absorbance" in plot_title:
                y.append(float(m[1])*100)
            else:
                y.append(float(m[1]))

        if "Absorbance" in plot_title:
            plot_y_label = "Absorbance (%)"

        plt.plot(x, y)
        plt.title(plot_title, loc="left", pad="30")
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.savefig(output_path)
        plt.show()

    else:
        # 2D data

        # Plot title
        plot_title = v.title

        # x label
        x_unit = v.x_unit
        if v.x_unit[0] == "/":
            x_unit = "(" + v.x_unit[1:] + ")"
        x_unit = x_unit.replace("um","µm")
        plot_x_label = v.x_label + " " + x_unit

        # y label
        y_unit = v.y_unit
        if v.y_unit[0] == "/":
            y_unit = "(" + v.y_unit[1:] + ")"
        y_unit = y_unit.replace("um","µm")
        plot_y_label = v.y_label + " " + y_unit

        # z label
        z_unit = v.z_unit
        if v.z_unit[0] == "/":
            y_unit = "(" + v.z_unit[1:] + ")"
        z_unit = z_unit.replace("um","µm")
        plot_z_label = v.z_label + " " + z_unit

        y = v.mesurements[0]
        y = [float(i) for i in y]

        # Number of y-data
        ycount = len(y)

        # Number od x and z data
        xcount = len(v.mesurements) - 1

        z = []
        xtable = []
        ztable = []
        for i in range(1, xcount + 1):
            z = []
            line = v.mesurements[i]
            x = float(line[0])
            for j in range(1, ycount + 1):
                z.append(float(line[j]))
            xtable.append(x)
            ztable.append(z)

        # print(ztable[0][0])
        # print(ztable[0][-1])
        # print(ztable[-1][0])
        # print(ztable[-1][-1])

        # Borders of the graph
        extent_data = (round(y[0], 1), round(y[-1], 1), round(xtable[0], 1), round(xtable[-1], 1))
        # print(round(y[0],1), "\n", round(y[-1],1), "\n",round(xtable[0],1), "\n",round(xtable[-1],1))
        # Initial gamma for color normalization
        # if len(args) > 0:
        #     try:
        #         gamma = args[0]
        #     except:
        #         gamma = 1.0
        # else:
        #     gamma = 1.0
        # gamma = 0.5
        # while gamma != "":
        #
        #     try:
        #         gamma = float(gamma)
        #     except ValueError:
        #         gamma = 1.0
        gamma = float(in_gamma)

            # Normalization
        norm = mpl.colors.PowerNorm(gamma=gamma)

        plt.clf() # Clear the previous graph
        plt.imshow(ztable, origin="lower", norm=norm, cmap='hot', extent=extent_data, interpolation='nearest',
                   aspect='auto')
        plt.colorbar().set_label(plot_z_label)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.title(plot_title, loc="left", pad="30")
        plt.savefig(output_path)
        plt.ion() # This is for non-blocking .show()
        plt.show()

            # print("Current gamma = {}.".format(gamma))
            # gamma = input("Input new gamma [0,1] or <cr> to accept current value: ")

        return output_path, success, info

# path = r'C:\Users\madzi\OneDrive\Pulpit\TEST\test_plot\I_t_u.cht'
# plot(path)