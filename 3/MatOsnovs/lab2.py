#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from datetime import datetime
from typing import Optional, Tuple, List
import unicodedata

# ---------------------------
# Алфавит (без 'ё', 'ё'≡'е')
# ---------------------------
RUS = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  # 32 буквы
INDEX_RUS = {ch: i for i, ch in enumerate(RUS)}
M = len(RUS)

# Частотные русские (ориентир для 2.5)
RU_COMMON = ["о","е","а","и","н","т","с","р","в","л","к","м","д","п","у","я","г","ь","ы","з","б","ч","й","х","ж","ш","ю","ц","щ","э","ф","ъ"]

# ---------------------------
# Нормализация 'ё' -> 'е'
# ---------------------------
def normalize_yo(text: str) -> str:
    return text.replace("ё", "е").replace("Ё", "Е")

# ---------------------------
# НОД / расширенный Евклид / обратный
# ---------------------------
def euclid_gcd(a: int, b: int) -> int:
    a0, b0 = abs(a), abs(b)
    while b0 != 0:
        a0, b0 = b0, a0 % b0
    return a0

def extended_euclid(a: int, b: int) -> Tuple[int, int, int]:
    a0, b0 = a, b
    x0, y0 = 1, 0
    x1, y1 = 0, 1
    while b0 != 0:
        q = a0 // b0
        a0, b0, x0, x1, y0, y1 = b0, a0 - q*b0, x1, x0 - q*x1, y1, y0 - q*y1
    return a0, x0, y0

def modinv_manual(a: int, m: int) -> Optional[int]:
    g, x, _ = extended_euclid(a, m)
    if g != 1 and g != -1:
        return None
    return x % m

# ---------------------------
# Решение сравнения и системы сравнений
# ---------------------------
def solve_linear_congruence_manual(a: int, b: int, m: int) -> List[int]:
    a_mod, b_mod = a % m, b % m
    g = euclid_gcd(a_mod, m)
    if b_mod % g != 0:
        return []
    a1, b1, m1 = a_mod // g, b_mod // g, m // g
    inv_a1 = modinv_manual(a1, m1)
    if inv_a1 is None:
        return []
    x0 = (inv_a1 * b1) % m1
    return sorted({ (x0 + k*m1) % m for k in range(g) })

def solve_affine_system_manual(a: int, b: int, c: int, d: int, m: int) -> List[Tuple[int, int]]:
    A = (a - c) % m
    B = (b - d) % m
    xs = solve_linear_congruence_manual(A, B, m)
    out = []
    for x in xs:
        y = (b - (a * x) % m) % m
        out.append((x, y))
    return out

# ---------------------------
# Аффинный шифр (RU)
# ---------------------------
class AffineRU:
    def __init__(self, alphabet: str = RUS):
        self.alph = alphabet
        self.m = len(alphabet)
        self.idx = {ch: i for i, ch in enumerate(alphabet)}

    def encrypt(self, plaintext: str, a: int, b: int) -> str:
        if euclid_gcd(a, self.m) != 1:
            raise ValueError(f"'a'={a} и m={self.m} не взаимно просты — шифрование некорректно.")
        res = []
        text = normalize_yo(plaintext)
        for ch in text:
            low = ch.lower()
            if low in self.idx:
                y = (a * self.idx[low] + b) % self.m
                enc = self.alph[y]
                res.append(enc.upper() if ch.isupper() else enc)
            else:
                res.append(ch)
        return "".join(res)

    def decrypt(self, ciphertext: str, a: int, b: int) -> str:
        inv = modinv_manual(a % self.m, self.m)
        if inv is None:
            raise ValueError(f"'a'={a} не имеет обратного по модулю m={self.m}; расшифровка невозможна.")
        res = []
        text = normalize_yo(ciphertext)
        for ch in text:
            low = ch.lower()
            if low in self.idx:
                x = (inv * (self.idx[low] - b)) % self.m
                dec = self.alph[x]
                res.append(dec.upper() if ch.isupper() else dec)
            else:
                res.append(ch)
        return "".join(res)

# ---------------------------
# Частотный анализ (2.4) + гипотезы (2.5)
# ---------------------------
def keep_only_russian(text: str) -> str:
    t = normalize_yo(text).lower()
    aset = set(RUS)
    return "".join(ch for ch in t if ch in aset)

