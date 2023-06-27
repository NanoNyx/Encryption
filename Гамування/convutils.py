def get_bin(val: int, n = -1) -> str:
    if n == -1:
        n = val.bit_length()

    return format(val, 'b').zfill(n)

def get_hex(val: int) -> str:
    return hex(val)[2:]

def foreach_char(text, operation):
    ret = ""
    for char in text:
        ret += operation(ord(char)) + " "
    return ret