import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ============================================================

X = np.array([0.034, 0.394, 0.754, 1.114, 1.474, 1.833, 2.193, 2.553, 2.913])
Y = np.array([2.156, 2.988, 3.377, 3.708, 3.802, 3.900, 4.067, 4.129, 4.171])

# (по результатам моделирования: хорошо работают линейный и экспоненциальный)
SELECTED_LAWS = ["linear", "exp_decay"]

# ============================================================
# БИБЛИОТЕКА АППРОКСИМИРУЮЩИХ ЗАКОНОВ
# Для линейных по параметрам: basis = [phi1(x), phi2(x), ...]
# Для нелинейных: используется линеаризация или численная оптимизация
# ============================================================
LAWS = {
    "linear": {
        "type": "linear",
        "basis": [lambda x: x, lambda x: np.ones_like(x)],
        "fmt": lambda c: f"y = {c[0]:.4f}x + {c[1]:.4f}",
        "params": ["a", "b"],
        "predict": lambda x, c: c[0]*x + c[1]
    },
    "quadratic": {
        "type": "linear",
        "basis": [lambda x: x**2, lambda x: x, lambda x: np.ones_like(x)],
        "fmt": lambda c: f"y = {c[0]:.4f}x² + {c[1]:.4f}x + {c[2]:.4f}",
        "params": ["a", "b", "c"],
        "predict": lambda x, c: c[0]*x**2 + c[1]*x + c[2]
    },
    "exp_decay": {
        "type": "linear",  # y = a*exp(-x) + b -> basis: [exp(-x), 1]
        "basis": [lambda x: np.exp(-x), lambda x: np.ones_like(x)],
        "fmt": lambda c: f"y = {c[0]:.4f}exp(-x) + {c[1]:.4f}",
        "params": ["a", "b"],
        "predict": lambda x, c: c[0]*np.exp(-x) + c[1]
    },
    "ln_linear": {
        "type": "linear",  # y = a*ln(x) + b
        "basis": [lambda x: np.log(x), lambda x: np.ones_like(x)],
        "fmt": lambda c: f"y = {c[0]:.4f}ln(x) + {c[1]:.4f}",
        "params": ["a", "b"],
        "predict": lambda x, c: c[0]*np.log(x) + c[1]
    },
    "inverse": {
        "type": "linear",  # y = a/x + b
        "basis": [lambda x: 1/x, lambda x: np.ones_like(x)],
        "fmt": lambda c: f"y = {c[0]:.4f}/x + {c[1]:.4f}",
        "params": ["a", "b"],
        "predict": lambda x, c: c[0]/x + c[1]
    },
    "power_law": {
        "type": "nonlinear",  # y = a*x^b + c -> линеаризация: ln(y-c) = ln(a) + b*ln(x)
        "fmt": lambda c: f"y = {c[0]:.4f}x^{c[1]:.4f} + {c[2]:.4f}",
        "params": ["a", "b", "c"],
        "predict": lambda x, c: c[0]*x**c[1] + c[2]
    }
}

def solve_normal_equations(x, y, basis):
    """
    Построение и решение системы нормальных уравнений МНК.
    A * c = B, где A[j,k] = Σ φj(xi)φk(xi), B[j] = Σ yi*φj(xi)
    """
    x, y = np.array(x), np.array(y)
    m = len(basis)
    A = np.zeros((m, m))
    B = np.zeros(m)
    
    for j in range(m):
        phi_j = basis[j](x)
        for k in range(m):
            A[j, k] = np.sum(phi_j * basis[k](x))
        B[j] = np.sum(y * phi_j)
    
    return A, B, np.linalg.solve(A, B)

def calc_residual(y_true, y_pred):
    """Невязка δ = Σ(yi - Φ(xi))²"""
    return np.sum((np.array(y_true) - np.array(y_pred))**2)

