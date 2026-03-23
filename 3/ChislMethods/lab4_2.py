import math

def get_function_input():
    print("=" * 60)
    print("МЕТОД ЗЕЙДЕЛЯ")
    print("=" * 60)
    print("\nВведите вашу систему в виде F(x,y) = 0 и G(x,y) = 0")
    print("Пример: 2*sin(x+1) - y - 0.5")
    print("Доступные функции: sin, cos, tan, exp, log, sqrt, pow")
    print("=" * 60)
    
    F_str = input("\nВведите F(x,y) = 0:  ")
    G_str = input("Введите G(x,y) = 0:  ")
    
    x = float(input("\nНачальное приближение x0: "))
    y = float(input("Начальное приближение y0: "))
    
    M1 = float(input("Параметр M1 (для x): "))
    M2 = float(input("Параметр M2 (для y): "))
    
    epsilon = float(input("Точность ε (например, 0.001): "))
    max_iter = int(input("Максимум итераций: "))
    
    return F_str, G_str, x, y, M1, M2, epsilon, max_iter

def evaluate_function(expr, x, y):
    try:
        return eval(expr, {
            "x": x, "y": y,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
            "pow": pow, "abs": abs, "pi": math.pi, "e": math.e
        })
    except Exception as e:
        print(f"Ошибка вычисления: {e}")
        return None

def solve_seidel():
    F_str, G_str, x, y, M1, M2, epsilon, max_iter = get_function_input()
    
    print("\n" + "=" * 60)
    print(f"{'Итерация':<10} {'x':<15} {'y':<15} {'Погрешность':<15}")
    print("=" * 60)
    
    for k in range(1, max_iter + 1):
        x_old = x
        y_old = y
        
        # Метод Зейделя: используем новое x сразу при расчёте y
        F = evaluate_function(F_str, x, y)
        x = x - F / M1
        
        G = evaluate_function(G_str, x, y)
        y = y - G / M2
        
        error = max(abs(x - x_old), abs(y - y_old))
        
        print(f"{k:<10} {x:<15.6f} {y:<15.6f} {error:<15.6f}")
        
        if error < epsilon:
            print("=" * 60)
            print(f" Решение найдено за {k} итераций!")
            print(f"x = {x:.6f}")
            print(f"y = {y:.6f}")
            return
    
    print(" Решение не найдено за максимальное число итераций.")

if __name__ == "__main__":
    solve_seidel()