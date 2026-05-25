# Метод Эйлера для задачи Коши
def f(x, y):
    return y - x**2  # y' = y - x^2

x0, y0 = -1.0, 1.0
x_end = 2.0
h = 0.6

def solve():
    n = int((x_end - x0) / h)
    xs = [x0 + i * h for i in range(n + 1)]
    ys = [0.0] * (n + 1)
    ys[0] = y0
    for i in range(n):
        ys[i+1] = ys[i] + h * f(xs[i], ys[i])
    return xs, ys

if __name__ == "__main__":
    xs, ys = solve()
    print("МЕТОД ЭЙЛЕРА | ВАРИАНТ 10")
    print(f"{'x':^10} | {'y':^10}")
    print("-" * 22)
    for x, y in zip(xs, ys):
        print(f"{x:10.3f} | {y:10.6f}")