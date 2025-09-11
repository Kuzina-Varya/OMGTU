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
            text = input("Введите текст для шифрования: ")
            try:
                key = int(input("Введите ключ (число): "))
                encrypted = caesar_encrypt_decrypt(text, key, 'encrypt')
                
                with open('encrypted.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Ключ: {key}\n")
                    f.write(f"Зашифрованный текст: {encrypted}")
                print("Результат сохранен в encrypted.txt")
            except ValueError:
                print("Ошибка: ключ должен быть целым числом!")
                
        elif choice == '2':
            text = input("Введите текст для расшифрования: ")
            try:
                key = int(input("Введите ключ (число): "))
                decrypted = caesar_encrypt_decrypt(text, key, 'decrypt')
                
                with open('decrypted.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Ключ: {key}\n")
                    f.write(f"Расшифрованный текст: {decrypted}")
                print("Результат сохранен в decrypted.txt")
            except ValueError:
                print("Ошибка: ключ должен быть целым числом!")
                
        elif choice == '3':
            text = input("Введите текст для расшифрования: ")
            with open('decrypted_multi.txt', 'w', encoding='utf-8') as f:
                for key in range(1, 33):
                    decrypted = caesar_encrypt_decrypt(text, key, 'decrypt')
                    f.write(f"Ключ {key}: {decrypted}\n")
            print("Все варианты сохранены в decrypted_multi.txt")
            
        elif choice == '4':
            # Пример зашифрованного текста из задания
            encrypted_text = "шйльфавкж"
            author_work = "грибоедовгореотума"
            
            with open('crack_result.txt', 'w', encoding='utf-8') as f:
                for key in range(1, 33):
                    decrypted = caesar_encrypt_decrypt(encrypted_text, key, 'decrypt')
                    f.write(f"Ключ {key}: {decrypted}\n")
                    
                    if decrypted == "асудьикто":
                        encrypted_author = caesar_encrypt_decrypt(author_work, key, 'encrypt')
                        f.write(f"\nНайден правильный ключ: {key}\n")
                        f.write(f"Зашифрованные автор и произведение: {encrypted_author}")
                        print(f"Найден ключ: {key}")
                        print(f"Зашифрованные данные: {encrypted_author}")
                        break
            print("Результаты взлома сохранены в crack_result.txt")
            
        elif choice == '5':
            print("Выход из программы...")
            break
            
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")
            
        # Пауза перед следующим выводом меню
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()