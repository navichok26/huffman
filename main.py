#!/usr/bin/env python3
import sys

class Node:
    def __init__(self, elem1, elem2):
        self.priorety = 0
        self.right = None
        self.left = None
        if type(elem1) is Node:
            self.priorety += elem1.priorety
            self.right = elem1
        else:
            self.priorety += elem1[0]
            self.right = elem1
        if type(elem2) is Node:
            self.priorety += elem2.priorety
            self.left = elem2
        else:
            self.priorety += elem2[0]
            self.left = elem2

if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, 'rb')
    input = f.read()
    f.close()
    dict_chars = {}
    for i in range(len(input)):
        dict_chars[input[i]] = dict_chars.get(input[i], 0) + 1
