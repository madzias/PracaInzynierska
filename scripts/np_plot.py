import os
from scripts.np_read_file import ReadFile


def plot(in_path):
    """
    Plots data from the .cht file and saves it as the png file.

    Input:
           .cht file from Omnisim.
           Shortcut: np [...] gamma
    Output:
           .png graphics file with a plot.
    """

    # Read data from input file
    v = ReadFile(in_path)
    v.run_read_file()

    # Output filename
    pre, ext = os.path.splitext(in_path)
    output_path = pre + ".png"

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
        x_unit = x_unit.replace("um", "µm")
        plot_x_label = v.x_label + " " + x_unit

        # y label
        y_unit = v.y_unit
        if v.y_unit[0] == "/":
            y_unit = "(" + v.y_unit[1:] + ")"
        y_unit = y_unit.replace("um", "µm")
        plot_y_label = v.y_label + " " + y_unit

        # Read data
        x = []
        y = []
        for m in v.measurements:
            x.append(float(m[0]))
            if "Absorbance" in plot_title:
                y.append(float(m[1])*100)
            else:
                y.append(float(m[1]))

        if "Absorbance" in plot_title:
            plot_y_label = "Absorbance (%)"

        # plt.plot(x, y)
        # plt.title(plot_title, loc="left", pad="30")
        # plt.xlabel(plot_x_label)
        # plt.ylabel(plot_y_label)
        # plt.savefig(output_path)
        # plt.show()
        return v.graph, {"x": x, "y": y, "plot_title": plot_title, "plot_x_label": plot_x_label, "plot_y_label": plot_y_label, "output_path": output_path}

    else:
        # 2D data

        # Plot title
        plot_title = v.title

        # x label
        x_unit = v.x_unit
        if v.x_unit[0] == "/":
            x_unit = "(" + v.x_unit[1:] + ")"
        x_unit = x_unit.replace("um", "µm")
        plot_x_label = v.x_label + " " + x_unit

        # y label
        y_unit = v.y_unit
        if v.y_unit[0] == "/":
            y_unit = "(" + v.y_unit[1:] + ")"
        y_unit = y_unit.replace("um", "µm")
        plot_y_label = v.y_label + " " + y_unit

        # z label
        z_unit = v.z_unit
        if v.z_unit[0] == "/":
            z_unit = "(" + v.z_unit[1:] + ")"
        z_unit = z_unit.replace("um", "µm")
        plot_z_label = v.z_label + " " + z_unit

        y = v.measurements[0]
        y = [float(i) for i in y]

        # Number of y-data
        ycount = len(y)

        # Number od x and z data
        xcount = len(v.measurements) - 1

        xtable = []
        ztable = []
        for i in range(1, xcount + 1):
            z = []
            line = v.measurements[i]
            x = float(line[0])
            for j in range(1, ycount + 1):
                z.append(float(line[j]))
            xtable.append(x)
            ztable.append(z)

        return v.graph, {"xtable": xtable, "ytable": y, "ztable": ztable, "plot_title": plot_title, "plot_x_label": plot_x_label, "plot_y_label": plot_y_label, "plot_z_label": plot_z_label, "output_path": output_path}
