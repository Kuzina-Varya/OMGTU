import numpy as np
import matplotlib.pyplot as plt

# Вариант 10
x_vals = np.array([0.083, 0.472, 1.347, 2.117, 2.947], dtype=float)
y_vals = np.array([-2.132, -2.013, -1.613, -0.842, 2.973], dtype=float)


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
    # 2 куска:
    # 1-й на [x0, x2]
    # 2-й на [x2, x4]
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
    print("=== Линейный сплайн ===")
    lin_coeffs = linear_spline_coefficients(x_vals, y_vals)
    for i, (a, b) in enumerate(lin_coeffs, start=1):
        print(f"На [{x_vals[i-1]:.3f}, {x_vals[i]:.3f}]: phi{i}(x) = {a:.6f}*x + {b:.6f}")

    print("\n=== Квадратичный сплайн ===")
    quad_coeffs = quadratic_spline_coefficients(x_vals, y_vals)
    print(f"На [{x_vals[0]:.3f}, {x_vals[2]:.3f}]: "
          f"phi1(x) = {quad_coeffs[0][0]:.6f}*x^2 + {quad_coeffs[0][1]:.6f}*x + {quad_coeffs[0][2]:.6f}")
    print(f"На [{x_vals[2]:.3f}, {x_vals[4]:.3f}]: "
          f"phi2(x) = {quad_coeffs[1][0]:.6f}*x^2 + {quad_coeffs[1][1]:.6f}*x + {quad_coeffs[1][2]:.6f}")

    x_linear = []
    y_linear = []
    for i in range(len(x_vals) - 1):
        segment = np.linspace(x_vals[i], x_vals[i + 1], 100)
        for xp in segment:
            x_linear.append(xp)
            y_linear.append(linear_spline(xp, x_vals, lin_coeffs))

    x_quad_1 = np.linspace(x_vals[0], x_vals[2], 200)
    y_quad_1 = [quadratic_spline(xp, x_vals, quad_coeffs) for xp in x_quad_1]

    x_quad_2 = np.linspace(x_vals[2], x_vals[4], 200)
    y_quad_2 = [quadratic_spline(xp, x_vals, quad_coeffs) for xp in x_quad_2]

    plt.figure(figsize=(10, 6))
    plt.plot(x_linear, y_linear, label="Линейный сплайн")
    plt.plot(x_quad_1, y_quad_1, label="Квадратичный сплайн")
    plt.plot(x_quad_2, y_quad_2)
    plt.scatter(x_vals, y_vals, label="Узлы интерполяции")
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Линейный и квадратичный сплайны")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()