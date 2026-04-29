import numpy as np

class TridiagonalSolver:
    """
    Метод прогонки для трехдиагональных матриц 
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
    print("="*60)
    print("МЕТОД ПРОГОНКИ (Трехдиагональная матрица)")
    print("="*60)
    print("\nВариант 10:")
    print("  3x₁ + 2.3x₂           = 2")
    print("  x₁ - 3x₂ + x₃         = 3.2")
    print("      2.2x₂ + 4x₃ - x₄  = 6")
    print("           5x₃ + 7x₄    = 5")
    print("="*60)

    # Система уравнений:
    # 3x₁ + 2.3x₂           = 2
    # x₁ - 3x₂ + x₃         = 3.2
    #      2.2x₂ + 4x₃ - x₄ = 6
    #           5x₃ + 7x₄   = 5
    
    # Коэффициенты (индексы 0..3 соответствуют уравнениям 1..4)
    a = np.array([0, 1, 2.2, 5], dtype=float)    # Нижняя диагональ (под главной)
    b = np.array([3, -3, 4, 7], dtype=float)     # Главная диагональ
    c = np.array([2.3, 1, -1, 0], dtype=float)   # Верхняя диагональ (над главной)
    d = np.array([2, 3.2, 6, 5], dtype=float)    # Правая часть

    solver = TridiagonalSolver()

    try:
        x = solver.thomas_algorithm(a, b, c, d)
        
        print(f"\nРешение методом прогонки:")
        for i in range(len(x)):
            print(f"  x{i+1} = {x[i]:.6f}")
        
        # Проверка невязки
        A_test = np.array([
            [3, 2.3, 0, 0],
            [1, -3, 1, 0],
            [0, 2.2, 4, -1],
            [0, 0, 5, 7]
        ])
        residual = np.dot(A_test, x) - d
        print(f"\nПроверка (невязка):")
        for i in range(len(residual)):
            print(f"  Уравнение {i+1}: {abs(residual[i]):.2e}")
        print(f"Максимальная невязка: {np.max(np.abs(residual)):.2e}")
        
    except Exception as e:
        print(f"Ошибка: {e}")