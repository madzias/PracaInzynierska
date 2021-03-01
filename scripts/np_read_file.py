import re
import sys


class ReadFile:
    def __init__(self, p):
        self.path = p
        self.file_lines = ''
        self.title = False
        self.type = ''
        self.measurements = []
        self.units = ''
        self.labels = ''
        self.graph = ''
        self.data_separator = ''
        self.header = ''
        self.x_label = ''
        self.x_unit = ''
        self.y_label = ''
        self.y_unit = ''
        self.z_label = ''
        self.z_unit = ''

        with open(self.path, 'r') as file:
            self.file = file.read()
            if self.file.startswith("#"):
                self.file = re.sub("#", "", self.file)
            self.file_lines = self.file.splitlines()

    def path_info(self):
        if self.path.endswith(".txt"):
            self.type = 'txt'
        elif self.path.endswith(".cht"):
            self.type = 'cht'
        else:
            print("The file must be .txt or .cht")
            sys.exit()

    def read_title(self):
        if self.type == 'txt':
            for line in self.file_lines:
                if line.__contains__('FDTD'):
                    self.title = line
                    break
            if self.title is False:
                print("Your file is incorrect. Your file needs to contain a title with 'FDTD' inside")

        elif self.type == 'cht':
            a = re.findall(r'(?<=").*(?="\s+//\stitle)', self.file)
            if len(a) > 0:
                self.title = a[0]
            if self.title is False:
                print("Your file is incorrect. Your file needs to contain a title with 'FDTD' inside")
                sys.exit()
            if "SGCHART2D" in self.file_lines[0]:
                self.graph = "2D"
                self.data_separator = ","
            else:
                self.graph = "1D"
                self.data_separator = " "
        else:
            print("Your file is incorrect. Your file needs to contain a title with 'FDTD' inside")
            return 0

    def read_header(self):
        if self.graph == "2D":
            self.header = re.match(r'^(.*?)//---', self.file, flags=re.DOTALL).group()[:-5]
        else:
            self.header = re.search(r'(^).*(?<=-----)', self.file, flags=re.DOTALL).group()

    def read_units_labels(self):
        if self.type == 'txt':
            for line in self.file_lines:
                if line.__contains__('/'):
                    self.units = line
                    self.labels = self.file_lines[self.file_lines.index(line) - 1]
                    break
            self.units = list(filter(None, self.units.split(' ')))
            self.x_unit = self.units[0]
            self.y_unit = self.units[1]
            self.labels = list(filter(None, self.labels.split('  ')))
            self.x_label = self.labels[0].strip()
            self.y_label = self.labels[1].strip()

        elif self.type == 'cht' and self.graph == "1D":
            a = re.findall(r'(?<=XSCALE\s["])([^"]+)', self.file)
            self.x_label = a[0].rsplit(' ', 1)[0]
            self.x_unit = a[0].rsplit(' ', 1)[1]
            b = re.findall(r'(?<=YSCALE\s["])([^"]+)', self.file)
            self.y_label = b[0].rsplit(' ', 1)[0]
            self.y_unit = b[0].rsplit(' ', 1)[1]
        elif self.type == 'cht' and self.graph == "2D":
            a = re.findall(r'(?<=").*(?="\s+// x-title)', self.file)
            self.x_label = a[0].rsplit(' ', 1)[0]
            self.x_unit = a[0].rsplit(' ', 1)[1]
            b = re.findall(r'(?<=").*(?="\s+// y-title)', self.file)
            self.y_label = b[0].rsplit(' ', 1)[0]
            self.y_unit = b[0].rsplit(' ', 1)[1]
            c = re.findall(r'(?<=").*(?="\s+// z-title)', self.file)
            self.z_label = c[0].rsplit(' ', 1)[0]
            self.z_unit = c[0].rsplit(' ', 1)[1]
        else:
            print("Wrong file. Try again.")
            sys.exit()

    def read_mesurements(self):
        if self.type == 'txt':
            for line in self.file_lines:
                a = re.findall(r'\s+\d+.*\s.*', line)
                if len(a) > 0:
                    a = a[0].split(' ')
                    a = list(filter(None, a))
                    self.measurements.append([float(a[0]), float(a[1])])
        elif self.type == 'cht' and self.graph == "1D":
            start = False
            for line in self.file_lines:
                if "Xvals" and "Yvals1" in line:
                    start = True
                if start:
                    if re.search(r'.*(\d+[.]\d+).*(\d+[.]\d+).*', line):
                        a = line.split(',')
                        a = list(filter(None, a))
                        self.measurements.append([float(a[0]), float(a[1])])
        elif self.type == 'cht' and self.graph == "2D":
            for line in self.file_lines:
                a = re.findall(r'(?=-{0,1}\d+\.\d+).*', line)
                if len(a) > 0 and len(line) > 40:
                    a = a[0].split(' ')
                    a = list(filter(None, a))
                    self.measurements.append(a)

    def run_read_file(self):
        self.path_info()
        self.read_header()
        self.read_title()
        self.read_units_labels()
        self.read_mesurements()
