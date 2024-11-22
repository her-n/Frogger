import pygame
import sys
import os
import random
import tkinter
from tkinter import messagebox

# Inicializar Pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Crear una pantalla
screen_info = pygame.display.Info()
ALTO = screen_info.current_h
ANCHO = screen_info.current_w
screen = pygame.display.set_mode((ANCHO, ALTO))

# Establecer el título de la ventana
pygame.display.set_caption("Frogger")

# Rutas de acceso de las imágenes
base_dir = os.path.dirname(os.path.abspath(__file__))

RUTA_JUGADOR = os.path.join(base_dir, "jugador.png")
RUTA_FONDO = os.path.join(base_dir, "calle.jpg")
RUTAS_COCHES = [os.path.join(base_dir, f"carro{i}.png") for i in range(1, 6)]
RUTA_HUEVO = os.path.join(base_dir, "huevo.png")

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Función para mostrar mensaje y salir
def gameover(perder):
    if not perder:
        pygame.quit()
        sys.exit()
    elif perder:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("GAME OVER", "Has Perdido, inténtalo de nuevo")
        root.destroy()
        pygame.quit()
        sys.exit()

# Clase del fondo
class Fondo:
    def __init__(self):
        self.image = pygame.image.load(RUTA_FONDO)
        self.image = pygame.transform.scale(self.image, (ANCHO, ALTO))
        self.rect = self.image.get_rect(topleft=(0, 0))

    def dibujar(self):
        screen.blit(self.image, self.rect)

# Clase del huevo (recompensas)
class Huevo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(RUTA_HUEVO)
        self.rect = self.image.get_rect(topleft=(x, y))

# Clase del jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(RUTA_JUGADOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidad = 4

    def dibujar(self):
        screen.blit(self.image, self.rect)
    
    def mover(self):    
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > ANCHO - self.rect.width:
            self.rect.x = ANCHO - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > ALTO - self.rect.height:
            self.rect.y = ALTO - self.rect.height

# Clase base para los coches
class Coche(pygame.sprite.Sprite):
    def __init__(self, y, direccion, color):
        super().__init__()
        self.color = color
        self.image = pygame.image.load(self.color)
        self.rect = self.image.get_rect(topleft=(ANCHO if direccion == 'izquierda' else -self.image.get_width(), y))
        self.velocidad = -4 if direccion == 'izquierda' else 4

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

# Crear una instancia del fondo
fondo1 = Fondo()

# Crear una instancia del jugador
jugador = Jugador(960, 1070)

# Grupos e instancias para los coches
coches_arriba2 = pygame.sprite.Group()
coches_abajo1 = pygame.sprite.Group()
coches_abajo2 = pygame.sprite.Group()
grupo_jugador = pygame.sprite.GroupSingle(jugador)
huevos = pygame.sprite.Group()

# Crear las instancias de los huevos
for i in range(10):
    huevo = Huevo(random.randint(0, ANCHO), random.randint(0, ALTO))
    huevos.add(huevo)

# Fuente para la puntuación
font = pygame.font.Font(None, 74)

# Puntuación inicial
puntuacion = 0

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Eventos y temporizadores de eventos
COCHE_ARRIBA2_EVENT = pygame.USEREVENT + 2
COCHE_ABAJO1_EVENT = pygame.USEREVENT + 3
COCHE_ABAJO2_EVENT = pygame.USEREVENT + 4
pygame.time.set_timer(COCHE_ARRIBA2_EVENT, random.randint(2000, 6000))
pygame.time.set_timer(COCHE_ABAJO1_EVENT, random.randint(2000, 6000))
pygame.time.set_timer(COCHE_ABAJO2_EVENT, random.randint(2000, 6000))

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover(False)
        elif event.type == COCHE_ARRIBA2_EVENT:
            coche2 = Coche(361, 'derecha', random.choice(RUTAS_COCHES))
            coches_arriba2.add(coche2)
        elif event.type == COCHE_ABAJO1_EVENT:
            coche3 = Coche(536, 'izquierda', random.choice(RUTAS_COCHES))
            coches_abajo1.add(coche3)
        elif event.type == COCHE_ABAJO2_EVENT:
            coche4 = Coche(720, 'derecha', random.choice(RUTAS_COCHES))
            coches_abajo2.add(coche4)

    # Llenar la pantalla con un color de fondo (por si acaso)
    screen.fill(BLANCO)

    # Obtener estado de las teclas
    keys = pygame.key.get_pressed()

    # Dibujar todos los objetos
    fondo1.dibujar()
    jugador.dibujar()

    # Funciones externas a dibujar de los objetos
    jugador.mover()

    # Colisiones con coches
    if (pygame.sprite.groupcollide(grupo_jugador, coches_arriba2, False, False) or 
        pygame.sprite.groupcollide(grupo_jugador, coches_abajo1, False, False) or 
        pygame.sprite.groupcollide(grupo_jugador, coches_abajo2, False, False)):
        gameover(True)

    # Colisiones con huevos
    colisiones_huevos = pygame.sprite.groupcollide(grupo_jugador, huevos, False, True)
    if colisiones_huevos:
        puntuacion += 1
        if puntuacion >= 10:
            gameover(False)

    # Actualizar coches
    coches_arriba2.update()
    coches_abajo1.update()
    coches_abajo2.update()

    # Dibujar coches y huevos
    coches_arriba2.draw(screen)
    coches_abajo1.draw(screen)
    coches_abajo2.draw(screen)
    huevos.draw(screen)

    # Mostrar la puntuación
    text = font.render(f"Puntuación: {puntuacion}", True, NEGRO)
    screen.blit(text, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar FPS
    clock.tick(60)