#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Tuple

# ====== Алгоритм целочисленного квадратного корня (по заданию) ======
def isqrt(m: int) -> int:
    """
    Возвращает h = floor(sqrt(m)), где h^2 <= m < (h+1)^2.
    Алгоритм из задания: итерации x_{k+1} = floor((x_k + floor(m/x_k)) / 2)
    """
    if m < 0:
        raise ValueError("m должно быть неотрицательным")
    if m == 0:
        return 0
    x = m
    while True:
        y = (x + m // x) // 2
        if y < x:
            x = y
        else:
            return x

# ====== НОД (алгоритм Евклида) ======
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a if a >= 0 else -a

# ====== Факторизация методом пробных делений (строго по заданию) ======
def trial_division_factor(n: int) -> Tuple[int, int]:
    """
    Факторизует n = p * q, используя метод пробных делений из задания:
    1. Выделяем степени 2 и 3.
    2. Вычисляем B = floor(sqrt(n)) с помощью isqrt.
    3. Генерируем все простые <= B.
    4. Применяем метод триплетов с НОД.
    5. Если не разложили — перебираем простые по одному.
    """
    original_n = n
    factors = []

    # 1. Выделяем степени 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # 2. Выделяем степени 3
    while n % 3 == 0:
        factors.append(3)
        n //= 3

    if n == 1:
        if len(factors) < 2:
            raise ValueError("n не может быть разложено на два множителя")
        p = 1
        for f in factors[:-1]:
            p *= f
        q = factors[-1]
        return p, q

    # 3. Вычисляем B = floor(sqrt(n)) — используем ВАШ алгоритм
    B = isqrt(n)

    # 4. Генерируем все простые числа от 2 до B (решето Эратосфена)
    if B < 2:
        primes = []
    else:
        sieve = [True] * (B + 1)
        sieve[0] = sieve[1] = False
        # Используем isqrt и здесь, как того требует логика
        limit_sieve = isqrt(B)
        for i in range(2, limit_sieve + 1):
            if sieve[i]:
                for j in range(i * i, B + 1, i):
                    sieve[j] = False
        primes = [i for i in range(2, B + 1) if sieve[i]]

    # Убираем 2 и 3 — они уже обработаны
    primes = [p for p in primes if p >= 5]

    # 5. Метод триплетов (произведения трёх подряд идущих простых)
    i = 0
    while i <= len(primes) - 3:
        p1, p2, p3 = primes[i], primes[i+1], primes[i+2]
        qs = p1 * p2 * p3
        if qs > original_n:
            break

        while n > 1:
            d = gcd(n, qs)
            if d == 1:
                break
            # Разлагаем d на p1, p2, p3
            for p in (p1, p2, p3):
                while d % p == 0:
                    factors.append(p)
                    n //= p
                    d //= p
                    if n == 1:
                        break
                if n == 1:
                    break
            if n == 1:
                break
        if n == 1:
            break
        i += 3

    # 6. Если n > 1 — перебираем все простые по одному (классический метод пробных делений)
    if n > 1:
        for p in primes:
            if p > isqrt(n):  # снова ваш isqrt!
                break
            while n % p == 0:
                factors.append(p)
                n //= p
                if n == 1:
                    break
            if n == 1:
                break
        if n > 1:
            factors.append(n)

    # Собираем два множителя (предполагаем, что original_n = p * q)
    if len(factors) == 2:
        return factors[0], factors[1]
    elif len(factors) > 2:
        p = 1
        for f in factors[:-1]:
            p *= f
        q = factors[-1]
        return p, q
    else:
        raise ValueError(f"Не удалось факторизовать n = {original_n}")

# ====== RSA: расширенный алгоритм Евклида и возведение в степень ======
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    g, x1, y1 = egcd(b % a, a)
    return g, y1 - (b // a) * x1, x1

def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m

def modexp(base: int, exp: int, mod: int) -> int:
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

# ====== Декодирование текста ======
DECODE_MAP = {}
RUS1 = "АБВГДЕЖЗИЙКЛМНОП"  # 10–25
RUS2 = "РСТУФХЦЧШЩЪЫЬЭЮЯ"  # 26–41
for i, ch in enumerate(RUS1, 10):
    DECODE_MAP[f"{i}"] = ch
for i, ch in enumerate(RUS2, 26):
    DECODE_MAP[f"{i}"] = ch
DECODE_MAP["99"] = " "

def codes_to_text(digit_str: str) -> str:
    if len(digit_str) % 2 != 0:
        digit_str = "0" + digit_str  # компенсация, если нужно
    text = []
    for i in range(0, len(digit_str), 2):
        code = digit_str[i:i+2]
        text.append(DECODE_MAP.get(code, "?"))
    return "".join(text)

def decrypt_rsa_blocks(C_blocks: List[int], d: int, n: int) -> str:
    digit_str = ""
    for c in C_blocks:
        m = modexp(c, d, n)
        # Предполагаем, что каждый блок — двузначный код 
        if m < 100:
            digit_str += f"{m:02d}"
        else:
            # Если блок длиннее — добавляем как есть 
            digit_str += str(m)
    return digit_str

# ====== Основная программа ======
def main():
    print("=== Атака на RSA: факторизация модуля ===")
    print("Реализованы два алгоритма из задания:\n")

    try:
        e = int(input("Введите e: ").strip())
        n = int(input("Введите n: ").strip())
        cipher_input = input("Введите C-блоки (через пробел или запятую): ").strip()
        if not cipher_input:
            raise ValueError("Пустой ввод C-блоков")
        cipher_input = cipher_input.replace(",", " ")
        C_blocks = [int(x) for x in cipher_input.split()]

        print(f"\nФакторизация n = {n} ...")
        p, q = trial_division_factor(n)
        print(f" Найдено: p = {p}, q = {q}")
        if p * q != n:
            print("  Внимание: p * q != n")

        phi = (p - 1) * (q - 1)
        d = modinv(e, phi)
        print(f" Закрытый ключ d = {d}")

        plaintext = decrypt_rsa_blocks(C_blocks, d, n)
        print(f"\n--- РАСШИФРОВАННЫЙ ТЕКСТ ---\n{plaintext}\n{'-' * 32}")

    except Exception as ex:
        print(f"\n Ошибка: {ex}")

if __name__ == "__main__":
    main()