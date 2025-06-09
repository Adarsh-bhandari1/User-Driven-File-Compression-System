import heapq
import os
import json
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    freq = defaultdict(int)
    for ch in text:
        freq[ch] += 1
    return dict(freq)

def build_huffman_tree(freq_table):
    heap = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def build_codes(node, code='', codes=None):
    if codes is None:
        codes = {}
    if node:
        if node.char is not None:
            codes[node.char] = code
        build_codes(node.left, code + '0', codes)
        build_codes(node.right, code + '1', codes)
    return codes

def compress(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()

    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    codes = build_codes(huffman_tree)
    encoded_text = ''.join(codes[char] for char in text)

    # Pad to full bytes
    padding = 8 - len(encoded_text) % 8
    if padding != 8:
        encoded_text += '0' * padding
    else:
        padding = 0
    padded_info = "{0:08b}".format(padding)
    encoded_text = padded_info + encoded_text

    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte, 2))

    # Write frequency table as JSON at the start, then a newline, then the binary data
    with open(output_path, 'wb') as output:
        freq_json = json.dumps(freq_table)
        output.write((freq_json + '\n').encode('utf-8'))
        output.write(bytes(b))

def decompress(input_path, output_path):
    import json

    with open(input_path, 'rb') as file:
        # Read the frequency table (JSON) from the first line
        freq_json = b''
        while True:
            ch = file.read(1)
            if ch == b'\n':
                break
            freq_json += ch
        freq_table = json.loads(freq_json.decode('utf-8'))

        # Read the rest as binary data
        bit_string = ""
        byte = file.read(1)
        while byte:
            bits = bin(ord(byte))[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

    # Remove padding
    padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:]
    if padding > 0:
        bit_string = bit_string[:-padding]

    # Rebuild Huffman tree and codes
    huffman_tree = build_huffman_tree(freq_table)

    # Decode the bit string
    decoded = []
    node = huffman_tree
    for bit in bit_string:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.char is not None:
            decoded.append(node.char)
            node = huffman_tree

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(''.join(decoded))