def frequency_report(text: str) -> Tuple[str, List[Tuple[str,int,int]]]:
    """
    Возвращает:
      - готовый текст отчёта с таблицей частот,
      - список [(буква, count, percent_int*100)], отсортированный по убыванию.
    """
    filtered = keep_only_russian(text)
    total = len(filtered)
    if total == 0:
        return "В тексте нет русских букв для анализа.", []
    cnt = Counter(filtered)
    items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
    lines = []
    lines.append(f"Всего русских букв: {total}")
    lines.append("Топ-2: " + ", ".join([f"{ch} ({c})" for ch, c in items[:2]]))
    lines.append("\nЧастоты (убывание):")
    rows = []
    for ch, c in items:
        pct = int(round(100 * c / total))
        rows.append((ch, c, pct))
        lines.append(f"{ch} : {c} ({pct}%)")
    return "\n".join(lines), rows

def guess_plain_pairs_from_top(rows: List[Tuple[str,int,int]], max_pairs: int = 10) -> List[Tuple[str,str]]:
    """
    Формирует гипотезы соответствия:
      самая частая буква шифра -> одна из {о,е,а,...}
      вторая по частоте -> следующая из списка частых, отличная от первой
    Возвращает список пар (p1, p2) — предполагаемые БУКВЫ ОТКРЫТОГО ТЕКСТА
    для двух самых частых букв шифртекста.
    """
    if len(rows) < 2:
        return []
    # берём топ-2 шифра (но возвращаем пары plaintext)
    candidates = []
    # перебор первых 6–8 наиболее распространённых букв
    top_plain = RU_COMMON[:8]
    for i in range(len(top_plain)):
        for j in range(len(top_plain)):
            if i == j:
                continue
            candidates.append((top_plain[i], top_plain[j]))
            if len(candidates) >= max_pairs:
                return candidates
    return candidates

def key_from_two_mappings(p1: str, p2: str, c1: str, c2: str) -> Optional[Tuple[int,int]]:
    """
    По двум соответствиям plaintext->cipher вычисляет (a,b):
      c1 ≡ a*p1 + b (mod m)
      c2 ≡ a*p2 + b (mod m)
      => a ≡ (c1 - c2) * inv(p1 - p2) (mod m),  b ≡ c1 - a*p1
    Возвращает None, если inv(p1-p2) не существует (неВП с m).
    """
    x1, x2 = INDEX_RUS[p1], INDEX_RUS[p2]
    y1, y2 = INDEX_RUS[c1], INDEX_RUS[c2]
    denom = (x1 - x2) % M
    inv = modinv_manual(denom, M)
    if inv is None:
        return None
    a = ((y1 - y2) * inv) % M
    b = (y1 - a * x1) % M
    if euclid_gcd(a, M) != 1:
        return None
    return a, b

def build_hypotheses(cipher_text: str, preview_len: int = 200) -> str:
    """
    Формирует текстовый отчёт:
      - Топ-2 букв шифра
      - Список гипотез (p1,p2) и вычисленные ключи (a,b), если возможно
      - Короткое превью дешифровки по каждому найденному ключу
    """
    report, rows = frequency_report(cipher_text)
    if not rows:
        return report
    c1, c2 = rows[0][0], rows[1][0]
    lines = [report, "\nГипотезы соответствий (2.5) и кандидаты ключей:"]
    pairs = guess_plain_pairs_from_top(rows, max_pairs=12)
    aff = AffineRU()
    count_ok = 0
    for p1, p2 in pairs:
        key = key_from_two_mappings(p1, p2, c1, c2)
        if key is None:
            lines.append(f"- {c1}->{p1}, {c2}->{p2} : ключ не вычисляется (нет обратного для (x1-x2))")
            continue
        a, b = key
        try:
            dec = aff.decrypt(cipher_text, a, b)
            preview = dec.replace("\n", " ")[:preview_len]
            lines.append(f"- {c1}->{p1}, {c2}->{p2} => (a={a}, b={b}) | превью: {preview}")
            count_ok += 1
        except Exception as ex:
            lines.append(f"- {c1}->{p1}, {c2}->{p2} => (a={a}, b={b}) | ошибка расшифровки: {ex}")
    if count_ok == 0:
        lines.append("Не удалось получить ни одного рабочего ключа из гипотез.")
    lines.append("\nПодсказка: выберите понравившуюся гипотезу и проверьте её в меню «Шифрование/Дешифрование» или используйте перебор.")
    return "\n".join(lines)

# ---------------------------
# Ввод/вывод: консоль или файл
# ---------------------------
def choose_io_direction(prompt_in_out: str = "Куда вывести результат? (1=console, 2=file): ") -> str:
    while True:
        choice = input(prompt_in_out).strip().lower()
        if choice in ("1", "console", "c", "консоль"):
            return "console"
        if choice in ("2", "file", "f", "файл"):
            path = input("Введите путь к файлу: ").strip()
            return path
        print("Введите '1' для console или '2' для file (или console/file).")

