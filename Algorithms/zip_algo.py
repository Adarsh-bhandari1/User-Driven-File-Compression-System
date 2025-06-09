import zipfile
import os

def compress(input_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        arcname = os.path.basename(input_path)
        zipf.write(input_path, arcname=arcname)

def decompress(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(path=extract_dir)