import numpy as np

def power_method(A, max_iter=1000, tol=1e-6):
    """
    Степенной метод - находит НАИБОЛЬШЕЕ по модулю собственное число
    и соответствующий собственный вектор
    """
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
    """
    QR-алгоритм - находит ВСЕ собственные числа
    """
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

def find_eigenvectors(A, eigenvalues):
    """
    Находит собственные векторы для каждого собственного числа
    """
    eigenvectors = []
    for lam in eigenvalues:
        # Решаем (A - λI)v = 0
        n = A.shape[0]
        B = A - lam * np.eye(n)
        
        # Используем SVD для нахождения нуль-пространства
        U, S, Vh = np.linalg.svd(B)
        v = Vh[-1, :]
        v = v / np.linalg.norm(v)
        eigenvectors.append(v)
    
    return np.array(eigenvectors)

def verify_solution(A, eigenvalues, eigenvectors):
    """
    Проверка: A·v = λ·v
    """
    print("\n" + "=" * 70)
    print("ПРОВЕРКА РЕШЕНИЯ (A·v = λ·v)")
    print("=" * 70)
    
    for i in range(len(eigenvalues)):
        lam = eigenvalues[i]
        v = eigenvectors[i]
        
        Av = A @ v
        lam_v = lam * v
        
        error = np.linalg.norm(Av - lam_v)
        
        print(f"\nλ{i+1} = {lam:.6f}")
        print(f"  Собственный вектор v{i+1} = {np.round(v, 6)}")
        print(f"  Невязка ||A·v - λ·v|| = {error:.2e}")

def main():
    print("=" * 70)
    print("Собственные числа и собственные векторы")
    print("=" * 70)
    
    # Вариант 10 
    A = np.array([
        [7.48,   16.21,   9.34,   0.58],
        [6.34,    1.47,   6.94,  -0.77],
        [-0.15,   1.24,   9.98,   7.63],
        [10.28,   1.38,  -7.51,  -2.99]
    ])
    
    print("\nИсходная матрица A:")
    print(A)
    print(f"Размерность: {A.shape[0]} × {A.shape[1]}")
    
    # ==================================================================
    # 1. СТЕПЕННОЙ МЕТОД (находит наибольшее собственное число + вектор)
    # ==================================================================
    print("\n" + "=" * 70)
    print("1. СТЕПЕННОЙ МЕТОД")
    print("=" * 70)
    
    lambda_max, v_max, iter_power = power_method(A)
    
    print(f"Наибольшее собственное число: λ = {lambda_max:.6f}")
    print(f"Собственный вектор: v = {np.round(v_max, 6)}")
    print(f"Число итераций: {iter_power}")
    
    # Проверка для степенного метода
    Av = A @ v_max
    lam_v = lambda_max * v_max
    error_power = np.linalg.norm(Av - lam_v)
    print(f"Невязка ||A·v - λ·v|| = {error_power:.2e}")
    
    # ==================================================================
    # 2. QR-АЛГОРИТМ (находит ВСЕ собственные числа)
    # ==================================================================
    print("\n" + "=" * 70)
    print("2. QR-АЛГОРИТМ")
    print("=" * 70)
    
    eigenvalues_qr, iter_qr = qr_algorithm(A)
    
    # Сортируем по убыванию модуля
    idx = np.argsort(np.abs(eigenvalues_qr))[::-1]
    eigenvalues_qr = eigenvalues_qr[idx]
    
    print(f"Все собственные числа (по убыванию |λ|):")
    for i, lam in enumerate(eigenvalues_qr):
        print(f"  λ{i+1} = {lam:.6f}")
    print(f"Число итераций: {iter_qr}")
    
    # ==================================================================
    # 3. НАХОЖДЕНИЕ ВСЕХ СОБСТВЕННЫХ ВЕКТОРОВ (через numpy)
    # ==================================================================
    print("\n" + "=" * 70)
    print("3. ВСЕ СОБСТВЕННЫЕ ВЕКТОРЫ (numpy.linalg.eig)")
    print("=" * 70)
    
    eigenvalues, eigenvectors = np.linalg.eig(A)
    
    # Сортируем по убыванию модуля собственных чисел
    idx = np.argsort(np.abs(eigenvalues))[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    print(f"\nВсе собственные числа:")
    for i, lam in enumerate(eigenvalues):
        if np.iscomplex(lam) and lam.imag != 0:
            print(f"  λ{i+1} = {lam.real:.6f} + {lam.imag:.6f}j")
        else:
            print(f"  λ{i+1} = {lam.real:.6f}")
    
    print(f"\nСоответствующие собственные векторы:")
    for i in range(len(eigenvalues)):
        v = eigenvectors[:, i]
        if np.iscomplex(v).any():
            print(f"  v{i+1} = {np.round(v.real, 6)} (комплексный)")
        else:
            print(f"  v{i+1} = {np.round(v.real, 6)}")
    
    # ==================================================================
    # 4. ПРОВЕРКА РЕШЕНИЯ
    # ==================================================================
    verify_solution(A, eigenvalues, eigenvectors)
    
    # ==================================================================
    # 5. ИТОГОВАЯ ТАБЛИЦА
    # ==================================================================
    print("\n" + "=" * 70)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 70)
    print(f"{'№':<5} {'Собственное число λ':<25} {'Собственный вектор v':<40}")
    print("-" * 70)
    
    for i in range(len(eigenvalues)):
        lam = eigenvalues[i]
        v = eigenvectors[:, i]
        
        if np.iscomplex(lam) and lam.imag != 0:
            lam_str = f"{lam.real:.4f} + {lam.imag:.4f}j"
        else:
            lam_str = f"{lam.real:.4f}"
        
        v_str = str(np.round(v.real, 4))
        
        print(f"{i+1:<5} {lam_str:<25} {v_str:<40}")
    
    print("=" * 70)

if __name__ == "__main__":
    main()