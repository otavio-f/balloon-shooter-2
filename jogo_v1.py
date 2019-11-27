# -*- coding: cp1252 -*-
import pygame, os, random

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

# Gera um balao de tamanho e posicao aleatorios
def gen_random_balloon(max_size, area_rect, balloon_models):
    balloon = entity()

    balloon.surface = random.choice(balloon_models)
    
    size = random.randint(int(max_size/2), max_size)
    
    balloon.surface = pygame.transform.smoothscale(balloon.surface, (size, size))

    balloon.rect = balloon.surface.get_rect()

    balloon.rect.x = random.randint(0, area_rect.width - balloon.rect.width)

    balloon.rect.y = area_rect.height - 1

    return balloon


'''
Jogo
'''
def game(display, resources):
    #Plano de fundo
    background = entity()

    background.rect = display.rect.copy()

    background.surface = pygame.Surface(background.rect.size)

    background.surface.fill(pygame.Color("skyblue"))

    #Chao do jogo
    ground = entity()

    ground.rect = pygame.Rect((0,640), display.rect.size)

    ground.surface = pygame.Surface(ground.rect.size)

    ground.surface.fill(pygame.Color("springgreen2"))

    # Balao
    balloon = gen_random_balloon(100, display.rect, resources["balloons"])
    
    # Mira
    crosshair = entity()

    crosshair.surface = resources["crosshair"]

    crosshair.rect = crosshair.surface.get_rect()

    crosshair.rect.center = pygame.mouse.get_pos()

    # Mouse
    pygame.mouse.set_visible(False)

    # Nivel e pontuacao
    level = 1
    points = 0
    is_paused = False

    # Painel de pontuacao
    panel = entity()

    panel.surface = resources["font"]["medium"].render("Pontos: {}".format(points),
                                                              True,
                                                              pygame.Color("Red"))
    
    panel.rect = panel.surface.get_rect()
    
    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_paused = not is_paused
        elif event.type == pygame.MOUSEMOTION:
            crosshair.rect.center = pygame.mouse.get_pos()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if balloon.collide_on(crosshair.rect.center) and not is_paused:
                resources["sounds"]["pop"].play()
                points += 1
                if points%3 == 0:
                    level += 1
                panel.surface = resources["font"]["medium"].render("Pontos: {}".format(points),
                                                              True,
                                                              pygame.Color("red"))
                balloon = gen_random_balloon(100, display.rect, resources["balloons"])
            else:
                resources["sounds"]["empty shot"].play()

        if not display.collide_with(balloon):
            pygame.mouse.set_visible(True)
            game_over(display, resources, points)
            break

        if not is_paused:
            balloon.rect.y -= 5+level

        display.draw(background)

        display.draw(ground)
        
        display.draw(panel)

        display.draw(balloon)
        
        display.draw(crosshair)

        pygame.display.update()

        resources["clock"].tick(30)

'''
Tela inicial
'''
def welcome(display, resources):
    #Plano de fundo
    background = entity()

    background.rect = display.rect.copy()

    background.surface = pygame.Surface(background.rect.size)

    background.surface.fill(pygame.Color("skyblue"))

    #Chao do jogo
    ground = entity()

    ground.rect = pygame.Rect((0,640), display.rect.size)

    ground.surface = pygame.Surface(ground.rect.size)

    ground.surface.fill(pygame.Color("springgreen2"))

    #Camada escura
    overlay = entity()

    overlay.rect = display.rect.copy()

    overlay.surface = pygame.Surface(overlay.rect.size)

    overlay.surface.fill(pygame.Color("black"))

    overlay.surface.set_alpha(32)
    
    # Balao
    balloon = gen_random_balloon(100, display.rect, resources["balloons"])
    
    # Painel: Entrar
    play_text = entity()

    play_text.surface = resources["font"]["big"].render("Jogar", True, pygame.Color("palegreen"))

    play_text.rect = play_text.surface.get_rect()

    play_text.rect.center = background.rect.center

    # Painel: Sair
    exit_text = entity()

    exit_text.surface = resources["font"]["medium"].render("Sair", True, pygame.Color("red"))

    exit_text.rect = exit_text.surface.get_rect()

    exit_text.rect.midtop = play_text.rect.midbottom
    
    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if play_text.collide_on(pygame.mouse.get_pos()):
                game(display, resources)
                break
            elif exit_text.collide_on(pygame.mouse.get_pos()):
                break
            
        if not display.collide_with(balloon):
            balloon = gen_random_balloon(120, display.rect, resources["balloons"])

        balloon.rect.y -= random.randint(5,20)

        display.draw(background)

        display.draw(ground)

        display.draw(balloon)

        display.draw(overlay)
        
        display.draw(play_text)

        display.draw(exit_text)

        pygame.display.update()

        resources["clock"].tick(30)

