import bz2

def compress(input_path, output_path):
    with open(input_path, "rb") as fin, bz2.open(output_path, "wb") as fout:
        fout.write(fin.read())

def decompress(input_path, output_path):
    with bz2.open(input_path, "rb") as fin, open(output_path, "wb") as fout:
        fout.write(fin.read())