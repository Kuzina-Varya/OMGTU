
# Интеграл: ∫[0, 4] (2x / (x^2 + 1)) dx, n = 8

def f(x):
    return (2 * x) / (x**2 + 1)

# ВАРИАНТА 10
a = 0.0
b = 4.0
n = 8  # Для Симпсона n обязательно четное

h = (b - a) / n

# Метод парабол (формула 6.13)
# I = (h/3) * [ f(a) + 4*Σ_нечет + 2*Σ_чет + f(b) ]
sum_odd = 0.0
sum_even = 0.0

for i in range(1, n, 2):  # Нечетные узлы: 1, 3, 5, 7
    x_i = a + i * h
    sum_odd += f(x_i)

for i in range(2, n, 2):  # Четные узлы: 2, 4, 6
    x_i = a + i * h
    sum_even += f(x_i)

I_simp = (h / 3) * (f(a) + 4 * sum_odd + 2 * sum_even + f(b))

print("МЕТОД ПАРАБОЛ (СИМПСОНА) (Вариант 10)")
print(f"Пределы: [{a}, {b}], n = {n}, шаг h = {h:.4f}")
print(f"Результат: I = {I_simp:.6f}")