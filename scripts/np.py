import os, sys
import argparse #biblioteka do analizowania argumentów
from scripts.np_change_type import change_type
from scripts.np_combine_files import CombineFiles

def read_arguments():
    #stworzenie parsera
    parser = argparse.ArgumentParser(description='List of options')


    #dodawanie opcji
    parser.add_argument('-0', '--database', help='Make material database using the refractive index', nargs='+')
    parser.add_argument('-1', '--plane', help='Change plane from xy to xz (and some other options)')
    parser.add_argument('-2', '--truncate', help='Truncate the spheres by some factor')
    parser.add_argument('-3', '--convert', help='Convert .txt sensor data into the .cht format or .cht sensor data into the .txt format', nargs=1)

    combine = parser.add_argument_group('combine')
    combine.add_argument('-4', '--combine', choices=['s', 'a', 't', 'u'], help='Combine two .cht files to substract data[s], unpolarize[s], calculate absorbance [a] and transmitance [t]')
    combine.add_argument('dir1')
    combine.add_argument('dir2')

    parser.add_argument('-5', '--max', help='Find local maxima in the .cht/.txt files with absorbance, and plot the result if possible')
    parser.add_argument('-6', '--plot', help='Plot (and save in the .png format) the .cht file')
    a = parser.parse_args()
    return a

def run_option(arguments):
    if arguments.database:
        for i in arguments.database:
            print(i)
    elif arguments.convert:
        if os.path.isfile(arguments.convert[0]):
            change_type(arguments.convert[0])
        else:
            print("File does not exist. Exiting...")
            sys.exit()
    elif arguments.combine:
        if os.path.isfile(arguments.dir1) and os.path.isfile(arguments.dir2):
            print(arguments.combine)
            if arguments.combine == 's':
                a = CombineFiles(arguments.dir1, arguments.dir2)
                a.subtructing()
            elif arguments.combine == 'u':
                print("start")
                a = CombineFiles(arguments.dir1, arguments.dir2)
                a.unpolarize()
            elif arguments.combine == 'a':
                print("start")
                a = CombineFiles(arguments.dir1, arguments.dir2)
                a.absorbance()
            elif arguments.combine == 't':
                print("start")
                a = CombineFiles(arguments.dir1, arguments.dir2)
                a.transmitance()

        else:
            print("No such files")





a = read_arguments()
run_option(a)



"""modules = \
{\
0:["np_make_material_database","Make material database using the refractive index"],\
1:["np_change_plane","Change plane from xy to xz (and some other options)"],\
2:["np_truncate_flatten","Truncate the spheres by some factor"],\
3:["np_txt_to_cht","Convert .txt sensor data into the .cht format"],\
4:["np_combine_cht","Combine two .cht files to substract data, unpolarize, calculate absorbance and transmitance"],\
5:["np_abs_max","Find local maxima in the .cht/.txt files with absorbance, and plot the result if possible"],\
6:["np_plot_cht","Plot (and save in the .png format) the .cht file"],\
}"""