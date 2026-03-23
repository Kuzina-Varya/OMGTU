import numpy as np

def input_matrix():
    """
    Ввод матрицы с клавиатуры
    """
    print("=" * 70)
    print("ВВОД МАТРИЦЫ")
    print("=" * 70)
    
    n = int(input("Размерность матрицы (n): "))
    
    print(f"\nВведите {n} строк матрицы (через пробел):")
    A = []
    for i in range(n):
        row = list(map(float, input(f"Строка {i+1}: ").split()))
        A.append(row)
    
    return np.array(A)

def power_method(A, max_iter=1000, tol=1e-6):
    n = A.shape[0]
    v = np.ones(n)
    v = v / np.linalg.norm(v)
    eigenvalue_old = 0
    
    for k in range(1, max_iter + 1):
        Av = A @ v
        eigenvalue = np.dot(v, Av) / np.dot(v, v)
        v_new = Av / np.linalg.norm(Av)
        error = abs(eigenvalue - eigenvalue_old)
        
        if error < tol:
            return eigenvalue, v_new, k
        
        eigenvalue_old = eigenvalue
        v = v_new
    
    return eigenvalue, v, max_iter

def qr_algorithm(A, max_iter=1000, tol=1e-6):
    n = A.shape[0]
    Ak = A.copy()
    eigenvalues_prev = np.diag(Ak)
    
    for k in range(1, max_iter + 1):
        Q, R = np.linalg.qr(Ak)
        Ak = R @ Q
        eigenvalues_curr = np.diag(Ak)
        error = np.max(np.abs(eigenvalues_curr - eigenvalues_prev))
        
        if error < tol:
            return np.diag(Ak), k
        
        eigenvalues_prev = eigenvalues_curr
    
    return np.diag(Ak), max_iter

def main():
    print("\n" + "=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №3")
    print("Нахождение собственных чисел и собственных векторов")
    print("=" * 70)
    
    # Выбор режима
    print("\n1 - Вариант 10 (готовая матрица)")
    print("2 - Ввести свою матрицу")
    choice = input("Выбор: ")
    
    if choice == "1":
        A = np.array([
            [7.48,   16.21,   9.34,   0.58],
            [6.34,    1.47,   6.94,  -0.77],
            [-0.15,   1.24,   9.98,   7.63],
            [10.28,   1.38,  -7.51,  -2.99]
        ])
        print("\n Используется матрица 10 варианта")
    else:
        A = input_matrix()
    
    print("\nИсходная матрица:")
    print(A)
    
    # Степенной метод
    lambda_max, v_max, iter_power = power_method(A)
    print(f"\n{'='*70}")
    print(f"СТЕПЕННОЙ МЕТОД")
    print(f"{'='*70}")
    print(f"Наибольшее собственное число: {lambda_max:.6f}")
    print(f"Собственный вектор: {v_max}")
    print(f"Итераций: {iter_power}")
    
    # QR-алгоритм
    eigenvalues, iter_qr = qr_algorithm(A)
    print(f"\n{'='*70}")
    print(f"QR-АЛГОРИТМ")
    print(f"{'='*70}")
    print(f"Все собственные числа: {np.sort(eigenvalues)[::-1]}")
    print(f"Итераций: {iter_qr}")
    
    # Проверка numpy
    np_eigenvalues, _ = np.linalg.eig(A)
    print(f"\n{'='*70}")
    print(f"ПРОВЕРКА (numpy.linalg.eig)")
    print(f"{'='*70}")
    print(f"Собственные числа: {np.sort(np_eigenvalues)[::-1]}")

if __name__ == "__main__":
    main()