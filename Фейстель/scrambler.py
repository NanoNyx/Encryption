import random

from commons import *
from convutils import *

class Scrambler:
    def __init__(self, poly_pows, init_val = -1):
        self.iteration = 0
        self.poly_bits = 0
        
        max_pow = poly_pows[0] - 1
        i = max_pow
        for p in range(max_pow, -1, -1):
            self.poly_bits = set_bit(self.poly_bits, i, int(p in poly_pows))
            i -= 1
        
        self.t = max_pow + 1
        self.init_val = (init_val, random.getrandbits(self.t))[init_val == -1]
        self.state = self.init_val
    
    def _next_state(self):
        res_bit = 0
        for i in range(self.t):
            res_bit += get_bit(self.state, i + 1) * get_bit(self.poly_bits, i + 1)
        res_bit %= 2

        self.state = set_bit(self.state >> 1, self.t - 1, res_bit)
        return self.state
    
    def get_state(self):
        return get_bin(self.state, self.t)
    
    def get_current_bit(self):
        return get_bit(self.state, 1)
    
    def next_bit(self) -> int:
        self.iteration += 1
        self._next_state()
        return self.get_current_bit()
    
    def set_state(self, new_state):
        self.init_val = new_state
        self.state = new_state
        self.iteration = 0
    
    def next_val(self, bits) -> int:
        gen_num = 0
        for i in range(bits):
            gen_num = set_bit(gen_num, i, self.next_bit())
        
        return gen_num
    
    def next_sequence(self, seq_len, elem_len) -> list:
        gen_seq = []
        for i in range(seq_len):
            gen_seq.append(self.next_val(elem_len))
        
        return gen_seq
    
    def shuffle(self):
        its = random.randint(1, (pow(2, self.t) - 1) // 2)
        for i in range(its):
            self.next_bit()
        return its
    
    def print_scrambler_info(self):
        print("N = " + str(self.t))
        print("Початковий стан: " + get_bin(self.init_val, self.t)
            + " (" + str(self.init_val) + ")")
        print("Поліном: " + get_bin(self.poly_bits, self.t))
    
    def print_iteration_info(self):
        print("#" + str(self.iteration))
        print("Стан: " + self.get_state())
        print("Новий біт: " + str(self.get_current_bit()))
    
    def get_period(self):
        self.set_state(self.init_val)
        new_state = self._next_state()
        t = 1
        max_it = pow(2, self.t) - 1

        while new_state != self.init_val:
            new_state = self._next_state()
            t += 1
            if t >= max_it:
                break

        return t
    
    def benchmark(self, its):
        print("Розрядність N =", self.t)
        print("Максимальна кількість ітерацій до зациклювання:",
              pow(2, self.t) - 1)
        print("Фактичний період при початковому стані [", self.init_val,
              "] T =", self.get_period())
        print("Результати теста в", its, "ітерацій:\n")
        cycle_map = {}
        zs = 0
        os = 0
        
        prev_bit = -1
        bit_comb_len = 0
        total_combs = 0
        new_bit = 0
        set1 = []
        for i in range(its):
            new_bit = self.next_bit()
            set1.append(new_bit)
            print(new_bit, sep="", end="")
            
            if prev_bit == -1:
                prev_bit = new_bit
            
            if prev_bit == new_bit:
                bit_comb_len += 1
            else:
                cycle_map[bit_comb_len] = cycle_map.get(bit_comb_len, 0) + 1
                bit_comb_len = 1
                total_combs += 1
            
            if new_bit == 1:
                os += 1
            else:
                zs += 1
            
            prev_bit = new_bit
        cycle_map[bit_comb_len] = cycle_map.get(bit_comb_len, 0) + 1
        total_combs += 1
        
        expected = its / 2
        hi_sqr = (pow(zs - expected, 2) / expected) + (pow((os - expected), 2) / expected)
        print("\n\nЗначення X^2 =", hi_sqr)
        if hi_sqr > 3.841:
            print("Вище критичного при p=0.05")
        else:
            print("Нижче критичного при p=0.05")

        print("\nСбалансованність:")
        print("Нулів:", zs, str((zs / its) * 100) + "%")
        print("Одиниць:", os, str((os / its) * 100) + "%")
        print("Різниця:", str((abs(os - zs) / its) * 100) + "%")
        
        print("\nЦиклічність:")
        for comb_len, count in cycle_map.items():
            print(count, str((count / total_combs) * 100) + "%",
                  "циклів довжиною", comb_len, "біт")
        
        eq = 0
        neq = 0
        n_bit = 0
        shf = self.shuffle()
        print("\n\nКореляция (зсув в", shf, "біт)\n")
        for i in range(its):
            n_bit = self.next_bit()
            if n_bit == set1[i]:
                eq += 1
            else:
                neq += 1
            print(n_bit, sep="", end="")
        print("\n\nСпівпадіння:", eq)
        print("Неспівпадіння:", neq)
        print("Різниця:", str((abs(eq - neq) / its) * 100) + "%")
        
    def create_from_string(scr_str):
        tokens = scr_str.split(" ")
        if scr_str:
            pow_list = [int(pow_str) for pow_str in tokens[:len(tokens) - 1]]
            init_val = int(tokens[len(tokens) - 1])
            
            print("Створюємо скремблер за степенями:")
            for p in pow_list:
                print(p, end=" ")
            print("")
            
            return Scrambler(pow_list, init_val)
        else:
            return Scrambler.create_random(True)
    
    def create_random(verbose = False):
        sample = range(3, random.randrange(5, 17))
        pows = random.sample(sample, random.randrange(1, len(sample)))
        pows.sort(reverse=True)
        
        if verbose:
            print("Сгенеровано довільний скремблер:")
            for p in pows:
                print(int(p), end=" ")
            print("")
        
        return Scrambler(pows)
    
    def demo():
        print("Демонстрація на умові із прикладу:")
        scrambler = Scrambler([7, 6, 2], 79)
        scrambler.print_scrambler_info()
        scrambler.benchmark(100)
        
        scrambler.set_state(79)
        print("\nПерші 9 ітерацій:")
        for i in range(9):
            print("")
            scrambler.next_bit()
            scrambler.print_iteration_info()