#!/usr/bin/env python3
import sys
import struct

class Leaf:
    def __init__(self, priorety, char):
        self.priorety = priorety
        self.char = char
    
    def __lt__(self, other):
        return self.priorety <= other.priorety
class Node:
    def __init__(self, elem1, elem2):
        self.priorety = elem1.priorety + elem2.priorety
        self.right = elem1
        self.left = elem2

    def __lt__(self, other):
        return self.priorety <= other.priorety
    

def rawbytes(s):
    """Convert a string to raw bytes without encoding"""
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('B', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)

def generate_huffman(root, code='', huffman_codes=dict()):
    if type(root.right) is Leaf:
        huffman_codes[root.right.char] = code + '1'
    else:
        huffman_codes = generate_huffman(root.right, code + '1', huffman_codes)
    if type(root.left) is Leaf:
        huffman_codes[root.left.char] = code + '0'
    else:
        huffman_codes = generate_huffman(root.left, code + '0', huffman_codes)
    return huffman_codes

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for _ in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text

def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1*extra_padding]

    return encoded_text

def get_byte_array(padded_encoded_text):
    if (len(padded_encoded_text) % 8 != 0):
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    print(b)
    return b



def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def generate_tree(sort_list_leafs):
    while (len(sort_list_leafs) >= 2):
        first = sort_list_leafs.pop(0)
        second = sort_list_leafs.pop(0)
        new_node = Node(first, second)
        sort_list_leafs.append(new_node)
        sort_list_leafs.sort()
    root_node = sort_list_leafs[0]
    return root_node

def counting_charaters(input):
    dict_chars = {}
    for i in range(len(input)):
        dict_chars[chr(input[i])] = dict_chars.get(chr(input[i]), 0) + 1
    return dict_chars

def to_binary(enc_text):
    result = ''
    for i in enc_text:
        bin_byte = bin(i)[2:].rjust(8, '0')
        result += bin_byte
    return result

def huf_decompress(bin_encoded_text, inv_huffman_codes):
    text = ''
    next_code = ''
    for bit in bin_encoded_text:
        next_code += bit
        if (next_code in inv_huffman_codes.keys()):
            text += inv_huffman_codes[next_code]
            next_code = ''
    return text

def help():
    return "Using: huf [(c)ompress\\(d)ecompress] <input_file> <output_file>"

def compress():
    filenamein = sys.argv[2]
    filenameout = sys.argv[3]
    f = open(filenamein, 'rb')
    input = f.read()
    f.close()

    dict_chars = counting_charaters(input)
    print(dict_chars)
    sort_list_leafs = sorted([Leaf(dict_chars[i], i) for i in dict_chars])
    root_node = generate_tree(sort_list_leafs)
    huffman_codes = generate_huffman(root_node)
    print(huffman_codes)

    f = open(filenameout, 'wb')
    f.write(b"HUF") # signature
    col_letters = len(huffman_codes.keys()).to_bytes(1, byteorder='little')
    print(col_letters)
    f.write(col_letters)
    for letter, code in dict_chars.items():
        f.write(rawbytes(letter))
        f.write(code.to_bytes(4, byteorder='little'))
    enc_text = ''
    for i in input:
        ch = chr(i)
        enc_text += huffman_codes[ch]
    enc_text_pad = pad_encoded_text(enc_text)
    print(enc_text_pad)
    out = get_byte_array(enc_text_pad)
    f.write(bytes(out))

def decompress():
    filenamein = sys.argv[2]
    filenameout = sys.argv[3]
    f = open(filenamein, 'rb')
    input = f.read()
    f.close()
    col_letters = input[3]
    print(col_letters)
    header = input[4:5*col_letters + 4]
    print(header)
    enc_text_pad = input[5*col_letters + 4:]
    print(enc_text_pad)
    dict_chars = dict()
    for i in range(col_letters):
        dict_chars[chr(header[i*5])] = int.from_bytes(header[i*5+1:i*5+5], byteorder='little')
    print(dict_chars)
    print(len(dict_chars.keys()))


    sort_list_leafs = sorted([Leaf(dict_chars[i], i) for i in dict_chars])
    root_node = generate_tree(sort_list_leafs)
    huffman_codes = generate_huffman(root_node)
    print(huffman_codes)
    inv_huffman_codes = {v: k for k, v in huffman_codes.items()}
    print(inv_huffman_codes)
    print(enc_text_pad)
    bin_enc_text_pad = to_binary(enc_text_pad)
    print("bin_enc_text_pad", bin_enc_text_pad)
    bin_enc_text = remove_padding(bin_enc_text_pad)
    print("bin_enc_text", bin_enc_text)
    text = huf_decompress(bin_enc_text, inv_huffman_codes)
    print("text", text)
    f = open(filenameout, 'wb')
    f.write(rawbytes(text))
    f.close()

if __name__ == '__main__':
    if (len(sys.argv) != 4):
        print(help())
        exit(0)
    if (sys.argv[1] == 'c'):
        compress()
    elif (sys.argv[1] == 'd'):
        decompress()
    else:
        print(help())
