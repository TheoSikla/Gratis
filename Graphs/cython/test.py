from Graphs.cython.homogeneous import generate_graph
from Graphs.cython.pp import generate_graph_pure
from Support_Folders.timer import timeit
import sys
import re



REPEATS_RE = re.compile(r'(.)\1*')
NUMBERS_RE = re.compile(r'(\d+)(.)')


def to_numbers(match):
    length = len(match.group(0))
    return (
        str(length) + match.group(1)
        if length > 1
        else match.group(1)
    )


def from_numbers(match):
    return int(match.group(1)) * match.group(2)


def encode(string):
    return REPEATS_RE.sub(to_numbers, string)


def decode(string):
    # NUMBERS_RE.sub(from_numbers, string)
    return ''.join([''.join(str(ord(digit))) for digit in NUMBERS_RE.sub(from_numbers, string)])

x = 10000


@timeit
def t():
    string = generate_graph(x)
    # print(a[0])
    print(sys.getsizeof(string))
    # print(string[0])
    enc = encode([''.join(str(_) for _ in string[0])][0])
    print(enc)
    dec = decode(enc)
    print(dec)
    # print(len(dec))
    # print(sys.getsizeof(encode([''.join(str(_) for _ in string[0])][0])))
    # import zib
    #     # print([''.join(str(_) for _ in string[0])][0].encode("utf-8"))
    #     # # print(type([''.join(str(_) for _ in string[0])][0]))
    #     # st = [''.join(str(_) for _ in string[0])][0]
    #     # print(sys.getsizeof(zlib.compress(st.encode("utf-8"))) * 10000)
    #     # print(zlib.compress(st.encode("utf-8")))lib
    # print([''.join(str(_) for _ in string[0])][0].encode("utf-8"))
    # # print(type([''.join(str(_) for _ in string[0])][0]))
    # st = [''.join(str(_) for _ in string[0])][0]
    # print(sys.getsizeof(zlib.compress(st.encode("utf-8"))) * 10000)
    # print(zlib.compress(st.encode("utf-8")))


@timeit
def r():
    generate_graph_pure(x)


# t()
# r()

import random
random_string = ''
for j in range(10):
    for i in range(100):
        random_string += chr(random.randint(0, 1))

    print(random_string)
    enc = encode(random_string)
    print(enc)
    # print(len(enc))
    dec = decode(enc)
    # print(dec)
    # print(len(dec))
    print(''.join([''.join(str(ord(digit))) for digit in random_string]))
    assert ''.join([''.join(str(ord(digit))) for digit in random_string]) == dec
    random_string = ''


# random_string = 'aaaaabbhhnaaasssdd'
# print(random_string)
# enc = encode(random_string)
# print(enc)
# dec = decode(enc)
# print(dec)