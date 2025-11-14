#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Tuple, Optional, Dict
import unicodedata

# ====== Глобальные настройки I/O ======
DEFAULT_INPUT_MODE = "console"
DEFAULT_OUTPUT_MODE = "console"

# ====== Таблица замен (Ё -> Е) ======
RUS1 = "АБВГДЕЖЗИЙКЛМНОП"  # 10..25
RUS2 = "РСТУФХЦЧШЩЪЫЬЭЮЯ"   # 26..41
CODE_MAP: Dict[str, str] = {}
DECODE_MAP: Dict[str, str] = {}
for i, ch in enumerate(RUS1, start=10):
    CODE_MAP[ch] = f"{i}"
    DECODE_MAP[f"{i}"] = ch
for i, ch in enumerate(RUS2, start=26):
    CODE_MAP[ch] = f"{i}"
    DECODE_MAP[f"{i}"] = ch
SPACE_CODE = "99"
DECODE_MAP[SPACE_CODE] = " "

def normalize_yo(text: str) -> str:
    return text.replace("Ё", "Е").replace("ё", "е")

def to_upper_ru(text: str) -> str:
    t = unicodedata.normalize("NFC", text)
    t = normalize_yo(t).upper()
    return t

# ====== Евклид ======
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    x0, y0, x1, y1 = 1, 0, 0, 1
    a0, b0 = a, b
    while b0 != 0:
        q = a0 // b0
        a0, b0 = b0, a0 - q * b0
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a0, x0, y0

def gcd(a: int, b: int) -> int:
    a0, b0 = abs(a), abs(b)
    while b0 != 0:
        a0, b0 = b0, a0 % b0
    return a0

def modinv(a: int, m: int) -> Optional[int]:
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def modexp(base: int, exp: int, mod: int) -> int:
    base %= mod
    res = 1
    e = exp
    while e > 0:
        if e & 1:
            res = (res * base) % mod
        base = (base * base) % mod
        e >>= 1
    return res

# ====== I/O ======
def choose_io_mode(kind: str = "input") -> str:
    while True:
        ans = input(f"Режим {('ввода' if kind=='input' else 'вывода')} (1=console, 2=file): ").strip().lower()
        if ans in ("1", "console", "c", "консоль"):
            return "console"
        if ans in ("2", "file", "f", "файл"):
            return input("Путь к файлу: ").strip()
        print("Введите 1 или 2.")