def fit_nonlinear_power(x, y):
    """
    Подбор параметров для степенного закона y = a*x^b + c
    через линеаризацию и перебор параметра c
    """
    best_delta = np.inf
    best_params = None
    
    # Перебираем возможные значения c
    for c_test in np.linspace(min(y)*0.5, min(y)*1.5, 50):
        y_shifted = y - c_test
        if np.any(y_shifted <= 0):
            continue  # логарифм не определён
            
        # Линеаризация: ln(y-c) = ln(a) + b*ln(x)
        X_lin = np.log(x)
        Y_lin = np.log(y_shifted)
        
        # Линейная аппроксимация: Y = A + b*X, где A = ln(a)
        A_mat = np.vstack([X_lin, np.ones_like(X_lin)]).T
        try:
            b, A_const = np.linalg.lstsq(A_mat, Y_lin, rcond=None)[0]
            a = np.exp(A_const)
            
            # Проверка качества
            y_pred = a * x**b + c_test
            delta = calc_residual(y, y_pred)
            
            if delta < best_delta:
                best_delta = delta
                best_params = (a, b, c_test)
        except:
            continue
    
    return best_params, best_delta if best_params else None

def main():
    print("="*70)
    print("Лабораторная работа №6. СГЛАЖИВАНИЕ. МНК")
    print("="*70)
    
    # 1. Нанесение точек на график
    plt.figure(figsize=(6, 4.5))
    plt.scatter(X, Y, c='red', s=40, zorder=5, label='Табличные точки')
    plt.title("Исходные данные", fontsize=12)
    plt.xlabel("x"); plt.ylabel("y")
    plt.grid(True, alpha=0.4, linestyle='--')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    results = []
    
    # 2. Аппроксимация выбранными законами
    for law_name in SELECTED_LAWS:
        law = LAWS[law_name]
        print(f"\n🔹 Закон: {law_name}")
        
        if law["type"] == "linear":
            # Линейный по параметрам случай
            A, B, coeffs = solve_normal_equations(X, Y, law["basis"])
            
            print("Система нормальных уравнений (A·c = B):")
            print("Матрица A:\n", np.round(A, 5))
            print("Вектор   B:\n", np.round(B, 5))
            print(f"Коэффициенты: {dict(zip(law['params'], np.round(coeffs, 5)))}")
            
            y_pred = law["predict"](X, coeffs)
            delta = calc_residual(Y, y_pred)
            formula = law["fmt"](coeffs)
            
        else:
            # Нелинейный случай (степенной закон)
            coeffs, delta = fit_nonlinear_power(X, Y)
            if coeffs is None:
                print(" Не удалось подобрать параметры")
                continue
            formula = law["fmt"](coeffs)
            y_pred = law["predict"](X, coeffs)
            print(f"Коэффициенты: {dict(zip(law['params'], np.round(coeffs, 5)))}")
        
        print(f"Формула: {formula}")
        print(f"Невязка δ = {delta:.6f}")
        results.append((law_name, law, coeffs, formula, delta, y_pred))
    
    # Сравнение невязок
    if results:
        best = min(results, key=lambda r: r[4])
        print("\n" + "="*70)
        print(f"НАИЛУЧШАЯ АППРОКСИМАЦИЯ: {best[0]}")
        print(f"Формула: {best[3]}")
        print(f"Минимальная невязка δ = {best[4]:.6f}")
        print("="*70)
        
        # 3. Сравнительный график
        plt.figure(figsize=(8, 5.5))
        plt.scatter(X, Y, c='black', s=50, zorder=5, label='Исходные точки')
        
        x_fine = np.linspace(min(X)*0.95, max(X)*1.05, 300)
        colors = ['blue', 'green', 'orange', 'purple']
        
        for idx, (name, law, coeffs, fmt, delta, _) in enumerate(results):
            if law["type"] == "linear":
                y_fine = law["predict"](x_fine, coeffs)
            else:
                y_fine = law["predict"](x_fine, coeffs)
            plt.plot(x_fine, y_fine, color=colors[idx%len(colors)], 
                    linewidth=2.5, label=f'{name} (δ={delta:.4f})')
        
        plt.title("Сравнение аппроксимирующих законов", fontsize=12)
        plt.xlabel("x"); plt.ylabel("y")
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3, linestyle=':')
        plt.tight_layout()
        plt.show()
    else:
        print(" Не удалось выполнить аппроксимацию ни по одному закону")

if __name__ == "__main__":
    main()