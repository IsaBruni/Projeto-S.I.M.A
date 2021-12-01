# Mapa.py
import pygame

class Porta:                            # Cria a classe das Portas
    def __init__(self, x, y, largura, altura, id=-1):  # Define as características básicas das Portas
       self.x = x
       self.y = y
       self.altura = altura
       self.largura = largura
       self.id = id # Identificação do destino da Porta

class Sala:                             # Cria a classe das Salas
    def __init__(self, x, y, largura, altura):  # Define as características básicas das Salas
       self.x = x
       self.y = y
       self.altura = altura
       self.largura = largura
       self.nmax = 0

class Corredor:                         # Cria a classe dos corredores
    def __init__(self, x, y, largura, altura):  # Define as características básicas dos Corredores
       self.x = x
       self.y = y
       self.altura = altura
       self.largura = largura
       self.porta = []

    def addPorta(self, porta):                  # Adiciona a porta
        self.porta.append(porta)    

    def VerificaPorta(self, player):            # Verifica se o player passou pela porta e retorna o Id da porta colidida
      for porta in self.porta: 
        rectporta = pygame.Rect((porta.x + self.x, porta.y + self.y, porta.largura, porta.altura))
        if player.colliderect(rectporta):
            return porta.id
      return None

class Mapa:                             # Cria a classe dos Bots
    def __init__(self, start_x, start_y, id): # Define as características básicas dos Mapas
       self.start_x = start_x
       self.start_y = start_y
       self.id = id
       self.salas = []
       self.corredores = []

    def addSala(self, sala):                  # Adiciona a sala
        self.salas.append(sala)    

    def addCorredor(self, corredor):          # Adiciona o corredor
        self.corredores.append(corredor)

def DesenhaMapa(Mapa, screen):          # Desenha o mapa atual com suas salas e corredores
    """
    Função responsável por desenhar as salas, corredores e portas do Mapa Atual na tela "screen"
    """
    for sala in Mapa.salas:          # Desenha as salas do mapa
        pygame.draw.rect(screen, (211, 211, 211), (sala.x, sala.y, sala.largura, sala.altura))

    for corredor in Mapa.corredores: # Desenha os corredores da sala
        pygame.draw.rect(screen, (169, 169, 169), (corredor.x, corredor.y, corredor.largura, corredor.altura))
        for porta in corredor.porta: # Desenha as portas dos corredores
            pygame.draw.rect(screen, (211, 211, 211), (porta.x + corredor.x, porta.y + corredor.y, porta.largura, porta.altura))

def MudaMapa(player, mapa_atual, bot_atual, sala_atual, TMapas, TBots, TSalas): # Muda o Mapa atual
    """
    * Suporta um Mapa com vários corredos, mas utilizou-se apenas 1 por Mapa

    Função responsável por mudar o mapa atual após o player passar pela porta.

    Recebe como parâmetros:

    player: O personagem jogável, para executar a função "VerificaPorta" e mudar a posição do player
    mapa_atual: Para verificar os corredos do Mapa
    bot_atual: Para manter os bots caso não passe de Mapa
    sala_atual: Para manter a sala caso não passe de Mapa
    TMapas: Lista completa com todas os Mapas, para identificação
    TBots: Lista completa com todas os Bots, para identificação
    TSalas: Lista completa com todas as Sala, para identificação

    Funcionamento:
    - Para cada corredor do mapa atual, executa "VerificaPorta" para identificar o Id da porta
    que o jogador colidiu, caso não haja um Id (não houve colisão), mantém a Sala, Mapa e Bot atual.
    - Caso ocorra a colisão, é definido um novo mapa, sala e Bot. Além disso, como o ID da porta representa o seu destino
    (Id_porta = 3, leva para o Mapa 3). Ademais, o Id oficialmente usado é (porta_id - 1), pois os IDs da porta começam em 1, mas
    as listas, por definição, começam em zero.
    - Por fim, verifica-se se o If da porta é maior ou menor que o da sala atual, isso representa se ocorrerá o avanço
    ou retrocesso da sala, mudando o local em que o player apareceria.
    """
    for corredor in mapa_atual.corredores:
        porta_id = corredor.VerificaPorta(pygame.Rect((player.x, player.y, player.raio, player.raio))) # Fornece o Id da porta colidida
        if porta_id != None:            # Isto é, caso ocorra colisão
            id = porta_id - 1
            mapa_novo = TMapas[id]      # Atualiza o mapa atual
            bot_novo = TBots[id]        # Atualiza a lista de bot atual
            sala_nova = TSalas[id]      # Atualiza a sala atual

            # Muda a posição do player ao avançar um mapa
            if mapa_atual.id < porta_id:
                player.x = 1200 - player.x
            
            # Muda a posição do player ao retornar um mapa
            if mapa_atual.id > porta_id:
                player.x = 1200 - (player.raio + 5) - player.x

        else: # Mantém o mapa, bot e sala atual, caso não ocorra colisão
            mapa_novo = mapa_atual
            bot_novo = bot_atual
            sala_nova = sala_atual
                
        return[mapa_novo, bot_novo, sala_nova]
