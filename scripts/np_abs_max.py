import os, sys, math, re
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from scripts.np_read_file import ReadFile


directory = r"C:\Users\madzi\OneDrive\Pulpit\TEST\test_abs_max"


def abs_maxima(directory, min, max, variable_name):

    '''
    Finds maxima of the absorption spectra given in the the *.txt or .cht files.

    Input:
           All .cht and .txt files from current directory, containing sensor data from Omnisim.
           For best results (e.g. automatic determination of variable names),
           Omnisim should be run in FDTD Scanner mode, scanning for np_size, inglass, trunc etc.
    Output:
           abs-max-out file
    '''
    # Maximum will be searched in range [xminint, xmaxint] with accuracy intstep
    # (by interpolating data in this range with given step, then taking the maximum)

    success = True
    info = []

    plot_partial = False
    plot_final = True
    do_linear_regression = True
    output_filename = os.path.join(str(directory), "abs-max-out")

    xminint = int(min)
    xmaxint = int(max)
    intstep = 0.01
    intpoints = int((xmaxint - xminint) / intstep)
    do_linear_regression = True
    output = os.path.join(directory, "")

    # Experimental maxima {size [nm] : maximum [nm]}
    # http://www.cytodiagnostics.com/store/pc/Gold-Nanoparticle-Properties-d2.htm
    experimental_maxima = {5:515, 10:517, 15:525, 20:524, 30:526, 40:530, 50:535, \
                           60:540, 70:548, 80:553, 90:564, 100:572}

    ### Check input files

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

    # Get the variable name from first file, second line.
    # If variable does not exists (i.e. Omnisim was not run in Scanner mode),
    # ask for a variable name
    with open(output_filename, 'w+') as output:
        for filename in input_filenames:
            file = ReadFile(filename)
            file.run_read_file()

            var_name = ""
            var_value = ""
            if input_filenames.index(filename) == 0:
                try:
                    var_name = re.findall(r'(?<=\().*(?=\s+\=)', file.title)[0]
                except:
                    var_name = variable_name
            try:
                var_value = re.findall(r'(?<=\=\s).*(?=\))', file.title)[0]
            except:
                var_value, ext = os.path.basename(filename).split(".")
                info.append = "Warning - variable value was taken from the filename"
            try:
                var_value = float(var_value)
            except ValueError:
                # Skip plots and regression, since there are no numeric var_values
                plot_partial = False
                plot_final = False
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
                # Convert from [%/100] to [%], if necessary
                #(some older results were given in [%/100])
                var_value *= 100

            x = []
            y = []

            # Take the variable value from input
            for m in file.mesurements:
                x.append(m[0])
                y.append(m[1])

            if 'um' in file.x_unit or 'µm' in file.x_unit:
                x = [round(a * 1000, 2) for a in x] #convert to nanometers

            # Data from Omnisim are in the reverse wavelength order, so unreversing
            x.reverse()
            y.reverse()

            # Interpolating function (it looks that cubic variant work best)
            fint = interp1d(x, y, kind='cubic', fill_value="extrapolate")

            # x values for interpolation
            xnew = np.linspace(xminint, xmaxint, num=intpoints, endpoint=True)
            # Interpolated y values
            yint = list(fint(xnew))

            ### Find all of the maxima
            xmax = []
            for i in range(1, len(yint)-1):
                if yint[i-1] < yint[i] > yint[i+1]:
                    xmax.append(round(xnew[i], 2))

            # If no local maximum is found, skip the file
            if not xmax:
                print("no max in range [{}, {}]".format(xminint, xmaxint))
                continue

            #print("max = ", xmax)

            # Append result to a list
            xmax_list.append(xmax)
            var_list.append(var_value)
            var_name = ""
            print(var_value)
            print(xmax)
            print("{}    {}\n".format(var_value,str(xmax)[1:-1].replace(","," ")))
            #output.readlines(var_value.ljust())

        # if plot_partial:
        #     plt.plot(xnew, fint(xnew))
        #     plt.plot(xmax, ymax, "x")
        #     if var_name == "np_size" and experimental_maxima.has_key(var_value):
        #         # If the experimental value exists for specific np_size, find it and plot
        #         xmax_exp = experimental_maxima[var_value]
        #         plt.plot(xmax_exp,ymax,"x")
        #         plt.text("{}{}  Difference: {} (nm)".format(xmax_exp,ymax,abs(xmax_exp-xmax)))
        #     plt.title("Absorption spectra, {} = {}".format(var_name, var_value))
        #     plt.xlabel("Wavelength (nm)")
        #     plt.ylabel("Absorbance (a.u.)")
        #     plt.show()


    #
    # if len(xmax_list) < 2:
    #     do_linear_regression = False
    #
    # if xmax_list:
    #     try:
    #         plt.plot(var_list, xmax_list, ".")
    #         if do_linear_regression:
    #             # Linear regression
    #             a, b = np.polyfit(var_list, xmax_list, 1)
    #             xmax_reg = [a*i+b for i in var_list]
    #             plt.plot(var_list, xmax_reg)
    #
    #         if var_name in ["trunc", "inglass"]:
    #             plot_title = \
    #                 "Position of the maximum of the absorption spectra \n for the truncated spheres of size 50 nm on glass"
    #             plot_xlabel = "Sphere truncate factor (%)\n(0% - full sphere; 50% - half sphere, etc.)"
    #         elif var_name == "np_size":
    #             plot_title = \
    #                 "Position of the maximum of the absorption spectra \n for the spheres of variable size in air"
    #             plot_xlabel = "Sphere size (µm)"
    #         elif var_name == "al2o3":
    #             plot_title = \
    #                 "Position of the maximum of the absorption spectra \n for the spheres covered by Al2O3 layer"
    #             plot_xlabel = "Thickness of the Al2O3 layer (µm)"
    #         else:
    #             plot_title = "Position of the maximum of the absorption spectra"
    #             plot_xlabel = var_name
    #
    #         plt.title(plot_title)
    #         plt.xlabel(plot_xlabel)
    #         plt.ylabel("Wavelength (nm)")
    #         plt.savefig()
    #         plt.show()
    #
    #     except ValueError:
    #         info = "Different numbers of maxima in datasets, skipping plot."
d = r'C:\Users\madzi\OneDrive\Pulpit\TEST\test_abs_max'

abs_maxima(d, 301, 699, "")