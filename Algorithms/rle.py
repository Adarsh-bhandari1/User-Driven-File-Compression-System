import os

def compress(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = file.read()

    encoded = []
    i = 0
    while i < len(data):
        count = 1
        while i + 1 < len(data) and data[i] == data[i + 1]:
            count += 1
            i += 1
        if count > 4:
            encoded.append(f"@{data[i]}{count}")
        else:
            encoded.extend(data[i] * count)
        i += 1

    encoded_str = ''.join(encoded)

    original_size = os.path.getsize(input_path)
    encoded_size = len(encoded_str.encode('utf-8'))

    if encoded_size >= original_size:
        print(f"RLE skipped: Compressed size ({encoded_size} bytes) is not smaller than original ({original_size} bytes).")
        return

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(encoded_str)

    print(f" Compression Done: {output_path}")

def decompress(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = file.read()

    decoded = []
    i = 0
    while i < len(data):
        if data[i] == '@':
            char = data[i + 1]
            count_str = ''
            i += 2
            while i < len(data) and data[i].isdigit():
                count_str += data[i]
                i += 1
            count = int(count_str)
            decoded.append(char * count)
        else:
            decoded.append(data[i])
            i += 1

    decoded_str = ''.join(decoded)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decoded_str)
