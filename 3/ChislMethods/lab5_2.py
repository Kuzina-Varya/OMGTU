import numpy as np

# Вариант 10
x_vals = np.array([0.083, 0.472, 1.347, 2.117, 2.947], dtype=float)
y_vals = np.array([-2.132, -2.013, -1.613, -0.842, 2.973], dtype=float)


def finite_differences(values):
    n = len(values)
    table = [values.copy()]
    current = values.copy()

    for _ in range(1, n):
        current = np.diff(current)
        table.append(current)

    return table


def divided_differences(x, y):
    n = len(x)
    table = np.zeros((n, n), dtype=float)
    table[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            table[i, j] = (table[i + 1, j - 1] - table[i, j - 1]) / (x[i + j] - x[i])

    return table


def print_finite_table(x, finite_table):
    n = len(x)
    print("=== Таблица конечных разностей ===")
    headers = ["xk", "yk", "Δyk", "Δ²yk", "Δ³yk", "Δ⁴yk"]
    print("{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}".format(*headers))

    for i in range(n):
        row = [f"{x[i]:.3f}"]
        for order in range(n):
            if i < len(finite_table[order]):
                row.append(f"{finite_table[order][i]:.6f}")
            else:
                row.append("")
        print("{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}".format(*row))


def print_divided_table(x, div_table):
    n = len(x)
    print("\n=== Таблица разделённых разностей ===")
    headers = ["xk", "yk", "1-го пор.", "2-го пор.", "3-го пор.", "4-го пор."]
    print("{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}".format(*headers))

    for i in range(n):
        row = [f"{x[i]:.3f}"]
        for j in range(n):
            if i < n - j:
                row.append(f"{div_table[i, j]:.6f}")
            else:
                row.append("")
        print("{:<10}{:<12}{:<12}{:<12}{:<12}{:<12}".format(*row))


def main():
    finite_table = finite_differences(y_vals)
    div_table = divided_differences(x_vals, y_vals)

    print_finite_table(x_vals, finite_table)
    print_divided_table(x_vals, div_table)


if __name__ == "__main__":
    main()