import math
from collections import Counter
import matplotlib.pyplot as plt
import os

def generate_ngrams(text, n):
    """Генерация k-грамм для очищенного текста"""
    ngrams_list = []
    for i in range(len(text) - n + 1):
        ngram = tuple(text[i:i + n])
        ngrams_list.append(ngram)
    return ngrams_list

def clean_text_simple(text):
    """Очистка текста от лишних символов"""
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Удаляем пробелы
    text = text.replace(" ", "")
    
    # Удаляем знаки препинания 
    punctuation = '.,!?;:-()""\'\''
    for char in punctuation:
        text = text.replace(char, '')
    return text

def calculate_entropy(text, k, k_grams):
    """
    Вычисляет энтропию H_k(T) для заданного k
    H_k(T) = -Σ p(z_i^k) * log2(p(z_i^k))
    """
    if len(text) < k:
        return 0
    
    # Считаем частоты k-грамм
    total_grams = len(k_grams)
    freq = Counter(k_grams)
    
    # Вычисляем энтропию
    entropy = 0.0
    for count in freq.values():
        probability = count / total_grams
        if probability > 0:  # избегаем log(0)
            entropy -= probability * math.log2(probability)
    
    return entropy

def calculate_normalized_entropy(text, k):
    """
    Вычисляет нормированную энтропию H_k(T)/k
    """
    # Нужно вычислить k_grams для этого k
    k_grams = generate_ngrams(text, k)
    h_k = calculate_entropy(text, k, k_grams)
    return h_k / k if k > 0 else 0

def calculate_redundancy(normalized_entropy, alphabet_size=33):
    """Вычисляет избыточность языка R = 1 - H_norm / H_max"""
    h_max = math.log2(alphabet_size)
    return 1 - (normalized_entropy / h_max) if h_max > 0 else 0

