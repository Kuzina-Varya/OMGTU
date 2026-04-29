import numpy as np

class DirectSolvers:
    """
    Прямые методы решения СЛАУ
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
    
    # Пример из методички: Вариант 10
    # Точность для прямых методов определяется машинной точностью
    print("\nРешение Варианта 10:")
    print("2.63x1 - 3.18x2 + 0.84x3 + 1.75x4 = 4.92")
    print("1.47x1 + 2.39x2 - 4.26x3 + 0.58x4 = -2.73")
    print("0.91x1 - 1.82x2 + 3.57x3 - 2.64x4 = 3.85")
    print("3.28x1 + 0.69x2 - 1.93x3 + 2.71x4 = 1.68")

    A = np.array([
        [2.63, -3.18, 0.84, 1.75],
        [1.47, 2.39, -4.26, 0.58],
        [0.91, -1.82, 3.57, -2.64],
        [3.28, 0.69, -1.93, 2.71]
    ], dtype=float)
    b = np.array([4.92, -2.73, 3.85, 1.68], dtype=float)

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