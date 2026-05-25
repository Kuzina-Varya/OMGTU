# Краевая задача методом конечных разностей (прогонка) 
# Уравнение: y'' + x*y' - 2*y = 4
# Условия: y'(0.9) = 1, y'(1.2) = 0.8, h = 0.1

def p(x): return x
def q(x): return -2.0
def f_rhs(x): return 4.0

a, b = 0.9, 1.2
h = 0.1
ya_dash, yb_dash = 1.0, 0.8

def solve():
    n = int((b - a) / h)
    xs = [a + i * h for i in range(n + 1)]
    
    # Коэффициенты трехдиагональной системы: A[i]*y[i-1] + B[i]*y[i] + C[i]*y[i+1] = D[i]
    A = [0.0]*(n+1)
    B = [0.0]*(n+1)
    C = [0.0]*(n+1)
    D = [0.0]*(n+1)
    
    # Внутренние узлы (центральные разности для y' и y'')
    for i in range(1, n):
        x = xs[i]
        A[i] = 1/h**2 - p(x)/(2*h)
        B[i] = -2/h**2 + q(x)
        C[i] = 1/h**2 + p(x)/(2*h)
        D[i] = f_rhs(x)
        
    # Граничные условия 1-го рода через односторонние разности
    B[0] = -1.0; C[0] = 1.0; D[0] = h * ya_dash       # (-y0 + y1)/h = y'(a)
    A[n] = -1.0; B[n] = 1.0; D[n] = h * yb_dash       # (-y_{n-1} + yn)/h = y'(b)
    
    # Прямой ход прогонки
    alpha = [0.0]*(n+1)
    beta  = [0.0]*(n+1)
    y = [0.0]*(n+1)
    
    alpha[1] = -C[0] / B[0]
    beta[1]  =  D[0] / B[0]
    for i in range(1, n):
        denom = B[i] + A[i]*alpha[i]
        alpha[i+1] = -C[i] / denom
        beta[i+1]  = (D[i] - A[i]*beta[i]) / denom
        
    # Обратный ход
    y[n] = (D[n] - A[n]*beta[n]) / (B[n] + A[n]*alpha[n])
    for i in range(n-1, -1, -1):
        y[i] = alpha[i+1]*y[i+1] + beta[i+1]
        
    return xs, y

if __name__ == "__main__":
    xs, ys = solve()
    print("КРАЕВАЯ ЗАДАЧА (КОНЕЧНЫЕ РАЗНОСТИ) | ВАРИАНТ 10")
    print(f"{'x':^10} | {'y':^10}")
    print("-" * 22)
    for x, y in zip(xs, ys):
        print(f"{x:10.3f} | {y:10.6f}")