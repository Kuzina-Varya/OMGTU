a = 0.5
b = 1.5

def f(x):
    return x**3 + 12*x - 12

count = 0

while abs(b - a) >= 0.01:
    f_a = f(a)
    # f_b удалено, так как не используется
    c = (a + b) / 2
    f_c = f(c)
    
    # Если знаки f(a) и f(c) совпадают, корень в правой части
    if (f_a > 0 and f_c > 0) or (f_a < 0 and f_c < 0):
        a = c
    else:
        b = c
    
    count += 1

root = (a + b) / 2
print(f"Итераций: {count}")
print(f"Корень: {root}")
print(f"Значение функции: {f(root)}")