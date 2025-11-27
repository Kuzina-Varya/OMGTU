#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def isqrt(m: int) -> int:
    """Целочисленный квадратный корень: наибольшее h, такое что h^2 <= m."""
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

def modexp(base: int, exp: int, mod: int) -> int:
    """Быстрое возведение в степень по модулю."""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result

def baby_step_giant_step(a: int, b: int, p: int) -> int:
    """Решает a^x ≡ b (mod p) методом 'шаг младенца – шаг великана'."""
    print(f"\nРешаем уравнение: {a}^x ≡ {b} (mod {p})")
    
    # Шаг 1: k = floor(sqrt(p)) + 1
    k = isqrt(p) + 1
    print(f"1. Вычисляем k = ⌊√{p}⌋ + 1 = {isqrt(p)} + 1 = {k}")

    # Шаг 2: Baby steps — z_j = b * a^j mod p, j = 0, 1, ..., k-1
    print("\n2. Выполняем 'шаги младенца' (строим таблицу z_j = b * a^j mod p)...")
    baby = {}
    a_j = 1  # a^0
    for j in range(k):
        z = (b * a_j) % p
        if z not in baby:  # сохраняем наименьший j
            baby[z] = j
        a_j = (a_j * a) % p  # a^(j+1)

    print(f"   Построено {len(baby)} уникальных значений z_j.")

    # Шаг 3: Giant steps — y_i = (a^k)^i mod p, i = 0, 1, ..., k
    print("\n3. Выполняем 'шаги великана' (ищем совпадение с таблицей z_j)...")
    a_k = modexp(a, k, p)  # a^k mod p
    y = 1  # (a^k)^0 = 1
    for i in range(k + 1):
        if y in baby:
            j = baby[y]
            x = i * k - j
            print(f"\n Найдено совпадение: y_{i} = z_{j} = {y}")
            print(f"   Вычисляем x = i * k - j = {i} * {k} - {j} = {x}")
            
            # Проверка
            check = modexp(a, x, p)
            print(f"   Проверка: {a}^{x} mod {p} = {check}")
            if check == b % p:
                return x
            else:
                raise RuntimeError("Ошибка: проверка не пройдена")
        y = (y * a_k) % p  # y = (a^k)^(i+1)

    raise ValueError("Решение не найдено. Возможно, дискретный логарифм не существует.")

def main():
    
    print("Метод 'шаг младенца – шаг великана'\n")
    
    # Ввод данных с консоли
    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    p = int(input("Введите p: "))

    if p <= 1:
        print("Ошибка: p должно быть > 1")
        return

    try:
        x = baby_step_giant_step(a, b, p)
        print(f"\n Ответ: x = {x}")
    except Exception as e:
        print(f"\n Ошибка: {e}")

if __name__ == "__main__":
    main()