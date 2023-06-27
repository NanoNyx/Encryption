import math
from commons import *
from scrambler import Scrambler
import enc_commons as enc
import random

def bit_flip(bits, idx):
    if bits[idx] == 0:
        bits[idx] = 1
    else:
        bits[idx] = 0

def bin_dump(bits, delim = False):
    i = 0
    ret = ""
    for bit in bits:
        if delim and (i+1) % (char_size+1) == 0:
            ret += " "
            i = 0
        ret += str(bit)
        i += 1
    return ret

def int_to_bits(n):
    return [int(digit) for digit in bin(n)[2:]]

def bits_to_int(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out

def str_to_bits(string):
    return list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(char_size,'0') for i in string])))

def bits_to_str(bits: list):
    return "".join(chr(int("".join(map(str,bits[i:i+char_size])),2)) for i in range(0,len(bits),char_size))

def bit_pad(lst, to_len):
    ret = lst.copy()
    while len(ret) < to_len:
                ret.insert(0, 0)
    return ret

# Подключ по сдвигу i, длина = 32 бита
def subkey_a(key, i):
    subkey = []
    key_bits = str_to_bits(key)
    key_len = len(key_bits)
    for k in range(32):
        subkey.append(key_bits[(k + i) % key_len])
    return subkey

# Скремблер [8, 1, 0] с поч. станом = біти [i, i+8] ключа
# Ключ = 32 біта, сгенерованих скремблером
def subkey_b(key, i):
    scrambler = Scrambler([8, 1, 0])
    key_bits = str_to_bits(key)
    key_len = len(key_bits)
    
    s_bits = []
    for k in range(8):
        s_bits.append(key_bits[(k + i) % key_len])
    state = bits_to_int(s_bits)
    scrambler.set_state(state)
    return bit_pad(int_to_bits(scrambler.next_val(32)), 32)

def bit_xor(a, b):
    ret = []
    """if len(a) < len(b):
        a = bit_pad(a, len(b))
    elif len(b) < len(a):
        b = bit_pad(b, len(a))"""
    min_lst = a if len(a) < len(b) else b
    max_lst = b if len(a) < len(b) else a

    for i in range(len(min_lst)):
        ret.append(min_lst[i] ^ max_lst[i])
    
    #print(bin_dump(a), "+", bin_dump(b), "=", bin_dump(ret), sep="\n")
    
    return ret
        
# Одинична утворююча функція
def F_a(l: list, v: list):
    return v

# Утворююча функція -> S(L) (+) Vi
# Где S(L) - ліва частина блока (+) 32 біта із скремблера [16, 14, 1, 0]
def F_b(l: list, v: list):
    x = bit_pad(int_to_bits(Scrambler([16, 14, 1, 0], 1337).next_val(32)), 32)
    tmp_l = bit_xor(l.copy(), x)
    return bit_xor(tmp_l, v)

subkey_f = subkey_a
F = F_a

def get_F():
    global F
    return F.__name__

def get_V():
    global subkey_f
    return subkey_f.__name__

def diff(bits_a, bits_b):
    diff_c = 0
    for i in range(len(bits_a)):
        if bits_a[i] == bits_b[i]:
            diff_c += 1
    return diff_c

def feistel(encrypt, msg_bits, key, block_len = 64, rounds = 16):
    msg_len = len(msg_bits)
    block_c = math.ceil(msg_len / block_len)
    blocks = []
    
    print(bin_dump(msg_bits))
    
    i = 0
    while i < msg_len:
        if i + block_len < msg_len:
            blocks.append(msg_bits[i:i+block_len])
        else:
            blocks.append(msg_bits[i:msg_len])
            lb = blocks[block_c-1]
            if len(lb) % 2 != 0:
                lb.insert(0, 0)
        i += block_len
    
    cypher_msg = []
    bc = 1
    for b in blocks:
        r = b[0:len(b)// 2]
        l = b[len(b)//2:block_len]
        round_range = range(rounds) if encrypt else range(rounds-1, -1, -1)
        for rn in round_range:
            print("\nРаунд ", rn, " | Блок ", bc, "/", block_c, sep="")
            print("L: " + bin_dump(l) + " | R: " + bin_dump(r))
            subkey = subkey_f(key, rn)
            print("V"+str(rn)+" =", bin_dump(subkey))
            tmp = l
            l = bit_xor(F(l, subkey), r)
            r = tmp
            print("L<->R")
            print("L: " + bin_dump(l) + " | R: " + bin_dump(r))
            print("")
        b.clear()
        b.extend(l)
        b.extend(r)
        cypher_msg.extend(b)
        bc += 1

    print("Операція в " + str(rounds) + " раундів проведена успішно!")
    print("Оброблено " + str(msg_len) + " біт")
    print("[" + str(block_c) + " блоків по " + str(block_len) + " біт]")
    br()
    return bits_to_str(cypher_msg)

def print_menu():
    print("f_encrypt [rounds=16] [block_len=64] - зашифрувати поточне повідомлення")
    print("f_decrypt [rounds=16] [block_len=64] - дешифрувати поточне повідомлення")
    print("f_v [a|b] - змінити функцію раундового ключа")
    print("f_F [a|b] - змінити утворюючу функцію")
    print("f_avalanche [rounds=16] [blocks=1]- перевірити лавиний еффект зміною 1 біта повідомлення")
    print("f_info - вивести назву функції раундових ключів і утворюючу функцію")

def exec(cmd, tokens, has_args):
    global subkey_f, F
    
    if cmd == "f_help":
        print_menu()

    elif cmd == "f_encrypt" or cmd == "f_decrypt":
        _encrypt = (cmd == "f_encrypt")
        msg_bits = str_to_bits(enc.msg)
        if not has_args:
            enc.msg = feistel(_encrypt, msg_bits, enc.key)
        else:
            b_len = 64
            rounds = 16
            if len(tokens) > 1:
                rounds = int(tokens[1])
            if len(tokens) > 2:
                b_len = int(tokens[2])
            enc.msg = feistel(_encrypt, msg_bits, enc.key, b_len, rounds)
        print("[", get_F(), get_V(), "]")
    
    elif cmd == "f_info":
        print("[", get_F(), get_V(), "]")
    
    elif cmd == "f_avalanche":
        b_len = 64
        blocks = 1
        if not has_args:
            rounds = 16
        else:
            rounds = int(tokens[1])
        if len(tokens) > 2:
            blocks = int(tokens[2])

        msg_bits = str_to_bits(enc.msg)[0:blocks * b_len]
        enc_orig = feistel(True, msg_bits, enc.key, b_len, rounds)
        flip_idx = random.randint(0, len(msg_bits)-1)
        bit_flip(msg_bits, flip_idx)
        enc_mod = feistel(True, msg_bits, enc.key, b_len, rounds)
        print("Перевірка лавиного еффекта після", rounds, "раундів в", blocks, "блоках")
        print("Змінено біт #", flip_idx, "поточного повідомлення")
        print("Загальна довжина повідомлення:", len(msg_bits), "бит")
        bit_diff = diff(enc_orig, enc_mod)
        print("Відмінність:", bit_diff, " біт ("
              + str((bit_diff / len(msg_bits)) * 100) + "%)")
    
    elif cmd == "f_v":
        subkey_f = subkey_a if tokens[1] == "a" else subkey_b
        print("Функція раундового ключа змінена на " + tokens[1])
    
    elif cmd == "f_F":
        F = F_a if tokens[1] == "a" else F_b
        print("Утворююча функція змінена на " + tokens[1])
        
            

def init():
    enc.scrambler = Scrambler([8, 1, 0])