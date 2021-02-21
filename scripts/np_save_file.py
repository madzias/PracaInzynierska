def save_file(path, header, col_names, mesurements):
    with open(path, 'w') as new_file:
        new_file.writelines(header)
        # Separator
        if path.endswith(".txt"):
            sep = ""
        else:
            sep = ","
        # Column width
        len_x = 0
        len_y = 0
        for line in mesurements:
            if len(str(line[0])) > len_x:
                len_x = len(str(line[0]))
            if len(str(line[1])) > len_y:
                len_y = len(str(line[1]))
        len_x += 3
        len_y += 3
        # Write column names
        for line in col_names:
            new_file.writelines("\n%s%s %s%s" % (line[0].rjust(len_x), sep, line[1].rjust(len_y), sep))
        # Write mesurements
        for line in mesurements:
            x = float(line[0])
            y = float(line[1])
            new_file.writelines("\n%s%s %s%s" % (str(x).rjust(len_x), sep, str(y).rjust(len_y), sep))
    return 0
