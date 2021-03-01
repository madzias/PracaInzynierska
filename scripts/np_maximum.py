import os
import re
from scipy.interpolate import interp1d
from datetime import datetime
import numpy as np
from scripts.np_read_file import ReadFile


def abs_maxima(directory, minv, maxv, variable_name):

    """
    Finds maxima of the absorption spectra given in the the *.txt or .cht files.

    Input:
           All .cht and .txt files from current directory, containing sensor data from Omnisim.
           For best results (e.g. automatic determination of variable names),
           Omnisim should be run in FDTD Scanner mode, scanning for np_size, inglass, trunc etc.
    Output:
           abs-max-out file
    """
    # Maximum will be searched in range [xminint, xmaxint] with accuracy intstep
    # (by interpolating data in this range with given step, then taking the maximum)

    success = True
    info = []

    output_filename = os.path.join(str(directory), "abs-max-out")

    xminint = int(minv)
    xmaxint = int(maxv)
    intstep = 0.01
    intpoints = int((xmaxint - xminint) / intstep)
    do_linear_regression = True

    # Collect the filenames with the absorption spectra
    input_filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt") or filename.endswith(".cht"):
            input_filenames.append(os.path.join(directory, filename))

    if len(input_filenames) == 0:
        info.append("No proper files found in the directory!")
        success = False
        return "", success, info

    input_filenames.sort()

    xmax_list = []
    var_list = []
    var_name = ""
    # Get the variable name from first file, second line.
    # If variable does not exists (i.e. Omnisim was not run in Scanner mode) use the variable entered in GUI
    with open(output_filename, 'w+') as output:
        for filename in input_filenames:
            file = ReadFile(filename)
            file.run_read_file()

            var_value = ""
            if input_filenames.index(filename) == 0:
                try:
                    var_name = re.findall(r'(?<=[(]).*(?=\s+[=])', file.title)[0]
                except:
                    var_name = variable_name
                output.write("# File created on {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                output.write("# {}lambda_max [nm]\n".format(var_name.ljust(9)))
            try:
                var_value = re.findall(r'(?<=[=]\s).*(?=[)])', file.title)[0]
            except:
                var_value, ext = os.path.basename(filename).split(".")
                info.append("Warning - variable value was taken from the filename")
            try:
                var_value = float(var_value)
            except ValueError:
                do_linear_regression = False

            # Check, if the file is the sensor data file
            if file.header.find("OmniSim + CrystalWave Sensor Data") == -1 and file.header.find("SGCHART:2 // signature:verNo") == -1:
                # Skipping file
                continue

            # Check, if the dataset is the absorbance
            if file.title.find("relative") == -1 and file.title.find("absorbance") == -1:
                # Skipping file
                continue

            # Do some rescaling etc.
            if var_name == "np_size":
                # Convert to nanometers
                var_value *= 1000
            if var_name == "inglass" and var_value < 1:
                var_value *= 100

            x = []
            y = []

            # Take the variable value from input
            for m in file.measurements:
                x.append(m[0])
                y.append(m[1])

            if 'um' in file.x_unit or 'µm' in file.x_unit:
                x = [round(a * 1000, 2) for a in x]  # convert to nanometers

            # Data from Omnisim are in the reverse wavelength order, so unreversing
            x.reverse()
            y.reverse()

            # Interpolating function (it looks that cubic variant work best)
            fint = interp1d(x, y, kind='cubic', fill_value="extrapolate")

            # x values for interpolation
            xnew = np.linspace(xminint, xmaxint, num=intpoints, endpoint=True)
            # Interpolated y values
            yint = list(fint(xnew))

            # Find all of the maxima
            xmax = []
            for i in range(1, len(yint)-1):
                if yint[i-1] < yint[i] > yint[i+1]:
                    xmax.append(round(xnew[i], 2))

            # If no local maximum is found, skip the file
            if not xmax:
                # print("no max in range [{}, {}]".format(xminint, xmaxint))
                continue

            # Append result to a list
            xmax_list.append(xmax)
            var_list.append(var_value)
            output.write("{}{}\n".format(str(round(var_value, 1)).ljust(11), str(xmax)[1:-1].replace(",", " ")))

    if len(xmax_list) < 2:
        do_linear_regression = False

    do_plot = True
    for i in xmax_list:
        if len(i) > 1:
            do_plot = False
            break
    if len(xmax_list) == 0:
        info.append("There is no maximum in chosen range.")
        do_plot = False
        success = False

    plot_title = ''
    plot_x_label = ''
    plot_y_label = ''
    plot_path = ''

    if do_plot:
        if var_name in ["trunc", "inglass"]:
            plot_title = \
                "Position of the maximum of the absorption spectra \n for the truncated spheres of size 50 nm on glass"
            plot_x_label = "Sphere truncate factor (%)\n(0% - full sphere; 50% - half sphere, etc.)"
        elif var_name == "np_size":
            plot_title = \
                "Position of the maximum of the absorption spectra \n for the spheres of variable size in air"
            plot_x_label = "Sphere size (µm)"
        elif var_name == "al2o3":
            plot_title = \
                "Position of the maximum of the absorption spectra \n for the spheres covered by Al2O3 layer"
            plot_x_label = "Thickness of the Al2O3 layer (µm)"
        else:
            plot_title = "Position of the maximum of the absorption spectra"
            plot_x_label = var_name

        plot_y_label = "Wavelength (nm)"
        plot_name = "plot_" + str(var_name) + "_" + str(minv) + "_" + str(maxv) + ".png"
        plot_path = os.path.join(directory, plot_name)

    else:
        plot_info = "Different numbers of maxima in datasets, skipping plot."

    if not success:
        if os.path.exists(output_filename):
            os.remove(output_filename)
    return output_filename, success, info, plot_info, {"do_plot": do_plot, "do_linear_regression": do_linear_regression, "plot_title": plot_title, "plot_x_label": plot_x_label, "plot_y_label": plot_y_label, "var_list": var_list, "xmax_list": xmax_list, "plot_path": plot_path}
