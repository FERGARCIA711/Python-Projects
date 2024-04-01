# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 00:51:12 2024

@author: Fernando
"""

# Se da la bienvenida al usuario
print("¡Bienvenido a mi quiz!")

# Se le pregunta al usuario si quiere jugar
jugar = input("¿Quieres jugar...?").lower()
print(jugar)
if jugar != "sí":
    quit()
print("Ok, ¡juguemos!")

# Inicializamos el contador
puntuacion = 0

# Le preguntamos al usuario la primera pregunta
respuesta = input("¿Qúe significa el acrónimo CPU?").lower()
if respuesta == "unidad central de procesamiento":
    print("¡Correcto!")
    puntuacion += 1
else:
    print("Incorrecto")
    
# Le preguntamos al usuario la segunda pregunta
respuesta = input("¿Qúe significa el acrónimo GPU?").lower()
if respuesta == "unidad de procesamiento de gráficos":
    print("¡Correcto!")
    puntuacion += 1
else:
    print("Incorrecto")

# Le preguntamos al usuario la tercera pregunta
respuesta = input("¿Qué significa RAM?").lower()
if respuesta == "memoria de acceso aleatorio":
    print("¡Correcto!")
    puntuacion += 1
else:
    print("Incorrecto")
    
# Le preguntamos al usuario la cuarta pregunta
respuesta = input("¿Qué significa PSU?").lower()
if respuesta == "unidad de fuente de alimentación":
    print("¡Correcto!")
    puntuacion += 1
else:
    print("Incorrecto")
    
# Imprimimos la puntuación
print("Obtuviste " + str(puntuacion) + " respuestas correctas") 
print("Obtuviste un " + str(puntuacion/4*100) + "% correcto") 
   