def read_text_source(prompt: str = "Откуда читать текст? (1=console, 2=file): ") -> str:
    src = choose_io_direction(prompt)
    if src == "console":
        print("Вводите текст. Пустая строка — завершить ввод.")
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
            with open(src, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print("Ошибка чтения файла:", e)
            return ""

def write_text_dest(default_text: str, prompt: str = "Куда вывести результат? (1=console, 2=file): "):
    dest = choose_io_direction(prompt)
    if dest == "console":
        print("\n---- РЕЗУЛЬТАТ ----")
        print(default_text)
        print("---- КОНЕЦ РЕЗУЛЬТАТА ----\n")
    else:
        try:
            with open(dest, "w", encoding="utf-8") as f:
                f.write(default_text)
            print("Записано в файл:", dest)
        except Exception as e:
            print("Ошибка записи в файл:", e)

# ---------------------------
# Устойчивое распознавание «да» (для перебора)
# ---------------------------
def _clean_answer(s: Optional[str]) -> str:
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00A0", " ").replace("\u202F", " ")
    s = "".join(ch for ch in s if not ch.isspace())
    return s.lower()

def is_yes(s: Optional[str]) -> bool:
    t = _clean_answer(s)
    return t in ("y", "yes", "д", "да", "1")

# ---------------------------
# Brute-force (2.6) — ЛОГ ПЕРЕЗАПИСЫВАЕТСЯ КАЖДЫЙ РАЗ
# ---------------------------
def brute_force_ru(ciphertext: str, log_path: str):
    """
    Перебирает пары (a,b) с gcd(a,m)=1, b∈[0..m-1].
    Лог ПЕРЕЗАПИСЫВАЕТСЯ (mode='w') при каждом запуске.
    Возвращает (found: bool, a, b, plaintext_or_none).
    """
    cipher = AffineRU()
    m = cipher.m
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("="*80 + "\n")
            f.write(f"BRUTE START {datetime.now().isoformat()} m={m}\n")
            for a in range(1, m):
                if euclid_gcd(a, m) != 1:
                    continue
                for b in range(0, m):
                    try:
                        dec = cipher.decrypt(ciphertext, a, b)
                    except Exception:
                        continue
                    f.write(f"[a={a:>2}, b={b:>2}] {dec}\n")
                    preview = dec.replace("\n", " ")[:200]
                    print(f"a={a}, b={b} | {preview}")
                    ans = input("Остановить? (1=да / y/yes/д/да, Enter=нет): ")
                    if is_yes(ans):
                        print("Останавливаемся. Полный лог сохранён в", log_path)
                        f.write("BRUTE STOPPED BY USER\n")
                        return True, a, b, dec
            f.write("BRUTE FINISHED\n")
    except Exception as e:
        print("Ошибка при работе с файлом лога:", e)
        return False, None, None, None
    print("Перебор завершён. Все варианты записаны в", log_path)
    return False, None, None, None

# ---------------------------
# Подменю математических расчётов (2.1–2.3)
# ---------------------------
def sub_menu_math():
    while True:
        print("\n--- Математические расчёты ---")
        print("1) НОД (a, b)")
        print("2) Обратный элемент a^{-1} (mod m)")
        print("3) Решение a*x ≡ b (mod m)")
        print("4) Система: (a*x + y)≡b, (c*x + y)≡d (mod m)")
        print("5) Назад")
        choice = input("Выберите (1-5 или слово): ").strip().lower()

        if choice in ("5", "назад", "back"):
            return

        if choice in ("1", "нод", "gcd"):
            try:
                a = int(input("a = ").strip())
                b = int(input("b = ").strip())
            except ValueError:
                print("Требуется целое число.")
                continue
            g = euclid_gcd(a, b)
            write_text_dest(f"gcd({a}, {b}) = {g}")
            continue

        if choice in ("2", "обратный", "inverse"):
            try:
                a = int(input("a = ").strip())
                m = int(input("m (>1) = ").strip())
            except ValueError:
                print("Требуется целое число.")
                continue
            inv = modinv_manual(a, m)
            if inv is None:
                write_text_dest(f"Обратного элемента для a={a} по модулю m={m} не существует (gcd(a,m) ≠ 1).")
                continue
            write_text_dest(f"a^(-1) ≡ {inv} (mod {m}). Проверка: {(a*inv)%m}")
            continue

        if choice in ("3", "решение", "solve"):
            try:
                a = int(input("a = ").strip())
                b = int(input("b = ").strip())
                m = int(input("m (>1) = ").strip())
            except ValueError:
                print("Требуется целое число.")
                continue
            sols = solve_linear_congruence_manual(a, b, m)
            if not sols:
                write_text_dest(f"Уравнение {a}*x ≡ {b} (mod {m}) не имеет решений.")
            else:
                write_text_dest(f"Решения: {sols}")
            continue

        if choice in ("4", "система", "system"):
            try:
                a = int(input("a = ").strip())
                b = int(input("b = ").strip())
                c = int(input("c = ").strip())
                d = int(input("d = ").strip())
                m = int(input("m (>1) = ").strip())
            except ValueError:
                print("Требуется целое число.")
                continue
            sols = solve_affine_system_manual(a, b, c, d, m)
            if not sols:
                write_text_dest("Система неразрешима (нет решений).")
            else:
                pairs = ", ".join([f"(x={x}, y={y})" for x, y in sols])
                write_text_dest(f"Решения: {pairs}")
            continue

        print("Неизвестный выбор. Введите цифру (1-5) или слово.")

# ---------------------------
# Меню частотного анализа и гипотез (2.4–2.5)
# ---------------------------
def menu_frequency_and_hypotheses():
    print("\n--- Частотный анализ и гипотезы (2.4–2.5) ---")
    text = read_text_source("Откуда взять шифртекст? (1=console, 2=file): ")
    if not text:
        print("Текст пустой — возврат в меню.")
        return
    report = build_hypotheses(text, preview_len=200)
    write_text_dest(report, "Куда вывести отчёт? (1=console, 2=file): ")

# ---------------------------
# Главное меню
# ---------------------------
def menu_main():
    cipher = AffineRU()
    while True:
        print("\n=== Аффинный шифр ===")
        print("1) Математические расчёты ")
        print("2) Шифрование / Дешифрование (ключ известен)")
        print("3) Взлом (перебор ключей) ")
        print("4) Частотный анализ и гипотезы ")
        print("5) Выход")
        choice = input("Выберите (1-5 или слово): ").strip().lower()

        if choice in ("1", "math", "математика"):
            sub_menu_math()
            continue

        if choice in ("2", "шифрование", "encrypt"):
            print("\n--- Шифрование / Дешифрование ---")
            text = read_text_source("Откуда взять текст для операции? (1=console, 2=file): ")
            if text == "":
                print("Пусто — назад.")
                continue
            try:
                a = int(input("a (взаимно просто с 32) = ").strip())
                b = int(input("b (0..31) = ").strip())
            except ValueError:
                print("Неверный ключ.")
                continue
            op = input("Выберите режим (1=шифровать, 2=дешифровать; или e/d): ").strip().lower()
            if op in ("1", "e", "шифровать", "encrypt"):
                try:
                    out = cipher.encrypt(text, a, b)
                except Exception as ex:
                    print("Ошибка:", ex)
                    continue
            else:
                try:
                    out = cipher.decrypt(text, a, b)
                except Exception as ex:
                    print("Ошибка:", ex)
                    continue
            write_text_dest(out)
            continue

        if choice in ("3", "взлом", "brute"):
            print("\n--- Взлом (brute-force) ---")
            ciphertext = read_text_source("Откуда взять шифртекст? (1=console, 2=file): ")
            if not ciphertext:
                print("Пустой — назад.")
                continue
            log_path = input("Путь для логов [Enter = affine_ru_log.txt]: ").strip() or "affine_ru_log.txt"
            print("Старт перебора. На каждой итерации будет превью и вопрос об остановке.")
            found, a, b, plain = brute_force_ru(ciphertext, log_path)

            # Итог: спросить, куда вывести результат
            if found:
                result_text = (
                    f"НАЙДЕН КЛЮЧ: a={a}, b={b}\n\n"
                    f"РАСШИФРОВКА:\n{plain}\n\n"
                    f"(Лог: {log_path})"
                )
            else:
                result_text = f"Ключ не подтверждён пользователем. Полный лог: {log_path}"
            write_text_dest(result_text, "Куда вывести результат? (1=console, 2=file): ")
            continue

        if choice in ("4", "частотный", "частоты", "анализ", "hypo", "freq"):
            menu_frequency_and_hypotheses()
            continue

        if choice in ("5", "exit", "выход"):
            print("Пока!")
            break

        print("Неверный пункт. Введите 1–5 (или слово).")

# ---------------------------
# Запуск
# ---------------------------
if __name__ == "__main__":
    menu_main()
