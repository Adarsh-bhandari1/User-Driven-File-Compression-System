import os
def compress(input_path, output_path):
    with open(input_path, 'r') as file:
        data = file.read()

    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ''
    result = []
    for c in data:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])

    compressed_data = ' '.join(map(str, result))
    with open(output_path, 'w') as file:
        file.write(compressed_data)

    original_size = os.path.getsize(input_path)
    encoded_size = len(compressed_data.encode('utf-8'))
    print(f" Compression Done: {output_path}")
    
def decompress(input_path, output_path):
    with open(input_path, 'r') as file:
        compressed = list(map(int, file.read().split()))

    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    w = chr(compressed.pop(0))
    result = [w]
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry

    with open(output_path, 'w') as file:
        file.write(''.join(result))
