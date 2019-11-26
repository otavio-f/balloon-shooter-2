# -*- coding: cp1252 -*-
import pygame, os

'''
Modificacoes da versao desenvolvida na ultima oficina:
* Inserido metodo entity.collide_on
* Removido metodo entity.move
* Rotina de jogo movida para o metodo game()
'''

# Classe representa qualquer objeto do jogo
class entity(object):
    def draw(self, other):
        self.surface.blit(other.surface, other.rect)

    def collide_with(self, other):
        return self.rect.colliderect(other.rect)

    def collide_on(self, point):
        return self.rect.collidepoint(point)

# Metodo principal
def game(display):
    # Plano de fundo
    background = entity()

    background.rect = display.rect.copy()

    background.surface = pygame.Surface(background.rect.size)

    background.surface.fill(pygame.Color("skyblue"))

    # Chao do jogo
    ground = entity()

    ground.rect = display.rect.copy()

    ground.rect.y = 640

    ground.surface = pygame.Surface(ground.rect.size)

    ground.surface.fill(pygame.Color("springgreen2"))

    # Balao
    balloon = entity()

    balloon.surface = pygame.image.load(os.path.join("imagem", "baloes", "balloon 1.png"))

    balloon.rect = balloon.surface.get_rect()

    # Mira
    crosshair = entity()

    crosshair.surface = pygame.image.load(os.path.join("imagem", "mira", "crosshair.png"))

    crosshair.rect = crosshair.surface.get_rect()

    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break

        display.draw(background)

        display.draw(ground)

        display.draw(balloon)

        display.draw(crosshair)

        pygame.display.update()


pygame.init()
'''Inicializa os modulos do pygame'''

# Janela do jogo
display = entity()

display.rect = pygame.Rect((0,0), (1024, 768))

display.surface = pygame.display.set_mode(display.rect.size)

# Metodo do jogo
game(display)

pygame.quit()
'''Finaliza os modulos do pygame e faz qualquer limpeza necessaria'''
