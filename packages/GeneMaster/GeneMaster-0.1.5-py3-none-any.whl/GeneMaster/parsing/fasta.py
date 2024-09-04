def read_fasta(file_path):
    dnas = {}
    with open(file_path) as fast:
        lines = fast.readlines()
        id = ''
        string = ''
        for line in lines:
            if line.startswith('>'):
                if id:
                    dnas[id] = string
                    string = ''
                id = line[1:].strip()
            else:
                string += line.strip()

        if id:
            dnas[id] = string

    return dnas