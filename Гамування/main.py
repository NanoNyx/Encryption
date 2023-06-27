import time
import calendar
import random

import convutils as util
from scrambler import Scrambler

max_out = 10
char_size = 8
line_delim = "*" * 50
key_ext = ".key"
msg_ext = ".txt"
scr_ext = ".scr"

now = lambda: calendar.timegm(time.gmtime())
get_bin = lambda x, n = char_size: util.get_bin(x, n)
br = lambda: print(line_delim)
nl = lambda: print("")

# Возвращает содержимое файла
def read(file):
    with open(file) as f:
        return f.read()

# Записывает text в файл file
def write(file, text):
    with open(file, "w") as f:
        f.write(text)

# Гаммирование сообщения msg ключом key
def xor_encrypt(msg, key):
    cypher_msg = ""
    i = 0
    for char in msg:
        char_num = ord(char)
        key_num = ord(key[i])
    
        cypher_char = char_num ^ key_num
        cypher_msg += chr(cypher_char)
        
        if i < max_out:
            print(get_bin(char_num) + " " + chr(char_num), end=" + ")
            print(get_bin(key_num) + " " + key[i], end=" = ")
            print(get_bin(cypher_char) + " " + chr(cypher_char))
        elif i == max_out:
            print("...")
        
        i += 1

    return cypher_msg

# Дешифрование гаммированием
def xor_decrypt(msg, key):
    return xor_encrypt(msg, key)

# Генерация случайного ключа длиной length символов
def gen_random_key(length):
    key = ""
    for x in range(length):
        key += chr(random.getrandbits(char_size))
    return key

# Генерация ключа длины length скремблером scrambler
def gen_scrambler_key(scrambler, length):
    keychar_list = scrambler.next_sequence(length, char_size)
    key = ""
    for char_num in keychar_list:
        key += chr(char_num)
    
    return key

# Обертка для отображения текста в разных представлениях (2, 16, чистый текст)
# +отображает длину текста
def show_text(header, text, method = "plain"):
    char_op = lambda char: char
    if method == "bin":
        char_op = lambda char: util.get_bin(char, char_size)
    elif method == "hex":
        char_op = lambda char: util.get_hex(char)

    out = ""

    if (method == "plain"):
        out = text
    else:
        out = util.foreach_char(text, char_op)

    print(header + "\n"
      + out
      + "\n(" + str(len(text)) + " символів)")


##########
#
# Чтение сообщения из файла
msg = read("msg.txt")
show_text("Початкове повідомлення:", msg, "plain")

# Случайный ключ по длине сообщения
key = gen_random_key(len(msg))

#write("key.txt", key)

# Скремблер x^8 + x^7 + x^6 + x^3 + x^2 + 1 с начальным состоянием 10
scrambler = Scrambler([8, 7, 6, 3, 2, 1], 10)
scrambler.print_scrambler_info()
#свойства скремблера

#scrambler.benchmark(it)

# it -- количество итераций прогонки скремблера, желательно что бы было чуть больше
# (2^N)-1 где N - старшая степень полинома скремблера

# Генерация ключа скремблером
scr_key = gen_scrambler_key(scrambler, len(msg))

# Шифрование по случайному ключу
print("\nШифрування:")
cr_msg = xor_encrypt(msg, key)
show_text("\nЗашифроване повідомлення:", cr_msg, "plain")

#write("cr_m.txt", cr_msg)

# Шифрование ключом, сгенерированным скремблером
print("\nШифрування скремблером")
cs_msg = xor_encrypt(msg, scr_key)
show_text("\nЗашифроване повідомлення (скремблер):", cs_msg, "plain")

#write("cs_m.txt", cs_msg)

# Дешифрование случайным ключом
print("\nДешифрування")
dr_msg = xor_decrypt(cr_msg, key)
show_text("\nРозшифроване повідомлення:", dr_msg, "plain")

#write("dr_m.txt", dr_msg)

# Дешифрование ключом, сгенерированным скремблером
print("\nДешифрування скремблером")
sr_msg = xor_decrypt(cs_msg, scr_key)
show_text("\nРозшифроване повідомлення (скремблер):", sr_msg, "plain")

#write("sr_m.txt", sr_msg)

#
##########
