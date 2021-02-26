import matplotlib as mpl
from matplotlib import colors
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os
from scripts.np_read_file import ReadFile

def plot(path):
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
    info = []

    # Read data from input file
    v = ReadFile(path)
    v.run_read_file()

    # Output filename
    pre, ext = os.path.splitext(path)
    output_path = pre + ".png"

    # Graph and font size
    # fig_size = plt.rcParams["figure.figsize"]
    # fig_size[0] = 15
    # fig_size[1] = 10
    # plt.rcParams["figure.figsize"] = fig_size
    # plt.rcParams.update({'font.size': 15})

    xtable = []
    ytable = []

    # The main part - plots
    if v.graph == "1D":
        # 1D data

        # Plot title
        plot_title = v.title
        plot_title = plot_title.replace("In positive flux relative to Out positive flux from FDTD", "Absorbance ")

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


        # Borders of the graph
        extent_data = (round(y[0], 1), round(y[-1], 1), round(xtable[0], 1), round(xtable[-1], 1))

            # Normalization
        def f(n):
            norm = mpl.colors.PowerNorm(gamma=n)
            return norm

        # plt.clf() # Clear the previous graph
        # plt.imshow(ztable, origin="lower", norm=norm, cmap='hot', extent=extent_data, interpolation='nearest',
        #            aspect='auto')
        # plt.colorbar().set_label(plot_z_label)
        # plt.xlabel(plot_x_label)
        # plt.ylabel(plot_y_label)
        # plt.title(plot_title, loc="left", pad="30")
        # plt.savefig(output_path)
        # plt.ion() # This is for non-blocking .show()
        # plt.show()

        gam = 0.7
        # plt.clf() # Clear the previous graph
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.01, bottom=0.25)
        l = plt.imshow(ztable, origin="lower", norm=f(gam), cmap='hot', extent=extent_data, interpolation='nearest', aspect='equal')
        #fig.colorbar(cm.ScalarMappable(norm=mpl.colors.PowerNorm(gamma=0.5), cmap='hot')).set_label(plot_z_label)
        plt.colorbar().set_label(plot_z_label)
        plt.xlabel(plot_x_label)
        plt.ylabel(plot_y_label)
        plt.title(plot_title, loc="left", pad="10")
        ax.margins(x=0)

        axb = plt.axes([0.15, 0.01, 0.65, 0.03])
        g = Slider(axb, "Gamma", 0.0, 1.0, valinit=gam)

        def update(val):
            gg = g.val
            l.set_norm(f(gg))
            fig.canvas.draw_idle()
        g.on_changed(update)

        # plt.savefig(output_path)
        # plt.ioff() # This is for non-blocking .show()
        # plt.show()
        # plt.close()

        plt.show()

        return output_path, success, info, g.val
#
# path = r'C:\Users\madzi\OneDrive\Pulpit\TEST\test_plot\I_xz_u.cht'
# plot(path)