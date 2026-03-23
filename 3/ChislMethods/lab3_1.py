import numpy as np

class DirectSolvers:
    """
    Прямые методы решения СЛАУ (Разделы 3.1 и 3.2 методички)
    """

    @staticmethod
    def gauss_method(A, b):
        """
        Метод Гаусса с выбором главного элемента.
        """
        n = len(b)
        # Расширенная матрица
        M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])

        # Прямой ход
        for i in range(n):
            # Выбор главного элемента (pivoting)
            max_row = i + np.argmax(np.abs(M[i:, i]))
            if abs(M[max_row, i]) < 1e-10:
                raise ValueError("Матрица вырожденная.")
            
            if max_row != i:
                M[[i, max_row]] = M[[max_row, i]]

            # Исключение
            for k in range(i + 1, n):
                c = -M[k, i] / M[i, i]
                M[k, i:] += c * M[i, i:]

        # Обратный ход
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
        
        return x

    @staticmethod
    def inverse_matrix_method(A, b):
        """
        Метод обратной матрицы (X = A^-1 * B).
        """
        try:
            A_inv = np.linalg.inv(A)
            x = np.dot(A_inv, b)
            return x
        except np.linalg.LinAlgError:
            raise ValueError("Матрица вырожденная.")

if __name__ == "__main__":
    print("="*50)
    print("ПРЯМЫЕ МЕТОДЫ (Гаусс, Обратная матрица)")
    print("="*50)
    
    # Пример из методички: Вариант 29 (стр. 91, задание "а")
    # Точность для прямых методов определяется машинной точностью
    print("\nРешение Варианта 29:")
    print("7x1 + 7x2 + 5x3 + 2x4 = 0")
    print("3x1 + 3x2 + 3x3 + 3x4 = 2")
    print("7x1 + 2x2 + 5x3 + 5x4 = -2")
    print("1x1 + 3x2 + 4x3 + 5x4 = -2")

    A = np.array([
        [7, 7, 5, 2],
        [3, 3, 3, 3],
        [7, 2, 5, 5],
        [1, 3, 4, 5]
    ], dtype=float)
    b = np.array([0, 2, -2, -2], dtype=float)

    solver = DirectSolvers()

    try:
        x_gauss = solver.gauss_method(A, b)
        print(f"\nМетод Гаусса: {np.round(x_gauss, 4)}")
    except Exception as e:
        print(f"\nОшибка метода Гаусса: {e}")

    try:
        x_inv = solver.inverse_matrix_method(A, b)
        print(f"Метод обратной матрицы: {np.round(x_inv, 4)}")
    except Exception as e:
        print(f"Ошибка метода обратной матрицы: {e}")