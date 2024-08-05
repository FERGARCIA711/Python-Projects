# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:56:21 2023

@author: Carlos Fernando García Vega
"""

# Importamos librerias
import numpy as np
import math 
import pygame
import sys

# Obtenemos la duración de la simulación y el paso del tiempo 
"""
Se recomienda ajustar los valores de duración = 60s y el paso = 0.01s. Esto 
dará una buena vista de cómo funciona la simulación.
"""
duracion = float(input("Ingrese la duración de la simulación en segundos: "))
paso = float(input("Ingrese el paso del tiempo en segundos: "))

# Inicializamos Pygame
pygame.init()

# Definimos constantes globales de PyGame
WIDTH, HEIGHT = 1000,1000                       # Altura y Ancho de la ventana
WIN = pygame.display.set_mode((WIDTH,HEIGHT))   # Creamos el objeto ventana
CLOCK = pygame.time.Clock()                     # Creamos el reloj
FPS = 60                                        # Frames Per Second

# Definimos los colores que usaremos
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)
GRIS = (128, 128, 128)
NARANJA = (255,165,0)
AZUL = (100, 149, 237)
ROJO = (188, 39, 50)
CAFE = (150, 75, 0)
ARENA = (236,204,162)
CIAN = (0, 255, 255)
AZUL_M = (0, 42, 119)

# Definimos el tipo de fuente que usaremos en la simulación
FONT = pygame.font.SysFont("arial", 26)

# Definimos la clase "Planeta" para representar a los cuerpos celestes
class Planeta:
    # Definimos algunas constantes que usaremos
	UA = 149.59e6 * 1000   # Unidad Astronómica
	G = 6.67430e-11        # Constante de la Gravedad
	ESCALA = 280 / UA      # 1UA = 100 pixels. 
	"""
	EN ESTE CASO SE AJUSTÓ LA ESCALA DE MODO QUE FUERAN VISIBLES SOLAMENTE 
    EL SOL Y CUATRO PLANETAS. SIN EMBARGO, SI LA ESCALA SE REAJUSTA A 15/UA ES 
    POSIBLE OBSERVAR A TODOS LOS PLANETAS DEL SISTEMA SOLAR.
	""" 
	TIMESTEP = 3600*24     # 1 día
    
	def __init__(self, x, y, masa, radio, color):
        # Iniciamos las coordenadas del planeta en el espacio
		self.x = x                  # Posición en x del planeta
		self.y = y                  # Posición en y del planeta
        # Iniciamos las componentes de la velocidad del planeta en las direcciones x e y (comienzan en cero)
		self.v_x = 0                # Velocidad en x del planeta
		self.v_y = 0                # Velocidad en y del planeta
        # Propiedades físicas del planeta
		self.masa = masa            # Masa del planeta
		self.radio = radio          # Radio del planeta (no a escala)
		self.color = color          # Color del planeta
        # Propiedades adicionales
		self.sol = False            # Indica si el planeta es el sol o no
		self.distancia_al_sol = 0   # Almacena la distancia al sol
		self.orbita = []            # Creamos una lista para almacenar las coordenadas de la órbita de los planetas

    # Hacemos una función para dibujar el planeta en la ventana de la simulación
	def dibujar(self, win):
        # Ajustamos las coordenadas a la escala de la ventana
		x = self.x * self.ESCALA + WIDTH / 2
		y = self.y * self.ESCALA + HEIGHT / 2
        # Verificamos que haya suficientes puntos en la órbita para dibujar las líneas
		if len(self.orbita) > 2:
            # Creamos una lista de puntos actualizados 
			puntos_actualizados = []
			for punto in self.orbita:
                # Extraemos las coordenadas (x, y) del punto en la órbita
				x, y = punto
                # Ajustamos las coordenadas del punto a la escala de la ventana
				x = x * self.ESCALA + WIDTH / 2
				y = y * self.ESCALA + HEIGHT / 2
                # Agregamos las coordenadas ajustadas a la lista de puntos actualizados
				puntos_actualizados.append((x, y))
            # Dibujamos la órbita del planeta
			pygame.draw.lines(win, self.color, False, puntos_actualizados, 2)
        # Dibujamos el planeta
		pygame.draw.circle(win, self.color, (x, y), self.radio)
        # Mostramos la distancia de cada planeta al sol 
		if not self.sol:
			distancia = round(self.distancia_al_sol / 1000, 1)      
			texto = FONT.render(f"{distancia} km", 1, BLANCO)
			win.blit(texto, (x - texto.get_width()/2, y - texto.get_height()/2))

    # Definimos una fuunción para calcular las fuerzas gravitacionales entre planetas
	def atraccion(self, otro):
        # Definimos las coordenadas del otro planeta
		otro_x, otro_y = otro.x, otro.y
        # Definimos las distancias en x e y entre este planeta y el otro
		distancia_x = otro_x - self.x
		distancia_y = otro_y - self.y
        # Calculamos la distancia entre los dos planetas
		distancia = np.sqrt(distancia_x ** 2 + distancia_y ** 2)
        # Actualizamos la distancia al sol 
		if otro.sol:
			self.distancia_al_sol = distancia
        # Calculamos la magnitud de la fuerza gravitacional entre dos planetas usando la ley de la gravitación universal
		fuerza = self.G * self.masa * otro.masa / distancia**2        
        # Calculamos las componentes de la fuerza en las direcciones x e y
		theta = math.atan2(distancia_y, distancia_x)
		fuerza_x = np.cos(theta) * fuerza
		fuerza_y = np.sin(theta) * fuerza
		return fuerza_x, fuerza_y

    # Definimos una función para actualizar la posición del planeta en función de las fuerzas gravitacionales
	def actualizar_posicion(self, planetas):
        # Iniciamos las fuerzas totales en ambas direcciones en cero
		total_fx = total_fy = 0
        # Al calcular la fuerza gravitacional evitamos calcular la atracción de un planeta consigo mismo
		for planeta in planetas:
			if self == planeta:
				continue
            # Calculamos la fuerza gravitacional entre planetas
			fx, fy = self.atraccion(planeta)
            # Sumamos las fuerzas en ambas direcciones
			total_fx += fx
			total_fy += fy
       
        # Utilizamos el método de Euler para actualizar las componentes de la velocidad del planeta.
		"""
		La velocidad se actualiza sumando las fuerzas totales divididas		
        por la masa del planeta (segunda ley de Newton) y multiplicadas por el 
        paso de tiempo. Esto utiliza la aproximación de Euler para resolver 
        ecuaciones diferenciales ordinarias.
		"""
		self.v_x += total_fx / self.masa * self.TIMESTEP
		self.v_y += total_fy / self.masa * self.TIMESTEP
		# Utilizamos el método de Euler para actualizar las coordenadas del planeta en función de su velocidad actual.
		"""
        Multiplicamos la velocidad por el paso de tiempo para obtener el cambio
        en posición. Esto utiliza la aproximación de Euler para la integración 
        numérica.
		"""
		self.x += self.v_x * self.TIMESTEP
		self.y += self.v_y * self.TIMESTEP
        # Agregamos las nuevas coordenadas a la lista de la órbita
		self.orbita.append((self.x, self.y))

# Definimos la función principal
def main():
    # Definimos al sol y los planetas
	sol = Planeta( 0, 0, 1.988500 * 10**30, 30, AMARILLO)
	sol.sol = True
    
	mercurio = Planeta(0.387 * Planeta.UA, 0, 3.3010 * 10**23, 8, GRIS)
	mercurio.v_y = -47.36 * 1000

	venus = Planeta(0.723 * Planeta.UA, 0, 4.8673 * 10**24, 14, NARANJA)
	venus.v_y = -35.02 * 1000    

	tierra = Planeta(-1 * Planeta.UA, 0, 5.9722 * 10**24, 16, AZUL)
	tierra.v_y = 29.783 * 1000 

	marte = Planeta(-1.524 * Planeta.UA, 0, 6.4169 * 10**23, 12, ROJO)
	marte.v_y = 24.077 * 1000
    
	jupiter = Planeta(-5.2 * Planeta.UA, 0, 1.89813 * 10**27, 19, CAFE)
	jupiter.v_y = 13.06 * 1000

	saturno = Planeta(-9.538 * Planeta.UA, 0, 5.6832 * 10**26, 18, ARENA)
	saturno.v_y = 9.67 * 1000

	urano = Planeta(-19.8 * Planeta.UA, 0, 8.6811 * 10**25, 17, CIAN)
	urano.v_y = 6.79 * 1000

	neptuno = Planeta(-30.07 * Planeta.UA, 0, 1.02409 * 10**26, 17, AZUL_M)
	neptuno.v_y = 5.45 * 1000       
	"""
	En este caso, toda la información de los cuerpos celestes fue extraída de 
    la página de la NASA, excepto por los radios, a los cuales se les asignaron
    valores arbitrarios (no a escala) para intentar recrear una representación 
    visual aproximada de las dimensiones de los planetas y el sol.
	"""
    
    # Creamos una lista de los planetas
	planetas = [sol, mercurio, venus, tierra, marte, jupiter, saturno, urano, neptuno]

	# Calculamos el número total de pasos de tiempo en la simulación
	total = int(duracion / paso)

    # Definimos el bucle principal de la simulación
	for step in range(total):
        # Controlamos la velocidad de la simulación ajustando el reloj según los FPS
		CLOCK.tick(FPS)
        # Hacemos que la ventana tenga un color de fondo negro
		WIN.fill((10, 10, 10))

        # Terminamos el bucle principal de la simulación para cerrar el programa
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()               

        # Actualizamos la posición de cada planeta en función de las fuerzas gravitacionales de los otros planetas
		for planeta in planetas:
			planeta.actualizar_posicion(planetas)
            # Dibujamos el planeta en la ventana de la simulación
			planeta.dibujar(WIN)

        # Actualizamos la pantalla de la simulación
		pygame.display.update()

    # Cerramos Pygame al finalizar la simulación
	pygame.quit()
    
# Ejecutamos la función principal
main()
