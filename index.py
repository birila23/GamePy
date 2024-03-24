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

caracteres = pygame.image.load("sprites/menina-n.png")

bloquinho = pygame.image.load("sprites/bloquinho2.png")

class Bloco(pygame.sprite.Sprite):
    def __init__(self, linha, coluna):
        pygame.sprite.Sprite.__init__(self)
        img_orig = bloquinho.subsurface((70 * 1, 70 * 1), (45, 45))
        self.image = pygame.transform.scale(img_orig, (BLOCO_LARGURA, BLOCO_ALTURA))
        x = coluna * BLOCO_LARGURA
        y = linha * BLOCO_ALTURA
        self.rect = pygame.Rect((x, y), (BLOCO_LARGURA, BLOCO_ALTURA))

# O sprite boy vai calcular a velocidade e também a posição, porém antes disso, ele irá testar a posição, se não puder, irá continuar na mesma posição.
class Girl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        girl_org = caracteres.subsurface((64 * 2, 64 * 2), (64, 64))
        self.image = pygame.transform.scale(girl_org, (BLOCO_LARGURA, BLOCO_ALTURA))
        self.rect = pygame.Rect((100, 100),(BLOCO_LARGURA, BLOCO_ALTURA))
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 0.009
        self.intencao_pos = list(self.rect.center)
  
    def moverDireita(self):
        self.vel_x = 1
        
    def moverEsquerda(self):
        self.vel_x = -1 
    
    def pular(self):
        self.vel_y = -1
        self.intencao_pos[1] += self.vel_y

    def update(self, *args):
        self.vel_y += self.gravidade
        self.intencao_pos[0] += self.vel_x
        self.intencao_pos[1] += self.vel_y

    def parar_horizontal(self):
        self.vel_x = 0
    
    def autorizar_movimento(self):
        self.rect.center = self.intencao_pos
    
    def recusar_movimento(self):
        self.intencao_pos = list(girl.rect.center)

    def teste_colisao(self, grupo):
        temp = self.rect.center
        self.rect.center = self.intencao_pos
        if not pygame.sprite.spritecollide(self, grupo, False):
            self.autorizar_movimento()
       
        else:
            self.recusar_movimento()
            self.vel_y = 0
            self.rect.center = temp
       
class Camera:
    def __init__(self, position, tamanho):
        self.window = pygame.Rect(position, tamanho)
        self.position = position
        self.offset_x = 0
        self.offset_y = 0
        self.clean_image = pygame.Surface(self.window.size)
        self.clean_image.fill((0, 0, 0))
        self.draw_area = pygame.Surface(self.window.size)

    def in_viewport(self, r):
        return self.window.colliderect(r)
    
    def move(self, pos):
        self.window.center = pos
        self.offset_x = self.window.x
        self.offset_y = self.window.y

    def start_drawing(self):
        self.draw_area.blit(self.clean_image, (0, 0))

    def paint(self, tela):
        tela.blit(self.draw_area, self.position)
        pygame.draw.rect(tela,(255, 0, 0), (self.position, self.window.size), 3)

    def draw_group(self, group):
        for s in group:
            if self.in_viewport(s.rect):
                self.draw_area.blit(s.image, (s.rect.x - self.offset_x, s.rect.y - self.offset_y))

girl = Girl()
principal = pygame.sprite.Group(girl)
blocos = pygame.sprite.Group()

#criar os sprites e colocar no grupo de blocos

for linha, lin in enumerate(mapinha): #pegar cada um dos elementos da matriz
    for coluna in range(0, 35):
        elemento = mapinha[linha][coluna]
        if elemento == "X": 
            bloco = Bloco(linha, coluna)
            blocos.add(bloco)

cam = Camera((0, 0), (largura, altura))
while True:
    #pinta cenario
    cam.start_drawing()
    cam.draw_group(blocos)
    cam.draw_group(principal)
    #tela.fill((0,0,0))
    #blocos.draw(tela)
    #principal.draw(tela)
    cam.paint(tela)
    pygame.display.update()

    #calcular regras
    principal.update()
    girl.teste_colisao(blocos)
    cam.move(girl.rect.center)

    #processa eventos
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
            