import time
import calendar
import convutils
import os, glob
import codecs

char_size = 8
line_delim = "*" * 50

now = lambda: calendar.timegm(time.gmtime())
get_bin = lambda x, n = char_size: convutils.get_bin(x, n)
br = lambda: print(line_delim)
nl = lambda: print("")

key_ext = ".key"
msg_ext = ".txt"
scr_ext = ".scr"

data_dir = "data/"

def read(file) -> str:
    with open(data_dir + file) as f:
        return f.read()

def write(file, text: str):
    with open(data_dir + file, "w") as f:
        f.write(text)

def write_bytes(file, b_arr: bytes):
    with open(data_dir + file, "wb") as f:
        f.write(b_arr)

def read_bytes(file) -> bytes:
    with open(data_dir + file, "rb") as f:
        return f.read().rstrip()

def list_files(ext):
    flist = sorted(glob.glob("./" + data_dir + "/*" + ext), key=os.path.getmtime)
    i = 1
    for file in flist:
        if i % 5 == 0:
            nl()

        print(file[2:] + "    ", end="")
        i += 1

def get_bit(n, k):
    return ((n & (1 << (k - 1))) >> (k - 1))

def bit_set(value, bit):
    return value | (1<<bit)

def bit_unset(value, bit):
    return value & ~(1<<bit)

def set_bit(value, bit_pos, val):
    return (bit_unset(value, bit_pos), bit_set(value, bit_pos))[val == 1]

def show_text(header, text, method = "plain"):
    b_len = -1
    if isinstance(text, bytes):
        try:
            text = text.decode()
        except:
            b_len = len(text)
            text = text.hex(" ")
    
    char_op = lambda char: char
    if method == "bin":
        char_op = lambda char: convutils.get_bin(char, char_size)
    elif method == "hex":
        char_op = lambda char: convutils.get_hex(char)

    out = ""

    if (method == "plain"):
        out = text
    else:
        out = convutils.foreach_char(text, char_op)

    print(header + "\n" + out)
    
    if b_len == -1:
        print("[" + str(len(text)) + " символов]")
    else:
        print("[" + str(b_len) + " байт]")