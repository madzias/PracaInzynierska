import pandas
import os


def make_database(path1, path2, minv, maxv, material_name):
    # Open input files
    with open(path1) as re_file:
        data_re = pandas.read_csv(re_file, header=None)

    with open(path2) as im_file:
        data_im = pandas.read_csv(im_file, header=None)

    if material_name == "":
        material_name = "NEW_MATERIAL"

    head, tail = os.path.split(path1)
    output_file = os.path.join(head, "ps_refbase.mat")

    # Create new file
    with open(output_file, "w") as output:
        header = "// Materials Parameters Database - PS \
                \n    //--------------------------------------------\
                \n    <materbase(2.21)>\
                \n    INCLUDE refbase.mat\
                \n    //--------------------------------------------"

        output.write(header)
        output.write("\n    BEGIN {}".format(material_name))

        output.write("\nRIX_EXPRESSION \"spline(lambda")
        for index, row in data_re.iterrows():
            line = ", {}, {}".format(str(format(row[0], ".6f")), str(format(row[1], ".6f")))
            output.write(line)
        output.write(")\"")

        output.writelines("\nMATLOSS_EXPRESSION \"4*_PI*10000/lambda * spline(lambda")
        for index, row in data_im.iterrows():
            line = ", {}, {}".format(str(format(row[0], ".6f")), str(format(row[1], ".6f")))
            output.write(line)
        output.write(")\"")

        output.write("\nLAMBDA_REF 0")
        output.write("\nLAMBDA_RANGE {} {}".format(minv, maxv))
        output.write("\nEND\n")

    return output_file
