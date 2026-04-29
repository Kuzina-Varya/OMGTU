import math

def f(x):
    """
    Вариант 10:
    x^3 + 12x - 12 = 0
    """
    return x**3 + 12*x - 12

def df(x):
    """
    Производная функции f(x):
    f'(x) = 3x^2 + 12
    """
    return 3*x**2 + 12

def newton_method(x0, eps, max_iter):
    """
    Метод Ньютона (Касательных)
    Формула: x_{n+1} = x_n - f(x_n) / f'(x_n)
    """
    print("\n" + "=" * 70)
    print("МЕТОД НЬЮТОНА")
    print("=" * 70)
    print(f"{'Итерация':<10} {'x':<20} {'f(x)':<20} {'Погрешность':<15}")
    print("-" * 70)
    
    x = x0
    for k in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)
        
        if abs(dfx) < 1e-10:
            print("Производная близка к нулю! Метод не сходится.")
            return None, k
        
        x_new = x - fx / dfx
        error = abs(x_new - x)
        
        print(f"{k:<10} {x_new:<20.10f} {f(x_new):<20.2e} {error:<15.2e}")
        
        if error < eps:
            print("-" * 70)
            print(f"Решение найдено за {k} итераций!")
            return x_new, k
        
        x = x_new
    
    print("Превышено максимальное число итераций.")
    return x, max_iter

def secant_method(x0, x1, eps, max_iter):
    """
    Метод секущих
    Формула: x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    """
    print("\n" + "=" * 70)
    print("МЕТОД СЕКУЩИХ")
    print("=" * 70)
    print(f"{'Итерация':<10} {'x':<20} {'f(x)':<20} {'Погрешность':<15}")
    print("-" * 70)
    
    x_prev = x0
    x_curr = x1
    
    for k in range(1, max_iter + 1):
        f_prev = f(x_prev)
        f_curr = f(x_curr)
        
        if abs(f_curr - f_prev) < 1e-10:
            print("Разность функций близка к нулю! Деление на ноль.")
            return None, k
        
        x_new = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        error = abs(x_new - x_curr)
        
        print(f"{k:<10} {x_new:<20.10f} {f(x_new):<20.2e} {error:<15.2e}")
        
        if error < eps:
            print("-" * 70)
            print(f"Решение найдено за {k} итераций!")
            return x_new, k
        
        x_prev = x_curr
        x_curr = x_new
    
    print("Превышено максимальное число итераций.")
    return x_curr, max_iter

def main():
    print("=" * 70)
    print("Решение нелинейных уравнений")
    print("=" * 70)
    
    # ВАРИАНТ 10
    print("\nВариант 10:")
    print("  Уравнение: x^3 + 12x - 12 = 0")
    print("  Точность: 10^-6")
    print("=" * 70)
    
    # Параметры
    eps = 1e-6
    max_iter = 100
    
    # Начальные приближения
    # f(0) = -12, f(1) = 1 -> корень где-то между 0 и 1
    x0 = 1.0  # Для метода Ньютона
    x_sec0 = 0.0  # Для метода секущих (левая граница)
    x_sec1 = 1.0  # Для метода секущих (правая граница)
    
    print(f"\nНачальное приближение для Ньютона: x0 = {x0}")
    print(f"Начальные приближения для Секущих: x0 = {x_sec0}, x1 = {x_sec1}")
    
    # 1. Метод Ньютона
    root_newton, iter_newton = newton_method(x0, eps, max_iter)
    
    # 2. Метод секущих
    root_secant, iter_secant = secant_method(x_sec0, x_sec1, eps, max_iter)
    
    # Итоговый вывод
    print("\n" + "=" * 70)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 70)
    print(f"Точность ε = {eps}")
    print(f"\n1. Метод Ньютона:")
    if root_newton is not None:
        print(f"   Корень: x = {root_newton:.10f}")
        print(f"   Невязка f(x): {abs(f(root_newton)):.2e}")
        print(f"   Итераций: {iter_newton}")
    
    print(f"\n2. Метод Секущих:")
    if root_secant is not None:
        print(f"   Корень: x = {root_secant:.10f}")
        print(f"   Невязка f(x): {abs(f(root_secant)):.2e}")
        print(f"   Итераций: {iter_secant}")
    
    print("=" * 70)

if __name__ == "__main__":
    main()