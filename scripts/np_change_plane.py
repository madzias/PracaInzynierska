import re
import os


def change_plane(path, project, device, layer, baseline, set_orientation_zx, x_reverse, x_max):
    """
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
    """
    success = True
    structure = False
    info = ""

    if x_reverse == "False":
        x_reverse = False
    else:
        x_reverse = True

    if set_orientation_zx == "False":
        set_orientation_zx = False
    else:
        set_orientation_zx = True

    # Open file
    with open(path, 'r') as input_file:
        file = input_file.readlines()

    output_path = re.sub('[.]py', '_xz.py', path)
    with open(output_path, 'w+') as output:

        for line in file:
            values = re.findall(r'(?<=addellipsoid\().*(?=\)\"\))', line)
            if not values:
                output.writelines(line)
            else:
                structure = True
                values_list = values[0].split(",")
                z = float(values_list[1])
                x = float(values_list[2])
                angle = float(values_list[3])
                y = float(values_list[4])
                sizex = float(values_list[5])
                sizey = float(values_list[6])
                sizez = float(values_list[7])

                # Correct the value for the border between substrate and NPs
                baseline = float(baseline)
                old_baseline = z + sizez/2.0
                if baseline != old_baseline:
                    baseline_correction = baseline - old_baseline
                    z = z + baseline_correction

                # Exchange z and y and construct a new line
                z, y = y, z
                if set_orientation_zx:
                    x, z = z, x

                x_max = float(x_max)
                if x_reverse:
                    x = -x + x_max

                # Structure: addellipsoid: FUNCTION(layer, z, x, angle, y, sizez, sizex, sizey)
                newline = 'f.Exec("app.subnodes[{0}].subnodes[{1}].fsdevice.addellipsoid({2},{3},{4},{5},{6},{7},{8},{9})")\n' \
                        .format(project, device, layer, z, x, angle, y, sizez, sizex, sizey)
                output.write(newline)

    if not structure:
        success = False
        info = "Selected file does not have the appropriate structure."
    if not success:
        if os.path.exists(output_path):
            os.remove(output_path)

    return output_path, success, info
