
# Интеграл: ∫[0, 4] (2x / (x^2 + 1)) dx, n = 8

def f(x):
    return (2 * x) / (x**2 + 1)

#  ВАРИАНТА 10
a = 0.0
b = 4.0
n = 8

h = (b - a) / n

# 1. Метод левых прямоугольников 
sum_left = 0.0
for i in range(n):
    x_i = a + i * h
    sum_left += f(x_i)
I_left = h * sum_left

# 2. Метод правых прямоугольников 
sum_right = 0.0
for i in range(1, n + 1):
    x_i = a + i * h
    sum_right += f(x_i)
I_right = h * sum_right

print("📐 МЕТОД ПРЯМОУГОЛЬНИКОВ (Вариант 10)")
print(f"Пределы: [{a}, {b}], n = {n}, шаг h = {h:.4f}")
print(f"Левые прямоугольники : I = {I_left:.6f}")
print(f"Правые прямоугольники: I = {I_right:.6f}")
print(f"Среднее значение     : I = {(I_left + I_right) / 2:.6f}")