# Bots&Player.py
import pygame
import numpy as np
import random as rd
import Colisao as C
from tkinter import *

FPS = 60

Angle = (np.pi / 4)

def Randc():                                                # Randomiza uma Cor
    """ Randomiza uma Cor """
    return rd.uniform(0, 255)

#### Classes ####

class BOT:                                                  # Cria as características da classe Bot 
    def __init__(self, x, y, velocidade_i, distanciamento, id):
        self.raio = 15
        self.dist = distanciamento

        self.x = x
        self.y = y

        # Define as velocidades
        self.velocidade_i = velocidade_i
        self.v_x = 0
        self.v_y = 0
        self.lv_x = self.v_x
        self.lv_y = self.v_y

        self.color = (Randc(), Randc(), Randc())    # Randomiza a cor do Bot
        self.color_o = self.color                   # Armazena a cor original do Bot
        self.color_a = (255, 0, 0)                  # Define a cor vermelha como a cor de alerta

        self.collider = C.GCollider()               # Define as características e permite a colisão
        self.collider.swap = True                   # Permite a troca de velocidade entre Bots
        self.id = id                                # Identificação do Bot

        # Define a direção do Bot
        self.dir = 1
        if(rd.uniform(0, 1) >= 0.5):
            self.dir = -1

        # Randomiza o ângulo
        randAngle = rd.uniform(-Angle, Angle)

        # Randomiza velocidade
        self.randVelocidade = rd.uniform(self.velocidade_i/1.2, self.velocidade_i*1.2)
        self.v_x = self.dir * self.randVelocidade * np.cos(randAngle)
        self.v_y = self.randVelocidade * np.sin(randAngle)

class Player:                                               # Cria as características da classe Player
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.raio = r

        self.color = (255,20,147)                       # Define a cor do player
        self.color_o = self.color                       # Armazena a cor original
        self.color_a = (255, 0, 0)                      # Define Vermelho como a cor de alerta
        self.id = 0                                     # Define a identificação do player como 0

        self.collider = C.GCollider()                   # Define as características e permite a colisão
        self.collider.swap = False                      # NÃO Permite a troca de velocidade do player
        self.dist = 0                                   # Distanciamento incial de 0

        self.last_x = 0                                 # Armazena a velocidade no eixo x
        self.last_y = 0                                 # Armazena a velocidade no eixo y
        self.dir_x = 0                                  # Armazena a direção no eixo x
        self.dir_y = 0                                  # Armazena a direção no eixo y

#### Funções Bots #####

def ListaBot(n, dist, local):                               # Cria uma lista de [n] Bots com um distanciamento de [dist] em um determinado [local]
    lista = [] # Cria uma lista inicialmente vazia para os Bots
    for i in range(n):
        
        # Cria n bots com valores randomizados
        Bot = BOT( 
        rd.randint(local.x + 25, local.x - 25 + local.largura),
        rd.randint(local.y + 25, local.y - 25 + local.altura),
         (1 / FPS) * 3,
          dist,
           i+1)

        if len(lista) >= 1: # Se já houver um Bot na lista
            for Bot2 in lista: # Pega outro Bot
                if Bot != Bot2: # Caso esses Bots sejam diferentes
                    D = np.sqrt((Bot.x - Bot2.x)**2 +(Bot.y - Bot2.y)**2) # Calcula a distância entre eles
                    while D <= ((2 * Bot.raio) + (2* Bot.dist)): # Enquanto houver sobreposição, muda o x e y
                        Bot.x = rd.randint(local.x + 25, local.x - 25 + local.largura)
                        Bot.y = rd.randint(local.y + 25, local.y - 25 + local.altura)
                        D = np.sqrt((Bot.x - Bot2.x)**2 +(Bot.y - Bot2.y)**2) # Recalcula a distância
            lista.append(Bot) # Adiciona o Bot na Lista
        else:
            lista.append(Bot) # Adiciona o Bot na Lista
    return lista

def ListaAlerta(ListaBots):                                 # Cria uma lista de Rects dos Bots de [ListaBots] para alerta
    ListaDist = [] # Cria uma lista inicialmente vazia para Rects de Alerta
    for Bot in ListaBots:
        # Cria um Rect um pouco maior que o Bot, com base no Distanciamento
        b = pygame.Rect(((Bot.x - Bot.raio) - Bot.dist, (Bot.y - Bot.raio) - Bot.dist, (2*Bot.dist) + 2*Bot.raio, (2*Bot.dist) + 2*Bot.raio))
        ListaDist.append(b) # Adiciona o Rect na Lista
    return ListaDist

