from typing import Any
import pygame
from pygame.sprite import Group

pygame.init()
largura, altura = 800, 600


BLOCO_LARGURA = largura//16
BLOCO_ALTURA = altura//12

mapinha = ['....................................',
    '....................................',
    '....................................',
    '....................................',
    '....................................',
    '....................................',
    '....................................',
    '....................................',
    '..........XXXXXXXX..................',
    '.............................XXXXXX.',
    '....................................',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXX.........',
    'XXXXXXXX...........XXXXXXXXX........',
    'XXXXXXXXX..........XXXXXXXXXX.......',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX.......',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
]

tela = pygame.display.set_mode((largura, altura), 0) 
pygame.display.set_caption("joguinho")

caracteres = pygame.image.load("./sprites/menina-n.png")

class Bloco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Girl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        girl_org = caracteres.subsurface((64 * 2, 64 * 2), (64, 64))
        self.image = pygame.transform.scale(girl_org, (BLOCO_LARGURA, BLOCO_ALTURA))
        self.rect = pygame.Rect((100, 100),(BLOCO_LARGURA, BLOCO_ALTURA))
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 0.009
  
    def moverDireita(self):
        self.vel_x = 1
        
    def moverEsquerda(self):
        self.vel_x = -1
    
    def pular(self):
        self.vel_y = -1

    def update(self, *args):
        self.vel_y += self.gravidade
        self.rect.centerx += self.vel_x
        self.rect.centery += self.vel_y

    def parar_horizontal(self):
        self.vel_x = 0

girl = Girl()
principal = pygame.sprite.Group(girl)

while True:
    for linha, lin in enumerate(mapinha):
        for coluna in range(0, 16):
            x = coluna * BLOCO_LARGURA
            y = linha * BLOCO_ALTURA
            bloco = mapinha[linha][coluna]
            cor = (0, 0 ,0)
            if bloco == "X":
                cor = (255,255, 0)
            pygame.draw.rect(tela, cor, ((x,y), (BLOCO_LARGURA, BLOCO_ALTURA)), 0)

    principal.draw(tela)

    pygame.display.update()

    principal.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                girl.moverDireita()
            if event.key == pygame.K_LEFT:
                girl.moverEsquerda()
            if event.key == pygame.K_SPACE:
                girl.pular()
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                girl.parar_horizontal()
            