import math

a = 2
b = -5
c = -7
b_2 = b**2
delta = b_2 -4 * a * c
raiz = math.sqrt(delta)
parte_de_cima_positivo = -b + raiz
parte_de_cima_negativo = -b - raiz
parte_de_baixo = 2 * a
x1 = parte_de_cima_positivo/parte_de_baixo
x2 = parte_de_cima_negativo/parte_de_baixo
print(x1, x2)



