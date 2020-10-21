"""
author: Hanbing Guo
data: 2020/4/24
"""

name_length = 5
postfix = '.bmp'
pad_char = '0'

def gen_file_name(count):
    out_name = (name_length - len(str(count))) * pad_char + str(count) + postfix

    return out_name, count + 1