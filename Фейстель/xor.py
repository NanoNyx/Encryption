import random

import convutils as util
from scrambler import Scrambler
from commons import *
import enc_commons as enc

max_out = 5

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

def xor_decrypt(msg, key):
    decyph_msg = ""
    i = 0
    for c_char in msg:
        char_num = ord(c_char)
        key_num = ord(key[i])
        
        decyph_char = char_num ^ key_num
        decyph_msg += chr(decyph_char)
        
        if i < max_out:
            print(get_bin(char_num) + " " + chr(char_num), end=" + ")
            print(get_bin(key_num) + " " + chr(key_num), end=" = ")
            print(get_bin(decyph_char) + " " + chr(decyph_char))
        elif i == max_out:
            print("...")
        
        i += 1

    return decyph_msg

def gen_random_key(length):
    key = ""
    for x in range(length):
        key += chr(random.getrandbits(char_size))
    return key

def gen_scrambler_key(scrambler, length):
    keychar_list = scrambler.next_sequence(length, char_size)
    key = ""
    for char_num in keychar_list:
        key += chr(char_num)
    
    return key

def xor_test(msg, key):
    show_text("Початкове повідомлення:", msg)
    show_text("Гама:", key)
    
    print("\nШифрування:")
    cypher_msg = xor_encrypt(msg, key)
    
    time = now()
    write("rand-key-" + str(time) + ".key", key)
    write("cyphertext-" + str(time) + ".txt", cypher_msg)
    
    print("\nДешифрування:")
    decyph_msg = xor_decrypt(cypher_msg, key)
    
    print("\nОтримане повідомлення:\n", decyph_msg, sep="\n")

def scr_test():
    br()
    print("скремблер")
    br()
    Scrambler.demo()
    nl()

def run_tests():
    global key
    scr_test()
    
    nl(); br()
    print("Гамування")
    br(); nl()
    xor_test(msg, key)
    
    nl(); br()
    print("Генерація гами скремблером (a)")
    br(); nl()
    
    key = gen_scrambler_key(Scrambler([7, 5, 2, 0], 99), len(msg))
    xor_test(msg, key)
    
    nl(); br()
    print("Генерація гами скремблером (б)")
    br(); nl()
    
    key = gen_scrambler_key(Scrambler([7, 1, 0], 25), len(msg))
    xor_test(msg, key)

def print_menu():
    print("msg [hex | bin] - показати повідомлення")
    print("key [hex | bin] - показати гаму")
    print("gen [length] - сгенерувати гаму довільним способом")
    print("scr - інформація про поточний скремблер")
    print("scr_gen - сгенерувати гаму поточним скремблером")
    print("scr_create [pow1 pow2 pow3 ... init_val] - створити скремблер із вказаних параметрів")
    print("scr_load file - завантажити скремблер із файла")
    print("scr_state [bin] int - встановити стан скремблера в десятичній або бінарній формі")
    print("scr_bench iters - провести тест скремблера в n ітерацій")
    print("scr_next [times] - провести n ітерацій скремблера")
    print("xor_encrypt - зашифрувати повідомлення поточною гамою")
    print("xor_decrypt - розшифрувати повідомлення поточною гамою")
    print("msg_load file - завантажити повідомлення")
    print("key_load file - завантажити ключ")
    print("msg_save [file] - зберегти повідомлення")
    print("key_save [file] - зберегти ключ")
    print("ls - показати всі файли ключів і повідомлень у папці")
    print("msg_set text - задати повідомлення вручну")
    print("<ENTER> - вихід")

def exec(cmd, tokens, has_args):
    if cmd == "xor_help":
        print_menu()
    
    elif cmd == "msg" or cmd == "key":
        is_msg = (cmd == "msg")
        show_text(("Ключ:", "Повідомлення:")[is_msg],
                  (enc.key, enc.msg)[is_msg],
                  tokens[1] if has_args else "plain")
        
    elif cmd == "scr":
        print("Інформація про скремблер:")
        enc.scrambler.print_scrambler_info()
        print("\nІнформація про поточний стан:")
        enc.scrambler.print_iteration_info()
    
    elif cmd == "scr_bench":
        print("Перевірка властивостей скремблера:")
        enc.scrambler.benchmark(int(tokens[1]))
        
    elif cmd == "scr_gen":
        enc.key = gen_scrambler_key(enc.scrambler, len(enc.msg))
        print("Генерація ключа скремблером завершена!")
        
    elif cmd == "scr_create":
        enc.scrambler = Scrambler.create_from_string(" ".join(tokens[1:]))
    
    elif cmd == "scr_load":
        enc.scrambler = Scrambler.create_from_string(read(tokens[1] + scr_ext))
        print("Скремблер завантажено!")
    
    elif cmd == "scr_state":
        state = int(tokens[1]) if tokens[1] != "bin" else int(tokens[2], 2)
        enc.scrambler.set_state(state);
        print("Стан скремблера змінено на", enc.scrambler.get_state())
        
    elif cmd == "msg_load":
        msg_file = tokens[1] + msg_ext
        enc.msg = read(msg_file)
        print("Повідомлення із " + msg_file + " завантажено!")
    
    elif cmd == "key_load":
        key_file = tokens[1] + key_ext
        enc.key = read(key_file)
        print("Ключ із " + key_file + " завантажено!")
    
    elif cmd == "ls":
        print("Всі повідомлення в поточній директорії:")
        list_files(msg_ext)
        
        print("\n\nВсе ключі в поточній директорії:")
        list_files(key_ext)
        
        print("\n\nВсе скремблери в поточній директорії:")
        list_files(scr_ext)
        nl()
        
    elif cmd == "key_save":
        key_file = (tokens[1] + key_ext) if has_args else (str(now()) + key_ext)
        write(key_file, enc.key)
        print("Ключ збережено в " + key_file)
    
    elif cmd == "msg_save":
        msg_file = (tokens[1] + msg_ext) if has_args else (str(now()) + msg_ext)
        write(msg_file, enc.msg)
        print("Повідомлення збережено в " + msg_file)
    
    elif cmd == "msg_set":
        enc.msg = " ".join(tokens[1:])
        print("Повідомлення задано!")
        
    elif cmd == "key_set":
        if tokens[1] != "hex":
            enc.key = (" ".join(tokens[1:])).replace("_", chr(0))
        else:
            enc.key = ""
            hex_chars = tokens[2:]
            for hex_char in hex_chars:
                enc.key += chr(int(hex_char, 16))
        print("Ключ задано!")
    
    elif cmd == "gen":
        if not has_args:
            enc.key = gen_random_key(len(enc.msg))
        else:
            enc.key = gen_random_key(int(tokens[1]))
        print("Сгенеровано новий ключ!")
    
    elif cmd == "scr_next":
        its = 1 if not has_args else int(tokens[1])
        for i in range(its):
            enc.scrambler.next_bit()
        print(its, "ітерацій скремблера закінчено!")
    
    elif cmd == "xor_encrypt":
        enc.msg = xor_encrypt(enc.msg, enc.key)
        print("Повідомлення зашифровано!")
    
    elif cmd == "xor_decrypt":
        enc.msg = xor_decrypt(enc.msg, enc.key)
        print("Повідомлення расшифровано!")
        
    elif cmd == "xor_test":
        br()
        run_tests()
        br()
    
    elif cmd == "scr_test":
        scr_test()

def init():
    global key, msg