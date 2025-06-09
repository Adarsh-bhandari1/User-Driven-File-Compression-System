import lzma

def compress(input_path, output_path):
    with open(input_path, "rb") as fin, lzma.open(output_path, "wb") as fout:
        fout.write(fin.read())
