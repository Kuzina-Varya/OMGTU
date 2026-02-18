from sympy import symbols, diff, lambdify

a = 0.5
b = 1.5
x = symbols('x')

# Символьное выражение (для производных)
f_expr = x**3 + 12*x - 12

# Числовая функция (для вычислений в точках)
f = lambdify(x, f_expr, 'numpy')

count = 0


if f(a) * diff(f_expr, x, 2).subs(x, a) > 0:
    x0 = a
else:
    x0 = b

x1 = x0 - f(x0) / float(diff(f_expr, x).subs(x, x0)) 

while abs(x1 - x0) >= 0.01:
    x0 = x1
    # Численное значение производной в точке x0
    f_prime = diff(f_expr, x).subs(x, x0)
    x1 = x0 - f(x0) / float(f_prime)
    count += 1

print(f"Корень: {x1:.6f}")
print(f"Количество итераций: {count}")
