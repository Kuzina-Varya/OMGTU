# Метод Рунге-Кутта 4-го порядка 
def f(x, y):
    return y - x**2

x0, y0 = -1.0, 1.0
x_end = 2.0
h = 0.6

def solve():
    n = int((x_end - x0) / h)
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [0.0] * (n + 1)
    ys[0] = y0
    for i in range(n):
        k0 = h * f(xs[i], ys[i])
        k1 = h * f(xs[i] + h/2, ys[i] + k0/2)
        k2 = h * f(xs[i] + h/2, ys[i] + k1/2)
        k3 = h * f(xs[i] + h, ys[i] + k2)
        ys[i+1] = ys[i] + (k0 + 2*k1 + 2*k2 + k3) / 6
    return xs, ys

if __name__ == "__main__":
    xs, ys = solve()
    print("МЕТОД РУНГЕ-КУТТА (4 ПОРЯДОК) | ВАРИАНТ 10")
    print(f"{'x':^10} | {'y':^10}")
    print("-" * 22)
    for x, y in zip(xs, ys):
        print(f"{x:10.3f} | {y:10.6f}")