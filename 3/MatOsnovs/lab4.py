#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import List, Tuple, Optional, Dict
import unicodedata

# ====== Глобальные настройки I/O (можно менять в меню) ======
DEFAULT_INPUT_MODE = "console"   # "console" или путь к файлу
DEFAULT_OUTPUT_MODE = "console"  # "console" или путь к файлу

# ====== Таблица замен (верхний регистр), Ё -> Е ======
RUS1 = "АБВГДЕЖЗИЙКЛМНОП"  # 16 букв: 10..25
RUS2 = "РСТУФХЦЧШЩЪЫЬЭЮЯ"   # 16 букв: 26..41
CODE_MAP: Dict[str, str] = {}   # 'А' -> '10', ...
DECODE_MAP: Dict[str, str] = {} # '10' -> 'А', ...
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
    # нормализация юникода + замена ё -> е + верхний регистр
    t = unicodedata.normalize("NFC", text)
    t = normalize_yo(t).upper()
    return t

# ====== Базовая математика (вручную) ======
def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Расширенный алгоритм Евклида: g, x, y такие, что a*x + b*y = g = gcd(a,b)."""
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
    """Обратный элемент a^{-1} mod m, если gcd(a,m)=1; иначе None."""
    g, x, _ = egcd(a, m)
    if g % m != 1 % m:  # допускаем g = -1 в экзотике
        return None
    return x % m

def modexp(base: int, exp: int, mod: int) -> int:
    """Быстрое (бинарное) возведение в степень по модулю."""
    base %= mod
    res = 1
    e = exp
    while e > 0:
        if e & 1:
            res = (res * base) % mod
        base = (base * base) % mod
        e >>= 1
    return res

# ====== Вспомогательные I/O ======
def choose_io_mode(kind: str = "input") -> str:
    """
    Выбор режима ввода/вывода:
      - цифры: 1=console, 2=file
      - слова: console/file/консоль/файл
    Возвращает "console" или путь к файлу.
    """
    while True:
        ans = input(f"Выберите режим {('ввода' if kind=='input' else 'вывода')} (1=console, 2=file): ").strip().lower()
        if ans in ("1", "console", "c", "консоль"):
            return "console"
        if ans in ("2", "file", "f", "файл"):
            path = input("Укажите путь к файлу: ").strip()
            return path
        print("Введите 1/2 или console/file.")

def read_text(src: Optional[str] = None) -> str:
    """
    Читает текст из консоли (многострочно до пустой строки) или файла (весь).
    Если src=None, берёт DEFAULT_INPUT_MODE. Если src='console' — консоль.
    Если src — путь, то читает из файла.
    """
    use = DEFAULT_INPUT_MODE if src is None else src
    if use == "console":
        print("Вводите текст (пустая строка — завершить):")
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
            print("Ошибка чтения файла:", e)
            return ""

def write_text(data: str, dest: Optional[str] = None) -> None:
    """Пишет строку либо в консоль, либо в файл. dest=None -> DEFAULT_OUTPUT_MODE."""
    use = DEFAULT_OUTPUT_MODE if dest is None else dest
    if use == "console":
        print("\n--- РЕЗУЛЬТАТ ---")
        print(data)
        print("------ КОНЕЦ ------\n")
    else:
        try:
            with open(use, "w", encoding="utf-8") as f:
                f.write(data)
            print(f"Сохранено в файл: {use}")
        except Exception as e:
            print("Ошибка записи файла:", e)

# ====== Кодирование/декодирование текста ======
def text_to_codes(text: str) -> str:
    """
    Преобразует текст в последовательность двузначных кодов без разделителей.
    Разрешенные символы: русские буквы (Ё->Е) и пробел; всё остальное отбрасывается.
    """
    t = to_upper_ru(text)
    digits = []
    for ch in t:
        if ch == " ":
            digits.append(SPACE_CODE)
        elif ch in CODE_MAP:
            digits.append(CODE_MAP[ch])
        # прочие символы пропускаем (знаки преп., цифры и т.п.)
    return "".join(digits)

def codes_to_text(digit_str: str) -> str:
    """
    Превращает слепленную строку цифр (кратную 2) обратно в текст.
    Каждые 2 цифры — код (10..41 или 99). Неизвестные коды игнорируются.
    """
    if len(digit_str) % 2 != 0:
        raise ValueError("Длина цифровой строки не кратна 2.")
    out = []
    for i in range(0, len(digit_str), 2):
        code = digit_str[i:i+2]
        ch = DECODE_MAP.get(code, None)
        if ch is not None:
            out.append(ch)
        # неизвестное — пропускаем
    return "".join(out)

# ====== Разбиение на блоки ======
def split_into_blocks(digit_str: str, n: int) -> Tuple[List[int], List[int]]:
    """
    Делит строку двузначных кодов на блоки M_i (целые числа) < n.
    Возвращает:
      blocks: список целых M_i,
      lengths: длина каждой M_i в ЦИФРАХ (для восстановления при расшифровке).
    Гарантируем отсутствие ведущих нулей (по нашей таблице они невозможны,
    но дополнительно проверяем).
    """
    blocks: List[int] = []
    lengths: List[int] = []
    cur = ""

    for i in range(0, len(digit_str), 2):
        pair = digit_str[i:i+2]
        # пробуем добавить двузначный код к текущему блоку
        candidate = cur + pair
        if candidate.startswith("0"):
            # на всякий — не должно случаться
            if cur:
                blocks.append(int(cur))
                lengths.append(len(cur))
                cur = pair  # начнём новый блок с пары (она не '00', т.к. коды 10..41/99)
            else:
                # если вдруг пара сама '00' (не бывает) — пропустим
                continue
        else:
            # если новый блок пуст — точно добавляем
            if not cur:
                if int(pair) >= n:
                    # одиночная пара уже >= n — невозможно корректно шифровать при таком n
                    raise ValueError(f"Слишком маленький модуль n={n}: код '{pair}' уже ≥ n.")
                cur = pair
            else:
                # проверим, не выходит ли за предел n
                if int(candidate) < n:
                    cur = candidate
                else:
                    # текущий блок завершён
                    blocks.append(int(cur))
                    lengths.append(len(cur))
                    # начинаем новый блок с текущей пары
                    if int(pair) >= n:
                        raise ValueError(f"Слишком маленький n={n}: код '{pair}' уже ≥ n.")
                    cur = pair

    # завершаем последний блок, если есть
    if cur:
        blocks.append(int(cur))
        lengths.append(len(cur))

    return blocks, lengths

def join_blocks_to_digits(M_blocks: List[int], lengths: List[int]) -> str:
    """
    Склеивает расшифрованные блоки M_i обратно в строку цифр, используя сохранённые длины.
    Никаких ведущих нулей мы не добавляем, но если длина M в цифрах меньше
    ожидаемой (теоретически не должно случиться), слева дополним нулями.
    """
    if len(M_blocks) != len(lengths):
        raise ValueError("Длины блоков и список блоков не совпадают.")
    parts: List[str] = []
    for M, L in zip(M_blocks, lengths):
        s = str(M)
        if s.startswith("0"):
            raise ValueError("Обнаружен блок с ведущим нулём.")
        if len(s) < L:
            s = s.zfill(L)  # на всякий случай
        parts.append(s)
    return "".join(parts)

# ====== RSA ключи ======
def pick_e(phi: int) -> int:
    """Пытаемся взять e=65537, иначе ищем ближайшее нечётное взаимно простое с phi."""
    if gcd(65537, phi) == 1:
        return 65537
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            return e
        e += 2
    raise ValueError("Не удалось подобрать e, взаимно простое с φ(n).")

def generate_key_pair(p: int, q: int, e_choice: Optional[int] = None) -> Tuple[int, int, int, int, int]:
    """
    Возвращает (n, phi, e, d, ok_flag) ; ok_flag=1 если d нашлось.
    """
    if p <= 1 or q <= 1:
        raise ValueError("p и q должны быть простыми > 1.")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = e_choice if e_choice is not None else pick_e(phi)
    if gcd(e, phi) != 1:
        raise ValueError(f"e={e} не взаимно просто с φ(n)={phi}.")
    d = modinv(e, phi)
    if d is None:
        raise ValueError("Не удалось найти d (обратный к e по φ(n)).")
    return n, phi, e, d, 1

# ====== Шифрование / Расшифрование ======
def rsa_encrypt_blocks(M_blocks: List[int], e: int, n: int) -> List[int]:
    return [modexp(M, e, n) for M in M_blocks]

def rsa_decrypt_blocks(C_blocks: List[int], d: int, n: int) -> List[int]:
    return [modexp(C, d, n) for C in C_blocks]

# ====== Меню и логика CLI ======
def set_io_modes():
    global DEFAULT_INPUT_MODE, DEFAULT_OUTPUT_MODE
    print("\n--- Режим ввода/вывода по умолчанию ---")
    DEFAULT_INPUT_MODE  = choose_io_mode("input")
    DEFAULT_OUTPUT_MODE = choose_io_mode("output")
    print(f"Установлено: ввод = {DEFAULT_INPUT_MODE}, вывод = {DEFAULT_OUTPUT_MODE}")

def menu_generate_keys(keys_store: List[dict]):
    """
    Генерация ≥3 пар ключей. Пользователь вводит 3 набора p,q (и опционально e).
    Пары сохраняются в keys_store.
    """
    print("\n--- Генерация ключей (не менее трёх пар) ---")
    keys_store.clear()
    count = 3
    for i in range(1, count + 1):
        print(f"\nПара #{i}:")
        while True:
            try:
                p = int(input("Введите p (простое): ").strip())
                q = int(input("Введите q (простое): ").strip())
                e_str = input("Введите e (Enter — подобрать автоматически): ").strip()
                e_val = int(e_str) if e_str else None
                n, phi, e, d, _ = generate_key_pair(p, q, e_val)
                keys_store.append({"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d})
                print(f"OK: n={n}, φ={phi}, e={e}, d={d}")
                break
            except Exception as ex:
                print("Ошибка:", ex)
    print("\nСписок сгенерированных ключей:")
    for idx, k in enumerate(keys_store, start=1):
        print(f"{idx}) (e,n)=({k['e']},{k['n']}), (d,n)=({k['d']},{k['n']})")

def select_key(keys_store: List[dict]) -> Optional[dict]:
    if not keys_store:
        print("Сначала сгенерируйте ключи (пункт 2).")
        return None
    print("\nВыберите ключ по номеру:")
    for idx, k in enumerate(keys_store, start=1):
        print(f"{idx}) e={k['e']}, d={k['d']}, n={k['n']} (p={k['p']}, q={k['q']})")
    while True:
        s = input("Номер ключа: ").strip()
        if not s.isdigit():
            print("Введите номер (цифрой).")
            continue
        i = int(s)
        if 1 <= i <= len(keys_store):
            return keys_store[i-1]
        print("Нет такого номера.")

def menu_encrypt(keys_store: List[dict]):
    """
    Шифрование строки:
      1) выбираем ключ (e,n),
      2) читаем текст (из настроенного по умолчанию источника или переопределяем),
      3) кодируем в двузначные, режем на блоки < n,
      4) шифруем каждый блок: C = M^e mod n,
      5) выводим: список C и список длины блоков (в цифрах).
    """
    print("\n--- Шифрование ---")
    key = select_key(keys_store)
    if not key:
        return
    # Откуда взять текст?
    override = input("Переопределить источник ввода? (1=console, 2=file, Enter=использовать по умолчанию): ").strip()
    src = None
    if override in ("1", "2", "console", "file", "консоль", "файл", "c", "f"):
        src = "console" if override in ("1", "console", "консоль", "c") else choose_io_mode("input") if override == "2" else "console"
        # если ввёл "2", уже спросили путь в choose_io_mode
        if override == "2":
            # choose_io_mode уже вернул путь к файлу
            pass
    text = read_text(src)
    if not text:
        print("Пустой ввод.")
        return
    e, n = key["e"], key["n"]

    # Кодируем и режем на блоки
    digit_str = text_to_codes(text)
    if not digit_str:
        print("Нет кодируемых символов (оставлены только русские буквы и пробел).")
        return
    try:
        M_blocks, lengths = split_into_blocks(digit_str, n)
    except Exception as ex:
        print("Ошибка разбиения на блоки:", ex)
        return

    # Шифруем
    C_blocks = rsa_encrypt_blocks(M_blocks, e, n)

    # Готовим вывод
    result_lines = []
    result_lines.append(f"(e, n) = ({e}, {n})")
    result_lines.append("C (шифр-блоки): " + " ".join(str(c) for c in C_blocks))
    result_lines.append("LEN (длины блоков, в цифрах): " + " ".join(str(L) for L in lengths))
    result_lines.append(f"Количество блоков: {len(C_blocks)}")
    out_data = "\n".join(result_lines)

    # Куда вывести?
    dest_override = input("Куда вывести? (1=console, 2=file, Enter=по умолчанию): ").strip()
    dest = None
    if dest_override in ("1", "2", "console", "file", "консоль", "файл", "c", "f"):
        dest = "console" if dest_override in ("1", "console", "консоль", "c") else choose_io_mode("output")
    write_text(out_data, dest)

def menu_decrypt(keys_store: List[dict]):
    """
    Расшифрование:
      1) выбираем ключ (d,n)
      2) читаем шифр-блоки и список длин (в цифрах)
      3) считаем M_i = C_i^d mod n
      4) склеиваем в строку цифр с учётом длин
      5) переводим по таблице в текст.
    """
    print("\n--- Расшифрование ---")
    key = select_key(keys_store)
    if not key:
        return
    d, n = key["d"], key["n"]

    # Источник шифртекста (C-блоки)
    overrideC = input("Источник C-блоков? (1=console, 2=file, Enter=по умолчанию): ").strip()
    srcC = None
    if overrideC in ("1", "2", "console", "file", "консоль", "файл", "c", "f"):
        srcC = "console" if overrideC in ("1", "console", "консоль", "c") else choose_io_mode("input")
    C_raw = read_text(srcC).strip()
    if not C_raw:
        print("Пустые C-блоки.")
        return
    try:
        C_blocks = [int(x) for x in C_raw.replace(",", " ").split()]
    except Exception:
        print("Не удалось распарсить C-блоки (ожидаются целые, через пробел/запятую).")
        return

    # Источник длин блоков
    overrideL = input("Источник длин блоков (LEN)? (1=console, 2=file, Enter=по умолчанию): ").strip()
    srcL = None
    if overrideL in ("1", "2", "console", "file", "консоль", "файл", "c", "f"):
        srcL = "console" if overrideL in ("1", "console", "консоль", "c") else choose_io_mode("input")
    L_raw = read_text(srcL).strip()
    if not L_raw:
        print("Пустые длины блоков.")
        return
    try:
        lengths = [int(x) for x in L_raw.replace(",", " ").split()]
    except Exception:
        print("Не удалось распарсить длины (ожидаются целые, через пробел/запятую).")
        return
    if len(lengths) != len(C_blocks):
        print("Количество длин не совпадает с количеством C-блоков.")
        return

    # Дешифруем блоки
    M_blocks = rsa_decrypt_blocks(C_blocks, d, n)

    # Склеиваем цифры и переводим в текст
    try:
        digit_str = join_blocks_to_digits(M_blocks, lengths)
        plaintext = codes_to_text(digit_str)
    except Exception as ex:
        print("Ошибка восстановления текста:", ex)
        return

    # Куда вывести?
    result = []
    result.append(f"(d, n) = ({d}, {n})")
    result.append("M (расшифр. блоки): " + " ".join(str(m) for m in M_blocks))
    result.append("Восстановленная цифровая строка: " + digit_str)
    result.append("ТЕКСТ (верхний регистр):")
    result.append(plaintext)
    out_data = "\n".join(result)

    dest_override = input("Куда вывести? (1=console, 2=file, Enter=по умолчанию): ").strip()
    dest = None
    if dest_override in ("1", "2", "console", "file", "консоль", "файл", "c", "f"):
        dest = "console" if dest_override in ("1", "console", "консоль", "c") else choose_io_mode("output")
    write_text(out_data, dest)

# ====== Главное меню ======
def main_menu():
    keys_store: List[dict] = []
    while True:
        print("\n=== RSA ===")
        print("1) Режим ввода/вывода по умолчанию")
        print("2) Генерация ≥3 пар ключей")
        print("3) Шифрование текста")
        print("4) Расшифрование текста")
        print("5) Выход")
        choice = input("Выбор (цифра или слово): ").strip().lower()
        if choice in ("1", "ввод", "вывод", "режим", "io", "i/o"):
            set_io_modes()
        elif choice in ("2", "генерация", "ключ", "ключи", "keys", "generate"):
            menu_generate_keys(keys_store)
        elif choice in ("3", "шифрование", "encrypt", "enc"):
            menu_encrypt(keys_store)
        elif choice in ("4", "расшифрование", "decrypt", "dec"):
            menu_decrypt(keys_store)
        elif choice in ("5", "выход", "exit", "quit", "q"):
            print("Пока!")
            break
        else:
            # Попробуем распознать чисто цифры 1..5
            if choice in ("1","2","3","4","5"):
                # рекурсивно запустить соответствующую ветку:
                if choice == "1":
                    set_io_modes()
                elif choice == "2":
                    menu_generate_keys(keys_store)
                elif choice == "3":
                    menu_encrypt(keys_store)
                elif choice == "4":
                    menu_decrypt(keys_store)
                elif choice == "5":
                    print("Пока!")
                    break
            else:
                print("Неизвестная команда. Введите цифру 1–5 или слово.")

if __name__ == "__main__":
    main_menu()
