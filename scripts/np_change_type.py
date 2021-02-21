import re, pathlib, sys
from scripts.np_read_file import ReadFile
from scripts.np_save_file import save_file

def change_type(path):
    r = ReadFile(path)  #Read txt file
    r.run_read_file()
    mesurements = []
    col_names = []
    new_path = ''
    success = True
    #structure = False
    info = ""

    if r.type == 'txt':
        with open(r'..\scripts\cht_header.txt', 'r') as header:
            header = header.read()

        #Substitute elements in header
        header = re.sub('%%TITLE%%', r.title, header)
        header = re.sub('%%X-LABEL%%', r.x_label, header)
        header = re.sub('%%X-UNIT%%', r.x_unit, header)
        header = re.sub('%%Y-LABEL%%', r.y_label, header)
        header = re.sub('%%Y-UNIT%%', r.y_unit, header)
        header = re.sub('%%NUMBER_OF_MESUREMENTS%%', str(len(r.mesurements)), header)

        col_names.append(['Xvals', 'Yvals1'])

        #Create cht path
        new_path = re.sub('\.txt', '.cht', path)

        #Create lines with mesurements for cht and save
        # for i in r.mesurements:
        #     x = float(i[0])
        #     y = i[1]
        #     mesurements.append("%s, %s,\n" % (str(x).rjust(13), str(y).rjust(13)))

        save_file(new_path, header, col_names, r.mesurements)

    elif r.type == 'cht':
        with open(r'..\scripts\txt_header.txt', 'r') as header:
            header = header.read()

            header = re.sub('%%TITLE%%', r.title, header)

            if r.title.startswith('In'):
                header = re.sub('%%IN_OUT%%', 'IN-', header)
            elif r.title.startswith('Out'):
                header = re.sub('%%IN_OUT%%', 'OUT', header)
            else:
                info = "Title is incorrect. Cannot check if file is in or out positive flux."
                success = False
            col_names.append([r.x_label, r.y_label])
            col_names.append([r.x_unit, r.y_unit])

        #Create txt file
        new_path = re.sub('\.cht', '.txt', path)

        #Create lines with mesurements for cht and save
        # for i in r.mesurements:
        #     x = format(float(i[0]), "10.6e")
        #     y = format(float(i[1]), "10.6e")
        #     mesurements.append("\n%s%s" % (str(x).rjust(14), str(y).rjust(16)))
    if success:
        save_file(new_path, header, col_names, r.mesurements)
    return new_path, success, info

# path = r'C:\Users\madzi\OneDrive\Pulpit\TEST\in1moj.cht'
# change_type(path)
