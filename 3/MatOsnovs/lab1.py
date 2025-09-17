# -*- coding: utf-8 -*-

def caesar_encrypt_decrypt(text, key, mode='encrypt'):
    """
    Шифрует или расшифровывает текст с помощью шифра Цезаря.
    
    :param text: Исходный текст
    :param key: Ключ сдвига (целое число)
    :param mode: Режим: 'encrypt' или 'decrypt'
    :return: Обработанный текст
    """
    ru_alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    result = []
    
    for char in text:
        if char.lower() in ru_alphabet:
            is_upper = char.isupper()
            char_index = ru_alphabet.index(char.lower())
            
            if mode == 'encrypt':
                new_index = (char_index + key) % 32
            else:
                new_index = (char_index - key) % 32
                
            new_char = ru_alphabet[new_index]
            result.append(new_char.upper() if is_upper else new_char)
        else:
            result.append(char)
            
    return ''.join(result)


# ====== УТИЛИТЫ ВВОДА/ВЫВОДА ======
def ask_input_source() -> str:
    """Спросить, откуда брать текст."""
    print("\nВыберите источник текста:")
    print("1 - Ввести с консоли")
    print("2 - Прочитать из файла")
    src = input("Ваш выбор (1-2): ").strip()
    return src

def read_text_with_choice(prompt_console: str) -> str:
    """Вернуть текст из консоли или файла в зависимости от выбора пользователя."""
    src = ask_input_source()
    if src == '2':
        path = input("Введите путь к файлу: ").strip()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = f.read()
            print("Текст успешно прочитан из файла.")
            return data
        except FileNotFoundError:
            print("Ошибка: файл не найден. Возврат к вводу с консоли.")
        except OSError as e:
            print(f"Ошибка чтения файла: {e}. Возврат к вводу с консоли.")
    # По умолчанию — консоль
    return input(prompt_console)

def ask_output_target(default_filename: str) -> tuple[str, str|None]:
    """
    Спросить, куда выводить результат.
    Возвращает ('console', None) или ('file', filename)
    """
    print("\nКуда вывести результат?")
    print("1 - В консоль")
    print("2 - Записать в файл (и дополнительно вывести в консоль)")
    out = input("Ваш выбор (1-2): ").strip()
    if out == '2':
        name = input(f"Имя файла (по умолчанию {default_filename}): ").strip() or default_filename
        return 'file', name
    return 'console', None

def deliver_output(result_text: str, target: tuple[str, str|None]):
    """Вывести в консоль или записать в файл (и тоже вывести в консоль)."""
    where, fname = target
    if where == 'file' and fname:
        try:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(result_text)
            print(f"\nРезультат сохранён в {fname}.")
        except OSError as e:
            print(f"Ошибка записи файла: {e}. Печатаю результат в консоль.")
    # Всегда печать в консоль, как требовалось при записи в файл
    print("\n===== РЕЗУЛЬТАТ =====")
    print(result_text)
    print("=====================")

def ask_yes_no(prompt: str) -> bool:
    """Вернёт True для 'да', False для 'нет'."""
    ans = input(prompt).strip().lower()
    return ans in ('y', 'yes', 'д', 'да')


def main():
    """Основная функция программы."""
    while True:
        print("\n" + "="*50)
        print("Программа для работы с шифром Цезаря")
        print("="*50)
        print("Выберите режим работы:")
        print("1 - Шифрование текста")
        print("2 - Расшифрование текста с ключом")
        print("3 - Расшифрование перебором ключей")
        print("4 - Взлом шифра перебором")
        print("5 - Выход из программы")
        
        choice = input("Ваш выбор (1-5): ").strip()
        
        if choice == '1':
            text = read_text_with_choice("Введите текст для шифрования: ")
            try:
                key = int(input("Введите ключ (число): "))
                encrypted = caesar_encrypt_decrypt(text, key, 'encrypt')
                target = ask_output_target("encrypted.txt")
                result_text = f"Ключ: {key}\nЗашифрованный текст:\n{encrypted}"
                deliver_output(result_text, target)
            except ValueError:
                print("Ошибка: ключ должен быть целым числом!")
                
        elif choice == '2':
            text = read_text_with_choice("Введите текст для расшифрования: ")
            try:
                key = int(input("Введите ключ (число): "))
                decrypted = caesar_encrypt_decrypt(text, key, 'decrypt')
                target = ask_output_target("decrypted.txt")
                result_text = f"Ключ: {key}\nРасшифрованный текст:\n{decrypted}"
                deliver_output(result_text, target)
            except ValueError:
                print("Ошибка: ключ должен быть целым числом!")
                
        elif choice == '3':
            # 1) Получаем текст (консоль/файл)
            text = read_text_with_choice("Введите текст для расшифрования: ")

            # 2) Сразу спрашиваем, куда выводить
            target = ask_output_target("decrypted_multi.txt")

            where, fname = target
            if where == 'file':
                # Пишем все варианты в файл и дублируем в консоль (как раньше)
                lines = []
                for key in range(1, 33):
                    decrypted = caesar_encrypt_decrypt(text, key, 'decrypt')
                    lines.append(f"Ключ {key}: {decrypted}")
                result_text = "\n".join(lines)
                deliver_output(result_text, target)
            else:
                # Пошаговый показ в консоль с вопросом "продолжить?"
                print("\nБуду показывать варианты по одному. Когда найдёте ключ — ответьте 'нет'.\n")
                for key in range(1, 33):
                    decrypted = caesar_encrypt_decrypt(text, key, 'decrypt')
                    print(f"Ключ {key}: {decrypted}")
                    if not ask_yes_no("Продолжить просмотр вариантов? (д/н): "):
                        print("Окей, остановился.")
                        break
            
        elif choice == '4':
            # Пример зашифрованного текста из задания
            encrypted_text = "шйльфавкж"
            author_work = "грибоедовгореотума"
            
            lines = []
            found_block = None
            for key in range(1, 33):
                decrypted = caesar_encrypt_decrypt(encrypted_text, key, 'decrypt')
                lines.append(f"Ключ {key}: {decrypted}")
                if decrypted == "асудьикто":
                    encrypted_author = caesar_encrypt_decrypt(author_work, key, 'encrypt')
                    found_block = (key, encrypted_author)
                    break
            if found_block:
                k, enc_auth = found_block
                lines.append(f"\nНайден правильный ключ: {k}")
                lines.append(f"Зашифрованные автор и произведение: {enc_auth}")
                print(f"Найден ключ: {k}")
                print(f"Зашифрованные данные: {enc_auth}")

            target = ask_output_target("crack_result.txt")
            result_text = "\n".join(lines)
            deliver_output(result_text, target)
            
        elif choice == '5':
            print("Выход из программы...")
            break
            
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")
            
        # Пауза перед следующим выводом меню
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
