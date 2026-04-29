import numpy as np
import math

def F(x, y):
    """Первое уравнение: sin(y-1) + x - 1.3 = 0"""
    return math.sin(y - 1) + x - 1.3

def G(x, y):
    """Второе уравнение: y - sin(x+1) - 0.8 = 0"""
    return y - math.sin(x + 1) - 0.8

def Phi(x, y):
    """Целевая функция: Φ(x,y) = F²(x,y) + G²(x,y)"""
    return F(x, y)**2 + G(x, y)**2

def grad_Phi(x, y):
    """
    Градиент функции Φ(x,y)
    ∂Φ/∂x = 2*F*∂F/∂x + 2*G*∂G/∂x
    ∂Φ/∂y = 2*F*∂F/y + 2*G*∂G/∂y
    """
    f_val = F(x, y)
    g_val = G(x, y)
    
    # Частные производные F и G
    dF_dx = 1
    dF_dy = math.cos(y - 1)
    dG_dx = -math.cos(x + 1)
    dG_dy = 1
    
    # Частные производные Φ
    dPhi_dx = 2 * f_val * dF_dx + 2 * g_val * dG_dx
    dPhi_dy = 2 * f_val * dF_dy + 2 * g_val * dG_dy
    
    return dPhi_dx, dPhi_dy

def find_optimal_step(x, y, grad_x, grad_y, alpha_init=0.1, tol=1e-8, max_iter=100):
    """
    Поиск оптимального шага α методом одномерной минимизации
    Минимизируем Φ(x - α*grad_x, y - α*grad_y)
    """
    alpha = alpha_init
    
    # Метод дихотомии или простого перебора для поиска оптимального α
    for _ in range(max_iter):
        # Пробуем уменьшить шаг, если функция растет
        phi_new = Phi(x - alpha * grad_x, y - alpha * grad_y)
        phi_old = Phi(x, y)
        
        if phi_new < phi_old:
            # Увеличиваем шаг, если функция убывает
            while True:
                alpha_new = alpha * 1.5
                phi_test = Phi(x - alpha_new * grad_x, y - alpha_new * grad_y)
                if phi_test < phi_new:
                    alpha = alpha_new
                    phi_new = phi_test
                else:
                    break
            return alpha
        else:
            # Уменьшаем шаг
            alpha *= 0.5
            if alpha < tol:
                break
    
    return alpha

def gradient_descent(x0, y0, epsilon=0.001, max_iter=1000):
    """
    Метод наискорейшего спуска (градиентный метод)
    
    Параметры:
    x0, y0 - начальные приближения
    epsilon - точность
    max_iter - максимальное число итераций
    
    Возвращает:
    x, y - решение системы
    """
    print("=" * 70)
    print("МЕТОД НАИСКОРЕЙШЕГО СПУСКА")
    print("=" * 70)
    print("\nСистема уравнений:")
    print("  sin(y-1) + x = 1.3")
    print("  y - sin(x+1) = 0.8")
    print("=" * 70)
    
    x, y = x0, y0
    
    print(f"\n{'Итерация':<10} {'x':<15} {'y':<15} {'Φ(x,y)':<15} {'Шаг α':<10}")
    print("-" * 70)
    
    for k in range(1, max_iter + 1):
        x_old, y_old = x, y
        
        # Вычисляем градиент
        grad_x, grad_y = grad_Phi(x, y)
        
        # Находим оптимальный шаг
        alpha = find_optimal_step(x, y, grad_x, grad_y)
        
        # Делаем шаг
        x = x - alpha * grad_x
        y = y - alpha * grad_y
        
        # Вычисляем значение целевой функции
        phi_val = Phi(x, y)
        
        print(f"{k:<10} {x:<15.6f} {y:<15.6f} {phi_val:<15.2e} {alpha:<10.4f}")
        
        # Проверка сходимости
        error = max(abs(x - x_old), abs(y - y_old))
        
        if error < epsilon and phi_val < epsilon**2:
            print("-" * 70)
            print(f"\nРешение найдено за {k} итераций!")
            print(f"x = {x:.6f}")
            print(f"y = {y:.6f}")
            print(f"Φ(x,y) = {phi_val:.2e}")
            print(f"Невязки:")
            print(f"  F(x,y) = {F(x,y):.2e}")
            print(f"  G(x,y) = {G(x,y):.2e}")
            return x, y, k
    
    print("\nРешение не найдено за максимальное число итераций!")
    return x, y, max_iter

def main():
    # Начальные приближения (рекомендуемые для вашей системы)
    x0 = 0.5
    y0 = 1.5
    
    # Точность
    epsilon = 0.001
    
    # Запуск метода
    x, y, iterations = gradient_descent(x0, y0, epsilon)
    
    # Дополнительная проверка
    print("\n" + "=" * 70)
    print("ПРОВЕРКА РЕШЕНИЯ")
    print("=" * 70)
    print(f"Подставляем в исходные уравнения:")
    print(f"  sin({y:.6f}-1) + {x:.6f} = {math.sin(y-1) + x:.6f} (должно быть 1.3)")
    print(f"  {y:.6f} - sin({x:.6f}+1) = {y - math.sin(x+1):.6f} (должно быть 0.8)")

if __name__ == "__main__":
    main()