def AlertaB(ListaBots, ListaA):                             # Verifica o Distanciamento dos Bots de [ListaBots] e aciona o  Alerta
    for Rect in ListaA:                                                               
        colisao = Rect.collidelist(ListaA)                                                     # Verifica se a colisão ocorreu e retorna o indíce do objeto colidido
        Bot1 = ListaBots[ListaA.index(Rect)]                                                   # ListaB[ListaD.index(Rect)] acha o objeto oqual o Rect corresponde
        Bot2 = ListaBots[colisao]                                                              # ListaB[colisao] acha qual foi o objeto colidido
        if Rect != ListaA[colisao]:                                                            # Se os Rects pertencerem a objetos diferentes
            if colisao != -1:                                                                  # Se ocorrer colisão
                Bot1.color = Bot1.color_a                                                      # Muda para a cor de alerta
                Bot2.color = Bot2.color_a                                                    
        else:
            Bot1.color = Bot1.color_o                                                          # Volta para a cor original
            Bot2.color = Bot2.color_o

def DesenhaBots(ListaBots, screen):                         # Desenha [ListaBots] em uma tela [screen]
    for Bot in ListaBots:
        pygame.draw.circle(screen, Bot.color, (Bot.x, Bot.y ), Bot.raio)

def MovLimite(local, ListaBots, time):                      # Define o limite do movimento [ListaBots] em certo [local] com base em um certo [tempo]
    for Bot in ListaBots:                                 
        Bot.x += (Bot.v_x) * time                         # Movimenta o Bot
        Bot.y += (Bot.v_y) * time

        if(Bot.y < local.y + Bot.raio):                   # Colisão superior
            Bot.y = local.y + Bot.raio
            Bot.v_y = (-1)*Bot.v_y

        if(Bot.y > (local.y + local.altura) - Bot.raio):  # Colisão inferior
            Bot.y = (local.y + local.altura) - Bot.raio
            Bot.v_y = (-1)*Bot.v_y

        if(Bot.x < local.x + Bot.raio):                   # Colisão lateral (Esquerda)
            Bot.x = local.x + Bot.raio
            Bot.v_x = (-1)*Bot.v_x

        if(Bot.x > (local.x + local.largura) - Bot.raio): # Colisão lateral (Direita)
            Bot.x = (local.x + local.largura) - Bot.raio
            Bot.v_x = (-1)*Bot.v_x

#### Funções Player + Bots ####

def AlertaP(player, ListaBots, ListaA):                     # Verifica o Distanciamento do Bot de [ListaBots] com o player e aciona o  Alerta
    rectPlayer = pygame.Rect(((player.x - player.raio) - 8, (player.y - player.raio) - 8, player.raio*2 + 16, player.raio*2 + 16))                                                             
    colisao = rectPlayer.collidelist(ListaA)                                                    # Verifica se a colisão ocorreu e retorna o indíce do objeto colidido                                                  # ListaB[ListaD.index(Rect)] acha o objeto oqual o Rect corresponde
    Bot = ListaBots[colisao]                                                                    # ListaB[colisao] acha qual foi o objeto colidido                                                         # Se os Rects pertencerem a objetos diferentes
    if colisao != -1:                                                                           # Se ocorrer colisão
        player.color = player.color_a                                                           # Muda para a cor de alerta
        Bot.color = Bot.color_a                                                    
    else:
        player.color = player.color_o                                                           # Volta para a cor original
        Bot.color = Bot.color_o

def NPessoas(ListaBots, player, sala_atual):                # Conta nº de pessoas (Bot + player) na [sala_atual]
    RectSala = pygame.Rect(((sala_atual.x, sala_atual.y, sala_atual.largura, sala_atual.altura)))
    
    if RectSala.collidepoint(player.x, player.y): # Se o centro do player está na sala
        N = len(ListaBots) + 1
    else:
        N = len(ListaBots)
    return N