'''
Game over
'''
def game_over(display, resources, points):
    #Plano de fundo
    background = entity()

    background.rect = display.rect.copy()

    background.surface = pygame.Surface(background.rect.size)

    background.surface.fill(pygame.Color("skyblue"))

    #Chao do jogo
    ground = entity()

    ground.rect = pygame.Rect((0,640), display.rect.size)

    ground.surface = pygame.Surface(ground.rect.size)

    ground.surface.fill(pygame.Color("springgreen2"))

    #Camada escura
    overlay = entity()

    overlay.rect = display.rect.copy()

    overlay.surface = pygame.Surface(overlay.rect.size)

    overlay.surface.fill(pygame.Color("black"))

    overlay.surface.set_alpha(64)

    # Painel: GameOver
    game_over_text = entity()

    game_over_text.surface = resources["font"]["big"].render("Game Over", True, pygame.Color("black"))

    game_over_text.rect = game_over_text.surface.get_rect()

    game_over_text.rect.center = background.rect.center

    # Painel: Pontos
    points_text = entity()

    if points == 0:
        text = "Você não fez nenhum ponto."
    elif points == 1:
        text = "Você fez 1 ponto."
    else:
        text = "Você fez {} pontos!".format(points)

    points_text.surface = resources["font"]["small"].render(text, True, pygame.Color("palegreen"))

    points_text.rect = points_text.surface.get_rect()

    points_text.rect.midtop = game_over_text.rect.midbottom
    
    # Painel: Tentar novamente
    play_text = entity()

    play_text.surface = resources["font"]["medium"].render("Tentar novamente?", True, pygame.Color("palegreen"))

    play_text.rect = play_text.surface.get_rect()

    play_text.rect.midtop = points_text.rect.midbottom

    # Painel: Sair
    exit_text = entity()

    exit_text.surface = resources["font"]["medium"].render("Sair", True, pygame.Color("red"))

    exit_text.rect = exit_text.surface.get_rect()

    exit_text.rect.midtop = play_text.rect.midbottom
    
    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if play_text.collide_on(pygame.mouse.get_pos()):
                game(display, resources)
                break
            elif exit_text.collide_on(pygame.mouse.get_pos()):
                break

        display.draw(background)

        display.draw(ground)

        display.draw(overlay)

        display.draw(game_over_text)
        
        display.draw(points_text)
        
        display.draw(play_text)

        display.draw(exit_text)

        pygame.display.update()

        resources["clock"].tick(30)


pygame.display.init()
pygame.font.init()
pygame.mixer.init(buffer=256)
'''Inicializa os modulos do pygame'''

#Pre-carregamento
resources = {
    "balloons": [],
    "crosshair": pygame.image.load(os.path.join("imagem", "mira", "crosshair.png")),
    "sounds": {},
    "font": {
        "big": pygame.font.Font(os.path.join("fonte", "interface", "Clausly.ttf"), 130),
        "medium": pygame.font.Font(os.path.join("fonte", "interface", "Clausly.ttf"), 80),
        "small": pygame.font.Font(os.path.join("fonte", "interface", "Clausly.ttf"), 50)
        },
    "clock" : pygame.time.Clock()
    }

for img in os.listdir(os.path.join("imagem", "baloes")):
    resources["balloons"].append(pygame.image.load(os.path.join("imagem", "baloes", img)))

for snd in os.listdir(os.path.join("som", "sfx")):
    resources["sounds"].update(
        {os.path.splitext(snd)[0]: pygame.mixer.Sound(os.path.join("som", "sfx", snd))}
        )

#Janela do jogo
display = entity()

display.rect = pygame.Rect((0,0), (1024, 768))

display.surface = pygame.display.set_mode(display.rect.size)

pygame.display.set_caption("Balloon Shooter")

#Metodo do jogo
welcome(display, resources)

pygame.quit()
'''Finaliza os modulos do pygame e faz qualquer limpeza necessaria'''
