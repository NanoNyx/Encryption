from random import randrange, getrandbits, randint
from time import time


def is_prime(n, k=128):

    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True

def generate_prime_candidate(length):
    """ Generate an odd integer randomly        Args:
            length -- int -- the length of the number to generate, in bits        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=64):

    p = 4
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


def powmod(a: int, b: int, p: int):
    res = 1
    while (b != 0):
        if (b & 1):
            res = res * a % p
            b -= 1
        else:
            a = a * a % p
            b >>= 1
    return res

def primRoots(p: int, max_roots = 1):
    rn = 0
    roots = []

    fact = []
    phi = p - 1
    n = phi
    i = 2
    while i * i <= n:
        if (n % i == 0):
            fact.append(i)
            while (n % i == 0):
                n //= i
        i += 1
    if (n > 1):
        fact.append(n)

    for res in range(2, p + 1):
        ok = True
        i = 0
        while i < len(fact) and ok:
            ok &= powmod(res, phi // fact[i], p) != 1
            i += 1
        if (ok):
            roots.append(res)
            rn += 1
            if rn >= max_roots:
                return roots

    return -1

def DH(n, g):
    #t1 = time()
    Xa = randint(1,n-1)
    #t2 = time()
    print('Абонент А сгенерував випадкову секретну величину X =', Xa)
    #print('Витрачений час: t =', t2-t1)
    #t1 = time()
    Ya = powmod(g, Xa, n)
    #t2 = time()
    print('Абонент А розрахував відкриту величину Y =', Ya)
    #print('Витрачений час: t =', t2-t1)
    #t1 = time()
    Xb = randint(1,n-1)
    #t2 = time()
    print('Абонент B сгенерував випадкову секретну величину X =', Xb)
    #print('Витрачений час: t =', t2-t1)
    #t1 = time()
    Yb = powmod(g,Xb, n)
    #t2 = time()
    print('Абонент B розрахував відкриту величину Y =', Yb)
    #print('Витрачений час: t =', t2-t1)
    #t1 = time()
    A = powmod(Yb, Xa, n)
    #t2 = time()
    print('Обмін елементами по каналу зв_язку...')
    print('Абонент А визначив секретний ключ K =', A)
    #print('Витрачений час: t =', t2-t1)
    #t1 = time()
    B = powmod(Ya, Xb, n)
    #t2 = time()
    print('Абонент B визначив секретний ключ K =', B)
    #print('Витрачений час: t =', t2-t1)

def main():
    t1 = time()
    n = generate_prime_number()
    t2 = time()
    print('Лабораторна робота №5')
    print('Обмін ключами за схемою Диффи-Хеллмана')
    print('Генерація простого числа n =', n)
    print('Витрачений час: t =', t2-t1)
    t1 = time()
    g = primRoots(n)
    t2 = time()
    print('Первісний корінь g =', g)
    print('Витрачений час: t =', t2-t1)
    DH(n, min(g))

if __name__ == '__main__':
    main()