def read_text(src: Optional[str] = None) -> str:
    use = DEFAULT_INPUT_MODE if src is None else src
    if use == "console":
        print("Текст (пустая строка — завершить):")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "":
                break
            lines.append(line)
        return "\n".join(lines)
    else:
        try:
            with open(use, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print("Ошибка чтения:", e)
            return ""

def write_text(data: str, dest: Optional[str] = None) -> None:
    use = DEFAULT_OUTPUT_MODE if dest is None else dest
    if use == "console":
        print("\n--- РЕЗУЛЬТАТ ---")
        print(data)
        print("------ КОНЕЦ ------\n")
    else:
        try:
            with open(use, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"Сохранено в: {use}")
        except Exception as e:
            print("Ошибка записи:", e)

# ====== Кодирование ======
def text_to_codes(text: str) -> str:
    t = to_upper_ru(text)
    digits = []
    for ch in t:
        if ch == " ":
            digits.append(SPACE_CODE)
        elif ch in CODE_MAP:
            digits.append(CODE_MAP[ch])
    return "".join(digits)

def codes_to_text(digit_str: str) -> str:
    if len(digit_str) % 2 != 0:
        raise ValueError("Длина строки нечётна.")
    out = []
    for i in range(0, len(digit_str), 2):
        ch = DECODE_MAP.get(digit_str[i:i+2])
        if ch is not None:
            out.append(ch)
    return "".join(out)

# ====== Восстановление длины блока ======
def infer_block_length(M: int, n: int) -> int:
    max_digits = len(str(n - 1))
    s_raw = str(M)
    if len(s_raw) > max_digits:
        raise ValueError(f"M={M} >= n={n}")
    candidates = []
    for L in range(len(s_raw), max_digits + 1):
        if L % 2 != 0:
            continue
        s = s_raw.zfill(L)
        if all(s[i:i+2] in DECODE_MAP for i in range(0, L, 2)):
            candidates.append(L)
    if not candidates:
        raise ValueError(f"Невозможно декодировать M={M}")
    return min(candidates)

def join_blocks_without_lengths(M_blocks: List[int], n: int) -> str:
    return "".join(str(M).zfill(infer_block_length(M, n)) for M in M_blocks)

# ====== Разбиение на блоки ======
def split_into_blocks(digit_str: str, n: int) -> List[int]:
    if n <= 99:
        raise ValueError("n должно быть > 99")
    blocks = []
    cur = ""
    for i in range(0, len(digit_str), 2):
        pair = digit_str[i:i+2]
        candidate = cur + pair
        if not cur:
            if int(pair) >= n:
                raise ValueError(f"n слишком мало: {pair} >= {n}")
            cur = pair
        else:
            if int(candidate) < n:
                cur = candidate
            else:
                blocks.append(int(cur))
                if int(pair) >= n:
                    raise ValueError(f"n слишком мало: {pair} >= {n}")
                cur = pair
    if cur:
        blocks.append(int(cur))
    return blocks

# ====== Генерация ключей ======
def pick_e(phi: int) -> int:
    if gcd(65537, phi) == 1:
        return 65537
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            return e
        e += 2
    raise ValueError("Не удалось подобрать e")

def generate_key_pair(p: int, q: int, e_choice: Optional[int] = None) -> Tuple[int, int, int, int]:
    if p <= 1 or q <= 1:
        raise ValueError("p и q должны быть > 1")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = e_choice if e_choice is not None else pick_e(phi)
    if gcd(e, phi) != 1:
        raise ValueError(f"e={e} не взаимно просто с φ={phi}")
    d = modinv(e, phi)
    if d is None:
        raise ValueError("Не удалось найти d")
    return n, e, d, phi

# ====== Шифрование / Расшифрование ======
def rsa_encrypt_blocks(M_blocks: List[int], e: int, n: int) -> List[int]:
    return [modexp(M, e, n) for M in M_blocks]

def rsa_decrypt_blocks(C_blocks: List[int], d: int, n: int) -> List[int]:
    return [modexp(C, d, n) for C in C_blocks]

# ====== Ввод ключей  ======
def get_encryption_params() -> Tuple[int, int]:
    print("Как задать открытый ключ?")
    print("1) Ввести p и q")
    print("2) Ввести e и n напрямую")
    choice = input("Ваш выбор (1/2): ").strip()
    if choice == "1":
        p = int(input("p = ").strip())
        q = int(input("q = ").strip())
        e_str = input("e (Enter — автоматически): ").strip()
        e_val = int(e_str) if e_str else None
        n, e, d, phi = generate_key_pair(p, q, e_val)
        print(f"→ Вычислено: n = {n}, e = {e}")
        return e, n
    elif choice == "2":
        e = int(input("e = ").strip())
        n = int(input("n = ").strip())
        if n <= 99:
            raise ValueError("n должно быть > 99")
        return e, n
    else:
        raise ValueError("Выберите 1 или 2")

def get_decryption_params() -> Tuple[int, int]:
    print("Как задать закрытый ключ?")
    print("1) Ввести p, q и e")
    print("2) Ввести d и n напрямую")
    choice = input("Ваш выбор (1/2): ").strip()
    if choice == "1":
        p = int(input("p = ").strip())
        q = int(input("q = ").strip())
        e = int(input("e = ").strip())
        n, e_check, d, phi = generate_key_pair(p, q, e)
        if e_check != e:
            print(f"  e={e} не подходит, использовано e={e_check}")
        print(f"→ Вычислено: n = {n}, d = {d}")
        return d, n
    elif choice == "2":
        d = int(input("d = ").strip())
        n = int(input("n = ").strip())
        if n <= 99:
            raise ValueError("n должно быть > 99")
        return d, n
    else:
        raise ValueError("Выберите 1 или 2")

# ====== Вспомогательные функции ======
def choose_override_source() -> Optional[str]:
    override = input("Изменить источник ввода? (1=console, 2=file, Enter=по умолчанию): ").strip()
    if override == "1":
        return "console"
    elif override == "2":
        return choose_io_mode("input")
    else:
        return None

def choose_override_dest() -> Optional[str]:
    override = input("Куда вывести? (1=console, 2=file, Enter=по умолчанию): ").strip()
    if override == "1":
        return "console"
    elif override == "2":
        return choose_io_mode("output")
    else:
        return None

# ====== Генерация ключей  ======
def menu_generate_keys(keys_store: List[dict]):
    print("\n--- Генерация ≥3 пар ключей ---")
    keys_store.clear()
    for i in range(1, 4):
        print(f"\nПара #{i}:")
        while True:
            try:
                p = int(input("p = ").strip())
                q = int(input("q = ").strip())
                e_str = input("e (Enter — автоматически): ").strip()
                e_val = int(e_str) if e_str else None
                n, e, d, phi = generate_key_pair(p, q, e_val)
                keys_store.append({"p": p, "q": q, "n": n, "e": e, "d": d})
                print(f" n={n}, e={e}, d={d}")
                break
            except Exception as ex:
                print("Ошибка:", ex)
    print("\nСгенерировано 3 пары.")

# ====== Шифрование ======
def menu_encrypt():
    print("\n--- Шифрование ---")
    try:
        e, n = get_encryption_params()
    except Exception as ex:
        print("Ошибка ввода ключа:", ex)
        return

    src = choose_override_source()
    text = read_text(src)
    if not text:
        print("Пустой ввод.")
        return

    digit_str = text_to_codes(text)
    if not digit_str:
        print("Нет кодируемых символов.")
        return

    try:
        M_blocks = split_into_blocks(digit_str, n)
        C_blocks = rsa_encrypt_blocks(M_blocks, e, n)
    except Exception as ex:
        print("Ошибка шифрования:", ex)
        return

    result = f"(e, n) = ({e}, {n})\nC: " + " ".join(map(str, C_blocks))
    dest = choose_override_dest()
    write_text(result, dest)

# ====== Расшифрование  ======
def menu_decrypt():
    print("\n--- Расшифрование ---")
    try:
        d, n = get_decryption_params()
    except Exception as ex:
        print("Ошибка ввода ключа:", ex)
        return

    overrideC = input("Источник C-блоков? (1=console, 2=file, Enter=по умолчанию): ").strip()
    srcC = "console" if overrideC == "1" else choose_io_mode("input") if overrideC == "2" else None
    C_raw = read_text(srcC).strip()
    if not C_raw:
        print("Пустые C-блоки.")
        return
    try:
        C_blocks = [int(x) for x in C_raw.replace(",", " ").split()]
    except Exception:
        print("Ошибка парсинга C-блоков.")
        return

    try:
        M_blocks = rsa_decrypt_blocks(C_blocks, d, n)
        digit_str = join_blocks_without_lengths(M_blocks, n)
        plaintext = codes_to_text(digit_str)
    except Exception as ex:
        print("Ошибка расшифрования:", ex)
        return

    result = f"(d, n) = ({d}, {n})\nТЕКСТ:\n{plaintext}"
    dest = choose_override_dest()
    write_text(result, dest)

# ====== Прочие меню ======
def set_io_modes():
    global DEFAULT_INPUT_MODE, DEFAULT_OUTPUT_MODE
    print("\n--- Режимы ввода/вывода ---")
    DEFAULT_INPUT_MODE = choose_io_mode("input")
    DEFAULT_OUTPUT_MODE = choose_io_mode("output")

# ====== Главное меню ======
def main_menu():
    keys_store = []  # используется только в пункте 2
    while True:
        print("\n=== RSA ===")
        print("1) Режим ввода/вывода")
        print("2) Генерация ≥3 пар ключей (опционально)")
        print("3) Шифрование текста")
        print("4) Расшифрование текста")
        print("5) Выход")
        choice = input("Выбор (1–5): ").strip()
        if choice == "1":
            set_io_modes()
        elif choice == "2":
            menu_generate_keys(keys_store)
        elif choice == "3":
            menu_encrypt() 
        elif choice == "4":
            menu_decrypt()
        elif choice == "5":
            print("Пока!")
            break
        else:
            print("Введите 1–5.")

if __name__ == "__main__":
    main_menu()