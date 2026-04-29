import numpy as np
import matplotlib.pyplot as plt

# Вариант 10
x_vals = np.array([0.083, 0.472, 1.347, 2.117, 2.947], dtype=float)
y_vals = np.array([-2.132, -2.013, -1.613, -0.842, 2.973], dtype=float)


def lagrange_basis(x, i, nodes):
    result = 1.0
    for j in range(len(nodes)):
        if j != i:
            result *= (x - nodes[j]) / (nodes[i] - nodes[j])
    return result


def lagrange_polynomial(x, nodes, values):
    result = 0.0
    for i in range(len(nodes)):
        result += values[i] * lagrange_basis(x, i, nodes)
    return result


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


def linear_spline_coefficients(x, y):
    coeffs = []
    for i in range(len(x) - 1):
        a = (y[i + 1] - y[i]) / (x[i + 1] - x[i])
        b = y[i] - a * x[i]
        coeffs.append((a, b))
    return coeffs


def linear_spline(xp, x, coeffs):
    for i in range(len(x) - 1):
        if x[i] <= xp <= x[i + 1]:
            a, b = coeffs[i]
            return a * xp + b
    return None


def quadratic_spline_coefficients(x, y):
    quad_coeffs = []

    for start in [0, 2]:
        xs = x[start:start + 3]
        ys = y[start:start + 3]

        A = np.array([
            [xs[0] ** 2, xs[0], 1],
            [xs[1] ** 2, xs[1], 1],
            [xs[2] ** 2, xs[2], 1],
        ], dtype=float)

        coeff = np.linalg.solve(A, ys)
        quad_coeffs.append(coeff)

    return quad_coeffs


def quadratic_spline(xp, x, coeffs):
    if x[0] <= xp <= x[2]:
        a, b, c = coeffs[0]
        return a * xp ** 2 + b * xp + c
    elif x[2] <= xp <= x[4]:
        a, b, c = coeffs[1]
        return a * xp ** 2 + b * xp + c
    return None


def main():
    diff_table = divided_differences(x_vals, y_vals)
    lin_coeffs = linear_spline_coefficients(x_vals, y_vals)
    quad_coeffs = quadratic_spline_coefficients(x_vals, y_vals)

    x_plot = np.linspace(x_vals[0], x_vals[-1], 500)

    y_lagrange = [lagrange_polynomial(x, x_vals, y_vals) for x in x_plot]
    y_newton = [newton_polynomial(x, x_vals, diff_table) for x in x_plot]
    y_linear = [linear_spline(x, x_vals, lin_coeffs) for x in x_plot]
    y_quad = [quadratic_spline(x, x_vals, quad_coeffs) for x in x_plot]

    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_lagrange, label="Полином Лагранжа")
    plt.plot(x_plot, y_newton, label="Полином Ньютона")
    plt.plot(x_plot, y_linear, label="Линейный сплайн")
    plt.plot(x_plot, y_quad, label="Квадратичный сплайн")
    plt.scatter(x_vals, y_vals, label="Узлы интерполяции")
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Графики полиномов и сплайнов")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()