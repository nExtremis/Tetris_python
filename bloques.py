import pygame

from random import choice

bloque_azul = pygame.image.load("./img/azul.png")
bloque_azul = pygame.transform.scale(bloque_azul,(19,19))

bloque_celeste = pygame.image.load("./img/celeste.png")
bloque_celeste = pygame.transform.scale(bloque_celeste,(19,19))

bloque_naranja = pygame.image.load("./img/naranja.png")
bloque_naranja = pygame.transform.scale(bloque_naranja,(19,19))

bloque_purpura = pygame.image.load("./img/purpura.png")
bloque_purpura = pygame.transform.scale(bloque_purpura,(19,19))

bloque_rojo = pygame.image.load("./img/rojo.png")
bloque_rojo = pygame.transform.scale(bloque_rojo,(19,19))

bloque_verde =  pygame.image.load("./img/verde.png")
bloque_verde = pygame.transform.scale(bloque_verde,(19,19))

bloque_amarillo = pygame.image.load("./img/amarillo.png")
bloque_amarillo = pygame.transform.scale(bloque_amarillo,(19,19))

bloques_de_color = [bloque_verde,bloque_rojo,bloque_naranja,bloque_amarillo,bloque_purpura,bloque_celeste,bloque_azul]



nombres_de_colores = ["sky blue", "blue", "orange", "purple", "red", "green","yellow"]
