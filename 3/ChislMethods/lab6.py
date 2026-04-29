import numpy as np
import matplotlib.pyplot as plt

# ============================================================
X = [0.034, 0.394, 0.754, 1.114, 1.474, 1.833, 2.193, 2.553, 2.913]
Y = [2.156, 2.988, 3.377, 3.708, 3.802, 3.900, 4.067, 4.129, 4.171]

SELECTED_LAWS = ["quadratic", "exp_lin"]

# ============================================================
# БИБЛИОТЕКА АППРОКСИМИРУЮЩИХ ЗАКОНОВ
# Формат: имя -> {базисные функции phi_i(x), строка формулы, имена параметров}
# Все законы приведены к линейному виду: y = c1*phi1(x) + c2*phi2(x) + ...
# ============================================================
LAWS = {
    "linear": {
        "basis": [lambda x: x, lambda x: np.ones_like(x)],
        "fmt": "y = {a:.4f}x + {b:.4f}",
        "params": ["a", "b"]
    },
    "quadratic": {
        "basis": [lambda x: x**2, lambda x: x, lambda x: np.ones_like(x)],
        "fmt": "y = {a:.4f}x² + {b:.4f}x + {c:.4f}",
        "params": ["a", "b", "c"]
    },
    "exp_lin": {
        "basis": [lambda x: np.exp(-x), lambda x: np.ones_like(x)],
        "fmt": "y = {a:.4f}exp(-x) + {b:.4f}",
        "params": ["a", "b"]
    },
    "ln_lin": {
        "basis": [lambda x: np.log(x), lambda x: np.ones_like(x)],
        "fmt": "y = {a:.4f}ln(x) + {b:.4f}",
        "params": ["a", "b"]
    },
    "inv_lin": {
        "basis": [lambda x: 1/x, lambda x: np.ones_like(x)],
        "fmt": "y = {a:.4f}/x + {b:.4f}",
        "params": ["a", "b"]
    },
    "sin_lin": {
        "basis": [lambda x: np.sin(x), lambda x: np.ones_like(x)],
        "fmt": "y = {a:.4f}sin(x) + {b:.4f}",
        "params": ["a", "b"]
    }
}

def solve_normal_system(x, y, basis):
    """
    Построение и решение системы нормальных уравнений МНК 
    Возвращает: матрицу A, вектор B, найденные коэффициенты c.
    """
    x, y = np.array(x), np.array(y)
    m = len(basis)
    A = np.zeros((m, m))
    B = np.zeros(m)
    
    # Заполнение по формулам: A[j,k] = Σ φj(xi)φk(xi), B[j] = Σ yi φj(xi)
    for j in range(m):
        phi_j = basis[j](x)
        for k in range(m):
            A[j, k] = np.sum(phi_j * basis[k](x))
        B[j] = np.sum(y * phi_j)
        
    return A, B, np.linalg.solve(A, B)

def calc_residual(y_true, y_pred):
    """Вычисление невязки δ = Σ(yi - Φ(xi))²"""
    return np.sum((np.array(y_true) - np.array(y_pred))**2)

def main():
    print("="*60)
    print("Лабораторная работа №6. АППРОКСИМАЦИЯ МНК")
    print("="*60)

    # 1. Нанесение точек на график
    plt.figure(figsize=(5, 4))
    plt.scatter(X, Y, c='red', zorder=5, label='Табличные точки')
    plt.title("Исходные данные")
    plt.xlabel("x"); plt.ylabel("y"); plt.grid(True, alpha=0.5); plt.legend()
    plt.show()

    results = []
    # 2. Аппроксимация выбранными законами
    for law_name in SELECTED_LAWS:
        law = LAWS[law_name]
        A, B, coeffs = solve_normal_system(X, Y, law["basis"])
        
        x_arr = np.array(X)
        y_pred = sum(c * law["basis"][i](x_arr) for i, c in enumerate(coeffs))
        delta = calc_residual(Y, y_pred)

        # Вывод для отчета
        print(f"\n Закон: {law_name}")
        print("Система нормальных уравнений (A * c = B):")
        print("Матрица A:\n", np.round(A, 4))
        print("Вектор   B:\n", np.round(B, 4))
        print(f"Коэффициенты: {dict(zip(law['params'], np.round(coeffs, 4)))}")
        
        fmt = law["fmt"].format(**dict(zip(law["params"], coeffs)))
        print(f"Итоговая формула: {fmt}")
        print(f"Невязка δ = {delta:.6f}")
        results.append((law_name, law, coeffs, fmt, delta))

    # Сравнение невязок
    best = min(results, key=lambda r: r[4])
    print("\n" + "="*60)
    print(f" НАИЛУЧШАЯ АППРОКСИМАЦИЯ: {best[0]}")
    print(f"Формула: {best[3]} | Минимальная невязка δ = {best[4]:.6f}")
    print("="*60)

    # 3. Графики аппроксимаций вместе с исходной функцией
    plt.figure(figsize=(7, 5))
    plt.scatter(X, Y, c='black', zorder=5, label='Исходные точки')
    x_fine = np.linspace(min(X), max(X), 200)
    for n, l, c, fmt, d in results:
        y_fine = sum(val * l["basis"][i](x_fine) for i, val in enumerate(c))
        plt.plot(x_fine, y_fine, linewidth=2, label=f'{n} (δ={d:.4f})')
    plt.title("Сравнение аппроксимирующих законов")
    plt.xlabel("x"); plt.ylabel("y"); plt.grid(True, alpha=0.6); plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()