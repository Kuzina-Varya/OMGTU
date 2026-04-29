import math

def get_function_input():
    print("=" * 60)
    print("МЕТОД ЗЕЙДЕЛЯ")
    print("=" * 60)
    print("\n Вариант 10:")
    print("  sin(y-1) + x = 1.3")
    print("  y - sin(x+1) = 0.8")
    print("=" * 60)
    
    # Система в виде F(x,y) = 0 и G(x,y) = 0
    F_str = "sin(y-1) + x - 1.3"
    G_str = "y - sin(x+1) - 0.8"
    
    # Параметры M1 и M2 (из условия сходимости)
    # Частные производные:
    # ∂F/∂x = 1, ∂F/y = cos(y-1)
    # ∂G/x = -cos(x+1), ∂G/∂y = 1
    # Выбираем M1 >= max|∂F/∂x| = 1, M2 >= max|∂G/∂y| = 1
    M1 = 2
    M2 = 2
    
    print(f"\nF(x,y) = {F_str}")
    print(f"G(x,y) = {G_str}")
    print(f"\nПараметры сходимости:")
    print(f"  M1 = {M1}")
    print(f"  M2 = {M2}")
    
    # Начальные приближения (рекомендуемые)
    print("\nРекомендуемые начальные приближения: x0 = 0.5, y0 = 1.5")
    x = float(input("\nНачальное приближение x0: "))
    y = float(input("Начальное приближение y0: "))
    
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
    
    print("\n" + "=" * 80)
    print(f"{'Итерация':<10} {'x':<15} {'y':<15} {'м1':<15} {'Погрешность':<15}")
    print("=" * 80)
    
    for k in range(1, max_iter + 1):
        x_old = x
        y_old = y
        
        # Метод Зейделя: используем новое x сразу при расчёте y
        F = evaluate_function(F_str, x, y)
        x = x - F / M1
        
        G = evaluate_function(G_str, x, y)
        y = y - G / M2
        
        # м1 - значение функции F на текущей итерации
        m1 = F
        
        error = max(abs(x - x_old), abs(y - y_old))
        
        print(f"{k:<10} {x:<15.6f} {y:<15.6f} {m1:<15.6f} {error:<15.6f}")
        
        if error < epsilon:
            print("=" * 80)
            print(f"Решение найдено за {k} итераций!")
            print(f"x = {x:.6f}")
            print(f"y = {y:.6f}")
            print(f"м1 (параметр M1) = {M1}")
            print(f"м2 (параметр M2) = {M2}")
            return
    
    print("Решение не найдено за максимальное число итераций.")

if __name__ == "__main__":
    solve_seidel()