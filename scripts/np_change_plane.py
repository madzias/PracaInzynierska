import readchar, re
#from np_ps import set, select_file

def change_plane(path):
    '''
    Manipulates the Omnisim input file, created by the Nanoparticle Detector:
    changes plane in which nanoparticles are located - from xy to xz (or zx),
    and also allows for some other corrections as change project and device numbers,
    layer indices, baseline, and reversing values on the x-axis.

    Input:
          Python file (.py) with the following structure:
          (...)
          f.Exec("app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)")
          (...)
    Output:
          Python file (.py) with a "_xz" suffix.
    '''

    # New project, device, and nanoparticles layer
    # Old values will be overwritten
    project = 1
    device = 2
    layer = 1

    # New baseline (y-axis) for nanoparticles
    baseline = 0.5

    # In omnisim, z axis is horizontal, and x axis is vertical,
    # so it may be convenient to exchange x and z in the output to achieve
    # direct comparison to the SEM image
    set_orientation_zx = True

    # Reverse x-axis or not, to have the the same view as on the SEM image
    # To do this, x_max needs to be known
    x_reverse = False
    x_max = 1.285 # for SEM: mag 100 000 x

    # Collect input file name
    #filename = select_file('py')

    # Collect parameters
    ans = ""
    #while ans != readchar.key.ENTER:
    print()
    print("Current settings:")
    print("Project number = ", project)
    print("Device number = ", device)
    print("NP layer index = ", layer)
    print("NP baseline = ", baseline)
    print("Set orientation ZX = ", set_orientation_zx)
    print("Reversing x values = ", x_reverse)
    print("Maximum x value for reversing = ", x_max)
        # print()
        # print("Press <cr> to accept, or anything else to change.")
        #
        # ans = readchar.readkey()
        # if ans != readchar.key.ENTER:
        #     print()
        #     print("Modify settings:")
        #     project = set("project", project)
        #     device = set("device", device)
        #     layer = set("layer", layer)
        #     baseline = set("baseline", baseline)
        #     set_orientation_zx = set("set_orientation_zx", set_orientation_zx)
        #     x_reverse = set("x_reverse", x_reverse)
        #     if x_reverse:
        #         x_max = set("x_max", x_max)

    with open(path, 'r') as input_file:
        file = input_file.readlines()

    output_path = re.sub('\.py', '_xz.py', path)
    with open(output_path, 'w+') as output:

        for line in file:
            values = re.findall(r'(?<=addellipsoid\().*(?=\)\"\))', line)
            if not values:
                output.writelines(line)
            else:
                values_list = values[0].split(",")
                print(values_list)
                z = float(values_list[1])
                x = float(values_list[2])
                angle = float(values_list[3])
                y = float(values_list[4])
                sizex = float(values_list[5])
                sizey = float(values_list[6])
                sizez = float(values_list[7])
                print("wczytane")
                print("x = ", x)
                print("y = ", y)
                print("z = ", z)
                print("-------")
                # Correct the value for the border between substrate and NPs
                old_baseline = z + sizez/2.0
                if baseline != old_baseline:
                    baseline_correction = baseline - old_baseline
                    z = z + baseline_correction

                # Exchange z and y and construct a new line
                print("x = ", x)
                print("y = ", y)
                print("z = ", z)
                z, y = y, z
                if set_orientation_zx:
                    x, z = z, x
                print("x = ", x)
                print("y = ", y)
                print("z = ", z)
                if x_reverse:
                    x = -x + x_max
                print("x = ", x)
                print("y = ", y)
                print("z = ", z)
                # addellipsoid: FUNCTION(layer, z, x, angle, y, sizez, sizex, sizey)
                newline = 'f.Exec("app.subnodes[{0}].subnodes[{1}].fsdevice.addellipsoid({2},{3},{4},{5},{6},{7},{8},{9})")\n' \
                        .format(project, device, layer, z, x, angle, y, sizez, sizex, sizey)
                output.write(newline)


# file = r"C:\Users\madzi\OneDrive\Pulpit\TEST\change_plane\Ag_7nm_550C_15min_028_1024x944_2019-09-11_15-29-34-omnisim1.py"
# change_plane(file)