import numpy as np
import matplotlib.pyplot as plt

# Вариант 10
x_vals = np.array([0.083, 0.472, 1.347, 2.117, 2.947], dtype=float)
y_vals = np.array([-2.132, -2.013, -1.613, -0.842, 2.973], dtype=float)


def divided_differences(x, y):
    n = len(x)
    table = np.zeros((n, n), dtype=float)
    table[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = (table[i + 1, j - 1] - table[i, j - 1]) / (x[i + j] - x[i])

    return table


def newton_polynomial(x, nodes, diff_table):
    n = len(nodes)
    result = diff_table[0, 0]
    product = 1.0

    for i in range(1, n):
        product *= (x - nodes[i - 1])
        result += diff_table[0, i] * product

    return result


def main():
    diff_table = divided_differences(x_vals, y_vals)

    print("=== Полином Ньютона ===")
    print("Коэффициенты из первой строки таблицы разделённых разностей:")
    for i in range(len(x_vals)):
        print(f"a{i} = {diff_table[0, i]:.6f}")

    x_star = x_vals[1] + x_vals[2]
    n_value = newton_polynomial(x_star, x_vals, diff_table)

    print(f"\nТочка x1 + x2 = {x_vals[1]} + {x_vals[2]} = {x_star}")
    print(f"N4(x1 + x2) = {n_value:.6f}")

    x_plot = np.linspace(x_vals[0] - 0.2, x_vals[-1] + 0.2, 400)
    y_plot = [newton_polynomial(x, x_vals, diff_table) for x in x_plot]

    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, label="Полином Ньютона")
    plt.scatter(x_vals, y_vals, label="Узлы интерполяции")
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Интерполяционный многочлен Ньютона")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()