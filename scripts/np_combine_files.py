import re
import math
import os
from scripts.np_read_file import ReadFile
from scripts.np_save_file import save_file


class CombineFiles:
    def __init__(self, pathA, pathB):

        """
        Combines two .cht files containing field, absorbance or flux, e.g.
        - s: subtract: E = E1 - E2 (e.g. absorbance - reference absorbance)
        - u: unpolarize: |E| = sqrt(0.5|E_TE|^2 + 0.5|E_TM|^2) (e.g. EZ and HZ polarized fluxes)
        - a: calculate absorbance: E = log10(E1/E2) (e.g. input flux / output flux)
        - t: calculate transmitance: E = E2/E1 (e.g. output flux / input flux)

        Shortcut call: np [...] [s|u|a|t]

        Input:
               Two .cht files from Omnisim (2D/1D).
        Output:
               .cht file with suffix "_x", where x is a selected option.
               In (u) case: "_ez" or "_hz" are removed from filename.
               In (a) case: prefix "abs_" is added instead of "_a" suffix.
        """

        self.result = []
        self.col_names = []
        self.result_path = ""
        self.info = ""
        self.success = True

        self.A = ReadFile(pathA)
        self.A.run_read_file()

        self.B = ReadFile(pathB)
        self.B.run_read_file()

        self.pathA = pathA
        self.pathB = pathB

        # Check if file contains the same number of measurements
        if len(self.A.measurements) != len(self.B.measurements):
            self.info = "Input files have different number of measurements!"
            self.success = False

    def subtructing(self):
        # Subtract y values, only if x are equal
        # Output filename

        if self.A.type == 'cht':
            self.result_path = re.sub(r'\.cht', '_s.cht', self.pathA)
            self.col_names.append(['Xvals', 'Yvals1'])
        elif self.A.type == 'txt':
            self.result_path = re.sub(r'\.txt', '_s.txt', self.pathA)
            self.col_names.append([self.A.x_label, self.A.y_label])
            self.col_names.append([self.A.x_unit, self.A.y_unit])
        # Subtruction
        for i in range(0, len(self.A.measurements)):
            if round(self.A.measurements[i][0], 3) == round(self.A.measurements[i][0], 3):
                s = self.A.measurements[i][1] - self.B.measurements[i][1]
                self.result.append([self.A.measurements[i][0], s])
            else:
                self.info = "X-axis are different in the input files, exiting..."
                self.success = False

        if self.success:
            save_file(self.result_path, self.A.header, self.col_names, self.result)
        return self.result_path, self.success, self.info

    def unpolarize(self):
        self.result_path = self.A.path
        self.result_path = self.result_path.replace("_hz.", ".")
        self.result_path = self.result_path.replace("_ez.", ".")

        if self.A.type == 'cht':
            self.result_path = self.result_path.replace(".cht", "_u.cht")
            self.col_names.append(['Xvals', 'Yvals1'])
        elif self.A.type == 'txt':
            self.result_path = self.result_path.replace(".txt", "_u.txt")
            self.col_names.append([self.A.x_label, self.A.y_label])
            self.col_names.append([self.A.x_unit, self.A.y_unit])

        for i in range(0, len(self.A.measurements)):
            if self.A.measurements[i][0] == self.B.measurements[i][0]:
                # |E| = sqrt(0.5|E_TE|^2 + 0.5|E_TM|^2)
                E_TE = self.A.measurements[i][1]
                E_TM = self.B.measurements[i][1]
                try:
                    y = math.sqrt(0.5*abs(E_TE)**2 + 0.5*abs(E_TM)**2)
                except (ZeroDivisionError, ValueError):
                    y = 0
                self.result.append([self.A.measurements[i][0], y])

        save_file(self.result_path, self.A.header, self.col_names, self.result)
        return self.result_path, self.success, self.info

    def absorbance(self):
        head, tail = os.path.split(self.pathA)
        if "F_in" in tail:
            tail = re.sub("F_in", "abs", tail)
        if "_a" in tail:
            tail = re.sub("_a", "", tail)
        self.result_path = os.path.join(head, tail)

        header = self.A.header
        col_names = []
        if self.A.type == "cht":
            header = header.replace(self.A.title, "Absorbance")
            if self.A.y_unit == "/W/um":
                header = header.replace(self.A.y_label + " " + self.A.y_unit, "Absorbance (%/100)")
            if self.A.y_unit == "/dB":
                header = header.replace(self.A.y_label + " " + self.A.y_unit, "Absorbance (%/10)")
            header = header.replace(" /um", " (µm)")
            col_names.append(['Xvals', 'Yvals1'])

        elif self.A.type == "txt":
            header = header.replace(self.A.title, "Absorbance")
            col_names.append([self.A.x_label, "Absorbance"])
            x_unit = self.A.x_unit
            if self.A.x_unit == "/um":
                x_unit = "(µm)"
            if self.A.y_unit == "/W/um":
                col_names.append([x_unit, "(%/100)"])
            elif self.A.y_unit == "/dB":
                col_names.append([x_unit, "(%/10)"])

        for i in range(0, len(self.A.measurements)):
            if self.A.measurements[i][0] == self.B.measurements[i][0]:
                # e = log10(e1/e2)
                e1 = self.A.measurements[i][1]
                e2 = self.B.measurements[i][1]
                try:
                    e = math.log10(e1 / e2)
                except (ZeroDivisionError, ValueError):
                    e = 0
                self.result.append([self.A.measurements[i][0], e])
        if self.success:
            save_file(self.result_path, header, col_names, self.result)
        return self.result_path, self.success, self.info

    def transmitance(self):
        if self.A.type == 'cht':
            self.result_path = re.sub(r'\.cht', '_t.cht', self.pathA)
            self.col_names.append(['Xvals', 'Yvals1'])
        elif self.A.type == 'txt':
            self.result_path = re.sub(r'\.txt', '_t.txt', self.pathA)
            self.col_names.append([self.A.x_label, self.A.y_label])
            self.col_names.append([self.A.x_unit, self.A.y_unit])

        header = self.A.header
        col_names = []
        if self.A.type == "cht":
            col_names.append(['Xvals', 'Yvals1'])

        for i in range(0, len(self.A.measurements)):
            if self.A.measurements[i][0] == self.B.measurements[i][0]:
                # E = E2/E1
                e1 = self.A.measurements[i][1]
                e2 = self.B.measurements[i][1]
                try:
                    e = e2 / e1
                except (ZeroDivisionError, ValueError):
                    e = 0
                self.result.append([self.A.measurements[i][0], e])

        if self.success:
            save_file(self.result_path, header, col_names, self.result)
        return self.result_path, self.success, self.info
