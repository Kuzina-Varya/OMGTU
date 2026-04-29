import math

def get_function_input():
    print("=" * 60)
    print("МЕТОД НЬЮТОНА")
    print("=" * 60)
    print("\nВариант  10:")
    print("  sin(y-1) + x = 1.3")
    print("  y - sin(x+1) = 0.8")
    print("=" * 60)
    
    # Система в виде F(x,y) = 0 и G(x,y) = 0
    F_str = "sin(y-1) + x - 1.3"
    G_str = "y - sin(x+1) - 0.8"
    
    # Частные производные
    dF_dx_str = "1"
    dF_dy_str = "cos(y-1)"
    dG_dx_str = "-cos(x+1)"
    dG_dy_str = "1"
    
    print(f"\nF(x,y) = {F_str}")
    print(f"G(x,y) = {G_str}")
    print(f"\nЧастные производные:")
    print(f"  ∂F/x = {dF_dx_str}")
    print(f"  ∂F/∂y = {dF_dy_str}")
    print(f"  ∂G/∂x = {dG_dx_str}")
    print(f"  ∂G/∂y = {dG_dy_str}")
    
    print("\nРекомендуемые начальные приближения: x0 = 0.5, y0 = 1.5")
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
    
    print("\n" + "=" * 80)
    print(f"{'Итерация':<10} {'x':<15} {'y':<15} {'F(x,y)':<15} {'Погрешность':<15}")
    print("=" * 80)
    
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
        
        # Значение невязки F(x,y)
        f_val = F
        
        # Определитель матрицы Якоби
        D = Fx * Gy - Gx * Fy
        
        if abs(D) < 1e-10:
            print("Определитель матрицы Якоби близок к нулю!")
            return
        
        
        dx = (G * Fy - F * Gy) / D
        dy = (F * Gx - Fx * G) / D
        
        x = x + dx
        y = y + dy
        
        error = max(abs(dx), abs(dy))
        
        print(f"{k:<10} {x:<15.6f} {y:<15.6f} {f_val:<15.6f} {error:<15.6f}")
        
        if error < epsilon:
            print("=" * 80)
            print(f"Решение найдено за {k} итераций!")
            print(f"x = {x:.6f}")
            print(f"y = {y:.6f}")
            print(f"Невязка F(x,y) = {F:.6f}")
            print(f"Невязка G(x,y) = {G:.6f}")
            return
    
    print("Решение не найдено за максимальное число итераций.")

if __name__ == "__main__":
    solve_newton()