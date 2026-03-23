import numpy as np

class TridiagonalSolver:
    """
    Метод прогонки для трехдиагональных матриц (Раздел 3.3 методички)
    """

    @staticmethod
    def thomas_algorithm(a, b, c, d):
        """
        a - нижняя диагональ (n элементов, a[0] обычно 0)
        b - главная диагональ (n элементов)
        c - верхняя диагональ (n элементов, c[n-1] обычно 0)
        d - вектор правых частей (n элементов)
        
        Формулы (3.9), (3.10), (3.7)
        """
        n = len(b)
        alpha = np.zeros(n)
        beta = np.zeros(n)
        x = np.zeros(n)

        # Прямой ход прогонки
        # Для первого уравнения (i=0)
        if abs(b[0]) < 1e-10:
            raise ValueError("Деление на ноль в первом шаге прогонки.")
            
        alpha[0] = -c[0] / b[0]
        beta[0] = d[0] / b[0]

        for i in range(1, n):
            denom = b[i] + a[i] * alpha[i-1]
            if abs(denom) < 1e-10:
                raise ValueError("Деление на ноль в прогонке.")
            
            alpha[i] = -c[i] / denom if i < n-1 else 0
            beta[i] = (d[i] - a[i] * beta[i-1]) / denom

        # Обратный ход прогонки
        x[n-1] = beta[n-1]
        for i in range(n-2, -1, -1):
            x[i] = alpha[i] * x[i+1] + beta[i]

        return x

if __name__ == "__main__":
    print("="*50)
    print("МЕТОД ПРОГОНКИ (Трехдиагональная матрица)")
    print("="*50)

    # Пример из методички: Вариант 1 (стр. 92, задание "в")
    # 2x1 + 1x2           = 2
    # 0.5x1 + 2x2 - 1x3   = 0
    #      -1x2 + 2x3 - 1x4 = 3
    #           2x3 + 2x4 = 2
    
    print("\nРешение Варианта 1 (задание 'в'):")
    
    # Коэффициенты (индексы 0..3 соответствуют уравнениям 1..4)
    a = np.array([0, 0.5, -1, 2], dtype=float)   # Нижняя диагональ
    b = np.array([2, 2, 2, 2], dtype=float)      # Главная диагональ
    c = np.array([1, -1, -1, 0], dtype=float)    # Верхняя диагональ
    d = np.array([2, 0, 3, 2], dtype=float)      # Правая часть

    solver = TridiagonalSolver()

    try:
        x = solver.thomas_algorithm(a, b, c, d)
        print(f"\nРешение методом прогонки: {np.round(x, 4)}")
        
        # Проверка невязки
        A_test = np.array([
            [2, 1, 0, 0],
            [0.5, 2, -1, 0],
            [0, -1, 2, -1],
            [0, 0, 2, 2]
        ])
        residual = np.dot(A_test, x) - d
        print(f"Максимальная невязка: {np.max(np.abs(residual)):.6f}")
    except Exception as e:
        print(f"Ошибка: {e}")