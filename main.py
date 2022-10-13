#!/usr/bin/env python3
import sys

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

if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, 'rb')
    input = f.read()
    f.close()

    dict_chars = {}
    for i in range(len(input)):
        dict_chars[chr(input[i])] = dict_chars.get(chr(input[i]), 0) + 1

    print(dict_chars)
    sort_list_leafs = sorted([Leaf(dict_chars[i], i) for i in dict_chars])
    sort_list_tmp = sort_list_leafs

    while (len(sort_list_tmp) >= 2):
        first = sort_list_tmp.pop(0)
        second = sort_list_tmp.pop(0)
        new_node = Node(first, second)
        sort_list_tmp.append(new_node)
        sort_list_tmp.sort()
    root_node = sort_list_tmp[0]
    huffman_codes = generate_huffman(root_node)
    print(huffman_codes)
