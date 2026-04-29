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


def main():
    print("=== Полином Лагранжа ===")
    print("x =", x_vals)
    print("y =", y_vals)

    x_star = x_vals[1] + x_vals[2]
    l_value = lagrange_polynomial(x_star, x_vals, y_vals)

    print(f"\nТочка x1 + x2 = {x_vals[1]} + {x_vals[2]} = {x_star}")
    print(f"L4(x1 + x2) = {l_value:.6f}")

    x_plot = np.linspace(x_vals[0] - 0.2, x_vals[-1] + 0.2, 400)
    y_plot = [lagrange_polynomial(x, x_vals, y_vals) for x in x_plot]

    plt.figure(figsize=(10, 6))
    plt.plot(x_plot, y_plot, label="Полином Лагранжа")
    plt.scatter(x_vals, y_vals, label="Узлы интерполяции")
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Интерполяционный многочлен Лагранжа")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()