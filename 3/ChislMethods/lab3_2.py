import numpy as np

class IterativeSolvers:
    """
    Итерационные методы решения СЛАУ (Разделы 3.4 и 3.5 методички)
    """

    @staticmethod
    def jacobi_method(A, b, x0=None, eps=1e-2, max_iter=100):
        """
        Метод простой итерации (Якоби).
        Формула (3.12), условие остановки (3.14).
        """
        n = len(b)
        x = np.zeros(n) if x0 is None else x0.astype(float)
        
        # Проверка диагонального преобладания (условие 3.13)
        for i in range(n):
            diag = abs(A[i, i])
            off_diag = np.sum(np.abs(A[i, :])) - diag
            if diag <= off_diag:
                print(f"Предупреждение: Нет диагонального преобладания в строке {i+1}. Сходимость не гарантирована.")

        for k in range(max_iter):
            x_new = np.zeros(n)
            for i in range(n):
                s = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (b[i] - s) / A[i, i]
            
            # Проверка точности: max|x_new - x| < eps
            if np.max(np.abs(x_new - x)) < eps:
                return x_new, k + 1
            
            x = x_new
            
        print("Предупреждение: Достигнуто макс. число итераций.")
        return x, max_iter

    @staticmethod
    def seidel_method(A, b, x0=None, eps=1e-2, max_iter=100):
        """
        Метод Зейделя.
        Формула (3.17). Использует обновленные значения сразу.
        """
        n = len(b)
        x = np.zeros(n) if x0 is None else x0.astype(float)

        for k in range(max_iter):
            x_old = x.copy()
            for i in range(n):
                s1 = np.dot(A[i, :i], x[:i])      # Уже обновленные
                s2 = np.dot(A[i, i+1:], x_old[i+1:]) # Старые
                x[i] = (b[i] - s1 - s2) / A[i, i]
            
            if np.max(np.abs(x - x_old)) < eps:
                return x, k + 1
        
        print("Предупреждение: Достигнуто макс. число итераций.")
        return x, max_iter

if __name__ == "__main__":
    print("="*50)
    print("ИТЕРАЦИОННЫЕ МЕТОДЫ (Якоби, Зейдель)")
    print("="*50)

    # Используем систему Варианта 29, но с точностью 0.01 (задание "б")
    print("\nРешение Варианта 29 (точность 0.01):")
    A = np.array([
        [7, 7, 5, 2],
        [3, 3, 3, 3],
        [7, 2, 5, 5],
        [1, 3, 4, 5]
    ], dtype=float)
    b = np.array([0, 2, -2, -2], dtype=float)

    # Для сходимости итерационных методов часто требуется приведение к диагональному преобладанию.
    # В данном коде реализован базовый алгоритм согласно методичке.
    
    solver = IterativeSolvers()

    x_jacobi, iter_j = solver.jacobi_method(A, b, eps=0.01, max_iter=1000)
    print(f"\nМетод Якоби (итераций: {iter_j}): {np.round(x_jacobi, 4)}")

    x_seidel, iter_s = solver.seidel_method(A, b, eps=0.01, max_iter=1000)
    print(f"Метод Зейделя (итераций: {iter_s}): {np.round(x_seidel, 4)}")