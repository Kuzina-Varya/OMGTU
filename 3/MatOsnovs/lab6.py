#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def isqrt(m: int) -> int:
    """
    Целочисленный квадратный корень: наибольшее h, такое что h^2 <= m.
    Реализация по алгоритму из задания.
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

def gcd(a: int, b: int) -> int:
    """НОД двух чисел (алгоритм Евклида)."""
    while b:
        a, b = b, a % b
    return abs(a)

def build_residues(mod: int) -> list:
    """
    Строит список квадратичных вычетов по модулю mod.
    Возвращает список длины mod: True — вычет, False — невычет.
    """
    residues = [False] * mod
    for x in range(mod):
        residues[(x * x) % mod] = True
    return residues

def quadratic_sieve_factor(m: int) -> tuple:
    """
    Факторизация методом квадратичного решета.
    Запрашивает у пользователя три модуля a, b, c.
    """
    print(f"\n=== Метод квадратичного решета для m = {m} ===")
    
    # Запрос модулей
    a = int(input("Введите модуль a : "))
    b = int(input("Введите модуль b : "))
    c = int(input("Введите модуль c : "))
    mods = [a, b, c]
    
    # Шаг 1: построить решета (квадратичные вычеты)
    print("\nШаг 1: Построение квадратичных решет (вычетов)...")
    sieves = {}
    for mod in mods:
        residues = build_residues(mod)
        print(f"Модуль {mod}: вычеты = {[i for i, r in enumerate(residues) if r]}")
        sieves[mod] = residues

    # Шаг 2: определить интервал [start, end]
    sqrt_m = isqrt(m)
    start = sqrt_m + 1
    end = (m + 1) // 2
    print(f"\nШаг 2: Интервал поиска x: от {start} до {end}")
    
    # Определим смещения для каждого решета
    offsets = {}
    for mod in mods:
        offsets[mod] = start % mod
        print(f"Начало наложения решета по модулю {mod}: позиция {offsets[mod]}")

    # Шаг 3: перебираем x, ищем z = x^2 - m — полный квадрат
    print("\nШаг 3: Поиск x, для которого z = x^2 - m — полный квадрат...")
    x = start
    max_check = min(start + 500, end)  # чтобы не зависло на больших m
    while x <= max_check:
        # Проверка по решетам: z = x^2 - m должно быть вычетом по всем модулям
        z = x * x - m
        valid = True
        for mod in mods:
            z_mod = z % mod
            pos = (x - start + offsets[mod]) % mod  # смещение
            # проверить, является ли z_mod квадратичным вычетом
            if not sieves[mod][z_mod]:
                valid = False
                break
        if valid:
            # Проверяем, является ли z полным квадратом
            y = isqrt(z)
            if y * y == z:
                print(f"\nНайдено! x = {x}, z = {z} = {y}^2")
                p = x + y
                q = x - y
                if p * q == m:
                    print(f"Делители: p = {p}, q = {q}")
                    return p, q
                else:
                    print("Ошибка: p * q != m")
        x += 1

    raise ValueError("Факторизация методом квадратичного решета не удалась")

def rho_pollard_factor(m: int) -> int:
    """
    ρ-метод факторизации Полларда.
    Возвращает найденный делитель d (1 < d < m).
    """
    print(f"\n=== ρ-метод факторизации для m = {m} ===")
    
    x0_1 = int(input("Введите начальное значение x0 для первой последовательности: "))
    x0_2 = int(input("Введите начальное значение x0 для второй последовательности: "))
    
    def f(x):
        return (x * x + 1) % m

    x1 = x0_1
    x2 = x0_2
    n = 0
    print(f"\nШаги алгоритма:")
    print(f"{'n':>2} {'x1':>8} {'x2':>8} {'|x1-x2|':>10} {'НОД':>6}")
    
    while True:
        x1 = f(x1)
        x2 = f(f(x2))
        n += 1
        diff = abs(x1 - x2)
        d = gcd(diff, m)
        print(f"{n:2} {x1:8} {x2:8} {diff:10} {d:6}")
        if 1 < d < m:
            print(f"\nНайден делитель на шаге {n}: d = {d}")
            return d
        if n > 1000:  # защита от бесконечного цикла
            raise ValueError("ρ-метод не сошёлся за 1000 шагов")

def main():
    print("Лабораторная работа: Факторизация чисел")
    print("========================================")
    
    m = int(input("Введите число m для факторизации: "))
    if m <= 1:
        print("Ошибка: m должно быть > 1")
        return

    print("\nВыберите метод факторизации:")
    print("1. Метод квадратичного решета")
    print("2. ρ-метод Полларда")
    choice = input("Ваш выбор (1/2): ").strip()

    try:
        if choice == "1":
            p, q = quadratic_sieve_factor(m)
            print(f"\n Результат: {m} = {p} × {q}")
        elif choice == "2":
            d = rho_pollard_factor(m)
            p = d
            q = m // d
            print(f"\n Результат: {m} = {p} × {q}")
        else:
            print("Неверный выбор.")
    except Exception as e:
        print(f"\n Ошибка: {e}")

if __name__ == "__main__":
    main()