def save_results_to_file(results, cleaned_text, filename="entropy_analysis_result.txt"):
    """Сохраняет результаты анализа в файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("АНАЛИЗ ЭНТРОПИИ ТЕКСТА\n")
            f.write("=" * 50 + "\n")
            f.write(f"Длина очищенного текста: {len(cleaned_text)} символов\n")
            f.write(f"Текст (первые 200 символов): {cleaned_text[:200]}\n\n")
            
            for result in results:
                f.write(f"\n--- Анализ для k = {result['k']} ---\n")
                f.write(f"Количество {result['k']}-грамм: {len(result['k_grams'])}\n")
                f.write(f"Абсолютная энтропия H_{result['k']}(T): {result['h_k']:.4f}\n")
                f.write(f"Нормированная энтропия H_{result['k']}(T)/{result['k']}: {result['h_k_norm']:.4f}\n")
                f.write(f"Избыточность языка: {result['redundancy']:.4f}\n")
                
                # Топ-5 самых частых k-грамм
                if result['k_grams']:
                    freq = Counter(result['k_grams'])
                    f.write(f"Топ-5 самых частых {result['k']}-грамм:\n")
                    for gram, count in freq.most_common(5):
                        percentage = (count / len(result['k_grams'])) * 100
                        f.write(f"  {gram}: {count} раз ({percentage:.2f}%)\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("ИТОГОВАЯ ТАБЛИЦА\n")
            f.write("=" * 50 + "\n")
            f.write(f"{'k':<3} {'H_k(T)':<10} {'H_k(T)/k':<12} {'Избыточность':<15}\n")
            f.write("-" * 45 + "\n")
            for result in results:
                f.write(f"{result['k']:<3} {result['h_k']:<10.4f} {result['h_k_norm']:<12.4f} {result['redundancy']:<15.4f}\n")
        
        return True, filename
    except Exception as e:
        return False, str(e)

def print_results_to_console(results, cleaned_text):
    """Выводит результаты анализа в консоль"""
    print("\n" + "=" * 60)
    print("АНАЛИЗ ЭНТРОПИИ ТЕКСТА")
    print("=" * 60)
    print(f"Длина очищенного текста: {len(cleaned_text)} символов")
    print(f"Текст (первые 200 символов): {cleaned_text[:200]}")
    
    for result in results:
        print(f"\n--- Анализ для k = {result['k']} ---")
        print(f"Количество {result['k']}-грамм: {len(result['k_grams'])}")
        print(f"Абсолютная энтропия H_{result['k']}(T): {result['h_k']:.4f}")
        print(f"Нормированная энтропия H_{result['k']}(T)/{result['k']}: {result['h_k_norm']:.4f}")
        print(f"Избыточность языка: {result['redundancy']:.4f}")
        
        # Показываем первые 10 k-грамм для примера
        print(f"Примеры {result['k']}-грамм (первые 10): {result['k_grams'][:10]}")
        
        # Топ-5 самых частых k-грамм
        if result['k_grams']:
            freq = Counter(result['k_grams'])
            print(f"Топ-5 самых частых {result['k']}-грамм:")
            for gram, count in freq.most_common(5):
                percentage = (count / len(result['k_grams'])) * 100
                print(f"  {gram}: {count} раз ({percentage:.2f}%)")
    
    # Итоговая таблица
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ ТАБЛИЦА")
    print("=" * 60)
    print(f"{'k':<3} {'H_k(T)':<10} {'H_k(T)/k':<12} {'Избыточность':<15}")
    print("-" * 45)
    for result in results:
        print(f"{result['k']:<3} {result['h_k']:<10.4f} {result['h_k_norm']:<12.4f} {result['redundancy']:<15.4f}")

# Основная программа
while True:
    print('\nВыберите способ ввода текста: \n1 - ввести с консоли \n2 - прочитать из файла \n0 - выход')
    src = input('Ваш выбор: ')
    
    if src == '0':
        break
    elif src == '1':
        text = input('Введите текст: ')
        cleaned_text = clean_text_simple(text)
    elif src == '2':
        path = input('Введите путь к файлу: ')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            cleaned_text = clean_text_simple(text)
        except FileNotFoundError:
            print('Файл не найден!')
            continue
        except Exception as e:
            print(f'Ошибка при чтении файла: {e}')
            continue
    else:
        print('Неверный выбор')
        continue
    
    # Вычисляем результаты для k=1-5
    results = []
    for k in range(1, 6):
        if len(cleaned_text) < k:
            print(f"Текст слишком короткий для k={k}")
            break
            
        k_grams = generate_ngrams(cleaned_text, k)
        h_k = calculate_entropy(cleaned_text, k, k_grams)
        h_k_norm = h_k / k if k > 0 else 0
        redundancy = calculate_redundancy(h_k_norm)
        
        results.append({
            'k': k,
            'k_grams': k_grams,
            'h_k': h_k,
            'h_k_norm': h_k_norm,
            'redundancy': redundancy
        })
    
    # Спрашиваем пользователя о способе вывода результатов
    while True:
        print('\nВыберите способ вывода результатов:')
        print('1 - Вывести на консоль')
        print('2 - Сохранить в файл')
        output_choice = input('Ваш выбор: ')
        
        if output_choice == '1':
            print_results_to_console(results, cleaned_text)
            break
        elif output_choice == '2':
            # Предлагаем выбор пути и имени файла
            default_filename = "entropy_analysis_result.txt"
            default_path = os.path.join(os.getcwd(), default_filename)
            
            file_path = input(f'Введите путь и имя файла (по умолчанию: {default_path}): ').strip()
            
            if not file_path:
                file_path = default_path
            else:
                # Если пользователь ввел только имя файла без пути, добавляем текущую директорию
                if not os.path.dirname(file_path):
                    file_path = os.path.join(os.getcwd(), file_path)
            
            success, message = save_results_to_file(results, cleaned_text, file_path)
            
            if success:
                print(f'Результаты успешно сохранены в файл: {message}')
            else:
                print(f'Ошибка при сохранении файла: {message}')
                # Предлагаем сохранить в файл по умолчанию
                retry = input('Попробовать сохранить в файл по умолчанию? (y/n): ').lower()
                if retry == 'y':
                    success, message = save_results_to_file(results, cleaned_text)
                    if success:
                        print(f'Результаты успешно сохранены в файл: {message}')
                    else:
                        print(f'Ошибка при сохранении: {message}')
            break
        else:
            print('Неверный выбор, попробуйте еще раз')
    
    # Построение графика H_k(T)/k от k
    if results:
        k_values = [result['k'] for result in results]
        h_k_norm_values = [result['h_k_norm'] for result in results]
        
        plt.figure(figsize=(10, 6))
        plt.plot(k_values, h_k_norm_values, 'bo-', linewidth=2, markersize=8)
        plt.title('Зависимость H_k(T)/k от k')
        plt.xlabel('k')
        plt.ylabel('H_k(T)/k')
        plt.grid(True)
        
        # Добавляем значения на точки
        for i, v in enumerate(h_k_norm_values):
            plt.annotate(f'{v:.3f}', (k_values[i], v), textcoords="offset points", 
                        xytext=(0,10), ha='center')
        
        plt.show()

print("Программа завершена.")