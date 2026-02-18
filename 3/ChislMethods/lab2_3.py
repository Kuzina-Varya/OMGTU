from sympy import symbols, diff, lambdify

x = symbols('x')
# Символьное выражение (для производных)
f_expr = x**3 + 12*x - 12

# Числовая функция (для вычислений в точках)
f = lambdify(x, f_expr, 'numpy')

a = 0.5
b = 1.5

m=1.01 * f(b)
count = 0
x1=b
x0=a

while abs(x1-x0)>0.01:
    if(m!=0):
        x0=x1
        x1=x0-f(x0)/m
        count+=1
    else:
        print ("m=0")
        break

print ("Корень: ", x1)
print ("Количество итераций: ", count)


