import math

def get_function_input():
    print("=" * 60)
    print("МЕТОД НЬЮТОНА")
    print("=" * 60)
    print("\nВведите вашу систему в виде F(x,y) = 0 и G(x,y) = 0")
    print("Пример: 2*sin(x+1) - y - 0.5")
    print("=" * 60)
    
    F_str = input("\nВведите F(x,y) = 0:  ")
    G_str = input("Введите G(x,y) = 0:  ")
    
    # Частные производные (нужны для метода Ньютона)
    print("\n--- Частные производные ---")
    dF_dx_str = input("∂F/∂x = ")
    dF_dy_str = input("∂F/∂y = ")
    dG_dx_str = input("∂G/∂x = ")
    dG_dy_str = input("∂G/∂y = ")
    
    x = float(input("\nНачальное приближение x0: "))
    y = float(input("Начальное приближение y0: "))
    
    epsilon = float(input("Точность ε (например, 0.001): "))
    max_iter = int(input("Максимум итераций: "))
    
    return F_str, G_str, dF_dx_str, dF_dy_str, dG_dx_str, dG_dy_str, x, y, epsilon, max_iter

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

def solve_newton():
    F_str, G_str, dF_dx_str, dF_dy_str, dG_dx_str, dG_dy_str, x, y, epsilon, max_iter = get_function_input()
    
    print("\n" + "=" * 60)
    print(f"{'Итерация':<10} {'x':<15} {'y':<15} {'Погрешность':<15}")
    print("=" * 60)
    
    for k in range(1, max_iter + 1):
        x_old = x
        y_old = y
        
        F = evaluate_function(F_str, x, y)
        G = evaluate_function(G_str, x, y)
        
        Fx = evaluate_function(dF_dx_str, x, y)
        Fy = evaluate_function(dF_dy_str, x, y)
        Gx = evaluate_function(dG_dx_str, x, y)
        Gy = evaluate_function(dG_dy_str, x, y)
        
        if any(v is None for v in [F, G, Fx, Fy, Gx, Gy]):
            print("Ошибка вычисления!")
            return
        
        # Определитель матрицы Якоби
        D = Fx * Gy - Gx * Fy
        
        if abs(D) < 1e-10:
            print("⚠️ Определитель матрицы Якоби близок к нулю!")
            return
        
        # Поправки по формуле Крамера
        dx = (G * Fy - F * Gy) / D
        dy = (F * Gx - Fx * G) / D
        
        x = x + dx
        y = y + dy
        
        error = max(abs(dx), abs(dy))
        
        print(f"{k:<10} {x:<15.6f} {y:<15.6f} {error:<15.6f}")
        
        if error < epsilon:
            print("=" * 60)
            print(f" Решение найдено за {k} итераций!")
            print(f"x = {x:.6f}")
            print(f"y = {y:.6f}")
            return
    
    print(" Решение не найдено за максимальное число итераций.")

if __name__ == "__main__":
    solve_newton()