def MovePlayer(player, keys, time, screen):                 # Movimenta o Player por meio de WASD e salva sua direção

    # Calcula a direção de movimento
    player.dir_x = 0
    player.dir_y = 0

    if keys[pygame.K_d]:                                    # Movimento o player para a direita ao pressionar "D"
        player.dir_x += 1
                
    if keys[pygame.K_a]:                                    # Movimento o player para a esquerda ao pressionar "A"
        player.dir_x -= 1
                
    if keys[pygame.K_w]:                                    # Movimento o player para a cima ao pressionar "W"
        player.dir_y -= 1
                
    if keys[pygame.K_s]:                                    # Movimento o player para a direita ao pressionar "S"
        player.dir_y += 1

    if(player.dir_x != 0 and player.dir_y != 0):            # Normaliza o vetor direção
        tmp_normal = np.sqrt(np.power(player.dir_x, 2) + np.power(player.dir_y, 2))

        player.dir_x = player.dir_x / tmp_normal
        player.dir_y = player.dir_y / tmp_normal

    ####  Colisão por pixel  ####
    
    color = screen.get_at((             # Fornece a cor do pixel a frente do player
                                int(player.x + player.dir_x * player.raio*1.2),
                                int(player.y + player.dir_y * player.raio*1.2)
                            ))
    if(color != (70,130,180)):          # Se a cor do pixel for diferente da proibida, o Player se move
        if keys[pygame.K_d]:
            player.x += time*0.3
                
        if keys[pygame.K_a]:
            player.x -= time*0.3
                
        if keys[pygame.K_w]:
            player.y -= time*0.3
                
        if keys[pygame.K_s]:
            player.y += time*0.3

    #### Colisão por posição (Análise)  ####

def Atualiza(ListaBots, local, time, player, keys, screen): # Realiza todas as atualizações de [ListaBots] e [Player] em um determinado [local] com base em um certo [time]                
    ListaD = ListaAlerta(ListaBots)             # Cria uma Lista de Rects para alerta baseada em uma lista de Bots
    ListaGeral = ListaBots + [player]           # Cria uma lista geral de pessoas (Bots + player)

    AlertaB(ListaBots, ListaD)                  # Executa a função de Alerta entre os Bots
    AlertaP(player, ListaBots, ListaD)          # Executa a função de Alerta entre o Player e os Bots
    C.Colisao(ListaGeral)                       # Executa a colisão entre as pessoas (Bots + Player)

    MovLimite(local, ListaBots, time)           # Limita o movimento dos Bots dentro de um determinado local
    MovePlayer(player, keys, time, screen)      # Executa o movimento do player e define a colisão por cores

def Restaura(player, sala_atual, NPessoas, keys):           # Fecha a porta e permite a mudança de posição caso o limite ultrapasse
    # Cria um rect da Sala para colisão
    RectSala = pygame.Rect(((sala_atual.x, sala_atual.y, sala_atual.largura, sala_atual.altura)))

    # Se ultrapassar o limite máximo e o player estiver na sala
    if NPessoas >= (int((sala_atual).nmax)) and RectSala.collidepoint(player.x, player.y):
        porta_color = (70,130,180)             # Fecha a porta

        if keys[pygame.K_r]:                   # Permite a restauração da posição
            player.x = 50
            player.y = 480

    # Se ultrapassar o limite máximo, mas o player não está la
    elif NPessoas >= (int((sala_atual).nmax)):
        porta_color = (70,130,180)             # Simplismente fecha a porta

    else: # Caso contrário deixa aberta
        porta_color = (210, 180, 140)

    return(porta_color)

def AlertaAglo(screen, NP, sala_atual, player):             # Mostra o Alerta de aglomeração e o aviso da restauração
    # Cria um rect da Sala para colisão
    RectSala = pygame.Rect(((sala_atual.x, sala_atual.y, sala_atual.largura, sala_atual.altura)))
    
    aviso = pygame.image.load('Imagens/ATENÇÃO.png').convert()        # Importa a imagem de aviso (atenção)

    avisoR = pygame.image.load('Imagens/ATENÇÃO_R.png').convert()     # Importa a imagem de aviso com restauração

    # Define quando o alerta e o aviso da função Restauradora devem ser acionados
    if NP >= int((sala_atual).nmax) and RectSala.collidepoint(player.x, player.y):
        # Renderiza o Alerta com o aviso da função Restauradora
        screen.blit(avisoR, (5 , 45))

    elif NP >= int((sala_atual).nmax):
        # Renderiza  somente o Alerta
        screen.blit(aviso, (5 , 45))
        pass

    
