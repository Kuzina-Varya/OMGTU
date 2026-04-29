
# Интеграл: ∫[0, 4] (2x / (x^2 + 1)) dx, n = 8

def f(x):
    return (2 * x) / (x**2 + 1)

#  ВАРИАНТА 10
a = 0.0
b = 4.0
n = 8

h = (b - a) / n

# Метод трапеций 
# I = h * [ f(a)/2 + Σ f(x_i) + f(b)/2 ]
sum_mid = 0.0
for i in range(1, n):
    x_i = a + i * h
    sum_mid += f(x_i)

I_trap = h * (0.5 * f(a) + sum_mid + 0.5 * f(b))

print("МЕТОД ТРАПЕЦИЙ (Вариант 10)")
print(f"Пределы: [{a}, {b}], n = {n}, шаг h = {h:.4f}")
print(f"Результат: I = {I_trap:.6f}")