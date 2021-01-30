def save_file(path, header, col_names, mesurements):
    with open(path, 'w') as new_file:
        new_file.writelines(header)
        if path.endswith(".txt"):
            sep = ""
        else:
            sep = ","
        for line in col_names:
            new_file.writelines("\n%s%s %s%s" % (line[0].rjust(22), sep, line[1].rjust(22), sep))
        for line in mesurements:
            x = float(line[0])
            y = float(line[1])
            new_file.writelines("\n%s%s %s%s" % (str(x).rjust(22), sep, str(y).rjust(22), sep))
        # print("File saved as " + path)
    return 0
