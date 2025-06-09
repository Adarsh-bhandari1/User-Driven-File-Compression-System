from PIL import Image

def compress(input_path, output_path, mode="Low"):
    """
    Compress a BMP file.
    mode: "Low" for lossless (PNG), "High" for lossy (JPEG)
    """
    img = Image.open(input_path)
    if mode == "Low":
        img.save(output_path, "PNG")
    else:  # High (Lossy)
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=85)