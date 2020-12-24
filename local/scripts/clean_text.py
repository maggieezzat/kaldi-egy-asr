

def clean_text(in_file, out_file):
    with open(out_file, 'w') as out:
        with open(in_file, 'r') as f:
            for line in f:
                line = line.strip().split(" ", 1)
                fname = line[0]
                