# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 01:09:53 2024

@author: Fernando
"""

# Importamos librerias 
import random

# Pedimos al usuario que introduzca las cotas
c_inf = input("Introduzca la cota inferior del rango: ")
c_sup = input("Introduzca la cota superior del rango: ")

# Colocamos las condiciones para las cotas
if c_inf.isdigit():
    c_inf = int(c_inf)
    if c_inf <= 0:
        print("Porfavor introduzca un número mayor a 0 la próxima vez.")
        quit()
    c_sup = int(c_sup)
    if c_sup <= 0:
        print("Porfavor introduzca un número mayor a 0 la próxima vez.")
        quit()
else:
    print("Porfavor introduzca un número la próxima vez.")
    quit()

# Creamos el número aleatorio
numero = random.randint(c_inf,c_sup)

# Inicializamos el conteo de intentos
n = 0

# Pedimos al usuario que adivine el número
while True:
    n +=1    
    x = input("Adivina el número: ")
    if x.isdigit():
        x = int(x)
    else:
        print("Porfavor introduce un número la próxima vez.")
        continue
    if x == numero:
        print("¡Lo adivinaste!")
        break
    else:
        print("No lo has adivinado.")
    
# Imprimimos el conteo de intentos
print("Lo adivinzaste en", n, "oportunidades.")


