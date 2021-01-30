import re
import os
import sys
from math import sqrt
from random import normalvariate

def truncate_flatten(path, truncate, sigma_truncate, flatten, sigma_flatten, new_device):
    '''
    Program adjusts y-positions of the spheres in the input script for Omnisim,
    so they will appear as the truncated and flattened spheres in the baseline.
    It is done by applying the truncating and flattening factors, given in percent
    with some standard deviation.

    More info: http://www.ambrsoft.com/TrigoCalc/Sphere/Cap/SphereCap.htm

    Input:
          File with the following structure:
          (...)
          f.Exec("app.subnodes[project].subnodes[device].fsdevice.addellipsoid(layer,z,x,angle,y,sizez,sizex,sizey)")
          (...)
          Assumption: nanoparticles are placed in the "zx" or "xz" plane, so y value is to be adjusted.
    Output:
          File with a "_truncx_flaty" suffix,
          where x is the truncating factor and y is the flattening factor
    '''

    # # Truncating factor for the spheres [%]
    # truncate = -1
    # print("Spheres could be cut (truncated). 100% - full sphere, 50% - hemisphere, etc.")
    # while truncate < 0 or truncate > 100:
    #     truncate = int(input("Enter the percent where the spheres will be cut [0-100%]: "))
    #
    # sigma_truncate = -1
    # while sigma_truncate < 0:
    #     sigma_truncate = int(input("Enter the standard deviation for sphere cut, or 0: "))
    #
    # # Flattening factor for the spheres [%]
    # print("Spheres could be flattened. Y-size = 100% - full size, 50% - flatten by a half, etc.")
    # flatten = -1
    # while flatten < 0 or flatten > 100:
    #     flatten = int(input("Enter the percent of the nominal y-size of the spheres [0-100%]: "))
    #
    # sigma_flatten = -1
    # while sigma_flatten < 0:
    #     sigma_flatten = int(input("Enter the standard deviation for sphere flatten, or 0: "))
    #
    #
    # # The new device number (optionally)
    # try:
    #     new_device = int(input("Enter device number, or <cr> to keep existing one: "))
    # except ValueError:
    #     new_device = -1

    success = True
    structure = False
    info = ""
    # Read input file
    with open(path, 'r') as input_file:
        file = input_file.readlines()

    filename, ext = os.path.splitext(path)
    # Output file
    output_filename = "{}_trunc{}s{}_flat{}s{}.py".format(filename, truncate, sigma_truncate, flatten, sigma_flatten)

    with open(output_filename, 'w+') as output:
        for line in file:
            values = re.findall(r'(?<=addellipsoid\().*(?=\)\"\))', line)
            if not values:
                output.writelines(line)
            else:
                structure = True
                values_list = values[0].split(",")
                layer = int(values_list[0])
                z = float(values_list[1])
                x = float(values_list[2])
                angle = float(values_list[3])
                y = float(values_list[4])
                sizex = float(values_list[5])
                sizey = float(values_list[6])
                sizez = float(values_list[7])

                d = re.findall(r'(?<=subnodes\[)\d+(?=\])', line)
                project = int(d[0])
                if new_device == "":
                    device = int(d[1])
                else:
                    device = new_device

                # Calculate new size and y position
                R = sizex/2.0            # Radius of the original sphere
                # Truncate distribution:
                truncate_dist = normalvariate(truncate, sigma_truncate)
                h = (100-truncate_dist)*sizex / 100.0  # Height of the cap

                try:
                    r = sqrt(2*R*h-h*h)      # Radius of the cap
                except ValueError:
                    info = "Negative numbers can't have square roots. You should change parameters of truncation.."
                    success = False
                    break
                t = r/R                  # Ratio between radiuses
                rc = R/t                 # New radius of the sphere, adjusted of the ratio
                y = 2*R + y - h

                if 50 < truncate_dist < 100:
                    sizex = rc * 2
                    sizey = rc * 2
                    sizez = rc * 2

                # Flattening
                flatten_dist = normalvariate(flatten, sigma_truncate)
                y = y + sizey*(1-flatten_dist/100)/4
                sizey = sizey*flatten_dist/100

                # addellipsoid     FUNCTION(layer, z, x, angle, y, sizez, sizex, sizey)
                newline = 'f.Exec("app.subnodes[{0}].subnodes[{1}].fsdevice.addellipsoid({2},{3},{4},{5},{6},{7},{8},{9})")\n' \
                    .format(project, device, layer, z, x, angle, y, sizez, sizex, sizey)
                output.writelines(newline)
    if structure == False:
        success = False
        info = "Selected file does not have the appropriate structure."
    if success == False:
        if os.path.exists(output_filename):
            os.remove(output_filename)

    return output_filename, success, info
