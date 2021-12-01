# Estrutura.py

import pygame
from Mapa import *
from BotPlayer import *

# Definindo o player (x, y, raio)
player = Player(50, 480, 20)

# Densidade Demográfica - quantidade de pessoas na sala
def DDemo(Largura, Altura, Dist):
    NMax = ((Largura* Altura)//(Dist*2))//375 # Número máximo de pessoas
    if NMax == 0:
        NMax = 1                              # Define o mínimo com 1
    return(NMax)

# Define valores: largura e altura da sala, distanciamento e quantidade de pessoas
def Valores():
    """
    Função responsável por definir os valores de comprimento( ou largura), altura (ou profundidade),
    o distânciamento e o número de pessoas(Bots) na sala
    O usuário pode inserir os valores desejados para a simulação e o programa calcula um número máximo de 
    pessoas a serem escolhidas, todos esse valores são posteriormente utilizados no programa
    """
    largura = int(input("Informe o comprimento da sala, entre 15m e 90m: "))*10
    while largura < 150 or largura > 900:
        largura = int(input("Insira um valor entre 15m e 90m: "))*10

    altura = int(input("Informe a profundidade da sala, entre 15m e 35m: "))*10
    while altura < 150 or altura > 350:
        altura = int(input("Insira um valor entre 15m e 35m: "))*10

    Dist = float(input("Informe o distânciamento desejado, entre 1m e 4m: "))*10
    while Dist < 10 or Dist > 40:
        Dist = int(input("Insira um valor entre 1m e 4m: "))*10

    NMax = DDemo(largura, altura, Dist)
    
    NBot = int(input(f"Informe o número de pessoas dentro da sala respeitando o limite de {NMax} pessoas: "))
    while NBot > NMax or NBot < 1:
        NBot = int(input(f"Deve-se conter pelo menos uma pessoa e no máximo {NMax} : "))

    return[largura, altura, NBot, Dist, NMax]

# Cria Salas e Bots
def CriaMapa(player):
    """
    Função responsável por criar todos os mapas e organizar os seus respectivos Bots.
    Inicialmente, o usuário escolhe o modo que deseja utilizar, caso escolha o modo Manual,
    o programa pedirá a quantidade de salas e, em seguida, os parâmetros escolhidos. Assim, os Mapas
    são criados ao mesmo tempo que os dados são fornecidos 
    """
    # Saudações iniciais
    print(f"Olá, bem-vindo ao Sistema Inteligente de Monitoramento de Aglomeração, denominado S.I.M.A.\n"
    "Nosso programa busca simular fluxos de pessoas em ambientes limitados, a fim de indicar possíveis aglomerações \n" 
    "indesejadas em cenários pandêmicos de patógenos transmitidos por via aérea,\n"
    "como o Sars-Cov-2")

    modo = int(input("Para começar, você deseja utilizar salas prontas? (Sim = 1/Não = 0) "))
    while modo != 1 and modo != 0:
        modo = int(input("Digite um valor válido (Sim = 1/Não = 0) "))

    print("Preparando simulação...")
    TBots = []
    TMapas = []
    TSalas = []
    
    if modo == 0: # Modo de criação manual
        NMapa = int(input("Informe o número de salas: "))
        for n in range(1, NMapa+1): # Cria [NMapa] Mapas (Por opção, decidiu-se utilizar uma Sala por mapa, por isso NMapa = NSala)
            xcorredor = 25        # Fixa a posição X do corredor
            ycorredor = 410       # Fixa a posição Y do corredor
            if n == 1 and NMapa > 1: # Primeira Sala 
                mapa = Mapa(50, 50, n)
                largura, altura, NBot, Dist, NMax  = Valores()
                salax = 700 - (largura/2)
                salay = ycorredor - altura - 15
                sala = Sala(salax, salay, largura, altura)
                sala.nmax = NMax
                mapa.addSala(sala)

                corredor = Corredor(xcorredor, ycorredor, 1150, 150)
                mapa.addCorredor(corredor)
                corredor.addPorta(Porta(1150, 0, 25, 150, 2))
                ListaB = ListaBot(NBot, Dist, sala)
                player.dist = Dist
                TBots.append(ListaB)
                TMapas.append(mapa)
                TSalas.append(sala)

            elif n == 1 and NMapa == 1: # Sala Única
                mapa = Mapa(50, 50, n)
                largura, altura, NBot, Dist, NMax  = Valores()
                salax = 700 - (largura/2)
                salay = ycorredor - altura - 15
                sala = Sala(salax, salay, largura, altura)
                sala.nmax = NMax
                mapa.addSala(sala)

                corredor = Corredor(xcorredor, ycorredor, 1150, 150)
                mapa.addCorredor(corredor)
                ListaB = ListaBot(NBot, Dist, sala)
                player.dist = Dist
                TBots.append(ListaB)
                TMapas.append(mapa)
                TSalas.append(sala)
                
            elif n > 1 and n < NMapa and NMapa != 1: # Salas intermediárias
                mapa = Mapa(1200 - player.x, 600 - player.y, n)
                largura, altura, NBot, Dist, NMax  = Valores()
                salax = 700 - (largura/2)
                salay = ycorredor - altura - 15
                sala = Sala(salax, salay, largura, altura)
                sala.nmax = NMax
                mapa.addSala(sala)

                corredor = Corredor(xcorredor, ycorredor, 1150, 150)
                mapa.addCorredor(corredor)
                corredor.addPorta(Porta(-25, 0, 25, 150, n - 1))
                corredor.addPorta(Porta(1150, 0, 25, 150, n + 1))
                ListaB = ListaBot(NBot, Dist, sala)
                player.dist = Dist
                TBots.append(ListaB)
                TMapas.append(mapa)
                TSalas.append(sala)
                
            elif n == NMapa: # Ultima Sala
                mapa = Mapa(1200 - player.x, 600 - player.y, n)
                largura, altura, NBot, Dist, NMax  = Valores()
                salax = 700 - (largura/2)
                salay = ycorredor - altura - 15
                sala = Sala(salax, salay, largura, altura)
                sala.nmax = NMax
                mapa.addSala(sala)

                corredor = Corredor(xcorredor, ycorredor, 1150, 150)
                mapa.addCorredor(corredor)
                corredor.addPorta(Porta(-25, 0, 25, 150, n - 1))
                ListaB = ListaBot(NBot, Dist, sala)
                player.dist = Dist
                TBots.append(ListaB)
                TMapas.append(mapa)
                TSalas.append(sala)
            
    elif modo == 1: # Modo pré-definido
        player.dist = 15
        mapa_1 = Mapa(50, 50, 1)                              # Cria mapa 1
        sala_1_mapa_1 = Sala(250, 45, 900, 350)               # Cria Sala 1 
        mapa_1.addSala(sala_1_mapa_1)                         # Add Sala 1 no mapa 1
        sala_1_mapa_1.nmax = 15

        corredor_1_mapa_1 = Corredor(25, 410, 1150, 150)      # Cria corredor 1
        mapa_1.addCorredor(corredor_1_mapa_1)                 # Add corredor 1 no mapa 1

        corredor_1_mapa_1.addPorta(Porta(1150, 0, 25, 150, 2)) # Add Porta para o mapa 2 no mapa 1

        #############################

        mapa_2 = Mapa(1200 - player.x, 600 - player.y, 2)
        corredor_1_mapa_2 = Corredor(25, 410, 1150, 150)
        corredor_1_mapa_2.addPorta(Porta(-25, 0, 25, 150, 1))
        corredor_1_mapa_2.addPorta(Porta(1150, 0, 25, 150, 3))

        mapa_2.addCorredor(corredor_1_mapa_2)
        sala_1_mapa_2 = Sala(250, 45, 600, 350)
        mapa_2.addSala(sala_1_mapa_2)
        sala_1_mapa_2.nmax = 15

        #############################

        mapa_3 = Mapa(1000 - player.x, 600 - player.y, 3)
        corredor_1_mapa_3 = Corredor(25, 410, 1150, 150)
        corredor_1_mapa_3.addPorta(Porta(-25, 0, 25, 150, 2))

        mapa_3.addCorredor(corredor_1_mapa_3)
        sala_1_mapa_3 = Sala(250, 45, 750, 350)
        sala_1_mapa_3.nmax = 15
        mapa_3.addSala(sala_1_mapa_3)

        ##############   Listas   #############

        ListaB1 = ListaBot(15, 15, sala_1_mapa_1)
        ListaB2 = ListaBot(10, 15, sala_1_mapa_2)
        ListaB3 = ListaBot(14, 15, sala_1_mapa_3)

        TBots = [ListaB1, ListaB2, ListaB3]                    # Lista com todas as listas de bots
        TMapas = [mapa_1, mapa_2, mapa_3]                      # Lista com todos os mapas
        TSalas = [sala_1_mapa_1, sala_1_mapa_2, sala_1_mapa_3] # Lista com todos as salas
    
    return[TBots, TMapas, TSalas]

# Executa a estrutura do programa com os valores estabelecidos
def Estrutura(TMapas, TBots, TSalas, player):
    """
    Função essencial para a simulação, após os dados serão definidos pela função "Valores()", "Estrutura()"
    terá o papel de executar e gerencias a simulação

    O que faz?
    - __init__() : Define as bases do programa e recebe os parâmetro básicos de Tela

    - initSima (): Cria a tela, define a fonte e o tempo

    - Interface(): Em construção, visa gerar um menu inicial para o programa

    - SimaMain(): Executa as funções de Evento, Update e Renderização, além de ser a responsável por manter
    a execução do programa, juntamento com o seu encerramento

    - SimaEvent(): Verifica se "Quit" ou "Esc" foram precionados para informar à "SimaMain()" o fim da simulaçao

    - SimaUpdate(): Realiza a atualização da simulação, Muda o mapa atual, atualiza os Bots e o Player, calcula 
    o número de pessoas e define o estado da porta

    - SimaRender(): Atualiza a tela, Desenha e Renderiza os corredos, salas, mapas, portas, bots e players.
    Permite a visualização do que está ocorrendo

    """
    class SIMA():
        def __init__(self, screenSize = (1200, 600), fps=60, title='S.I.M.A', icon=None):
            
            self.SimaRunning = True                 # Status do programa (True = Em execução)
            self.screenSize = screenSize            # Tamanho da tela
            self.title = title                      # Título
            self.icon = icon                        # Icon
            self.fps = fps                          # FPS
            
            self.initSima()

            self.mapa_atual = TMapas[0]             # Define o Mapa atual como o primeiro da lista geral
            self.bot_atual = TBots[0]               # Define o conjunto de Bots atual como o primeiro da lista geral
            self.sala_atual = TSalas[0]             # Define a sala atual como a primeira da lista geral
            
        def initSima(self):
            # Define a Tela,  a fonte do texto e "relógio" da simulação
            self.screen = pygame.display.set_mode(self.screenSize)

            pygame.display.set_caption(self.title)

            if(self.icon != None):
                pygame.display.set_icon(self.icon)
            
            pygame.font.init()

            self.start = False

            self.SimaClock = pygame.time.Clock()
            self.SimaFont = pygame.font.SysFont('Arial', 25)

        def SimaMain(self):
            # Limpa/ atualiza a tela, marca o tempo e realiza as etapas da simulação
            while self.SimaRunning:
                self.deltaTime = self.SimaClock.tick(self.fps)

                for event in pygame.event.get():
                    self.SimaEvent(event)
                self.SimaUpdate()
                self.SimaRender()

                pygame.display.update()

            pygame.display.quit()   

        def SimaEvent(self, event):     
            # Verifica se o "QUIT" ou "ESC" foram precionados, se sim, fecha a simulação
            if(event.type == pygame.QUIT):
                self.SimaRunning = False
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_ESCAPE):
                    self.SimaRunning = False

        def SimaUpdate(self):
            # Retorna a tecla precionada
            keys = pygame.key.get_pressed()
            
            # Muda o Mapa atual
            self.mapa_atual, self.bot_atual, self.sala_atual = MudaMapa(player, self.mapa_atual, self.bot_atual, self.sala_atual, TMapas, TBots, TSalas)

            # Nº de pessoas na sala
            self.NP = NPessoas(self.bot_atual, player, self.sala_atual)

            # Atualiza os Bots que estão na tela
            Atualiza(self.bot_atual, self.sala_atual, self.deltaTime, player, keys, self.screen)
            
            # Fecha a porta e permite o usuário usar a função "Restaura"
            self.sala_color = Restaura(player, self.sala_atual, self.NP, keys)

        def SimaRender(self):
            # Limpa a Tela
            self.screen.fill((70,130,180))

            # Desenha o mapa atual com suas salas e corredores
            DesenhaMapa(self.mapa_atual, self.screen)

            # Porta
            pygame.draw.rect(self.screen, self.sala_color ,(((self.sala_atual.x + (self.sala_atual.largura/2)))-75, 395, 150, 15))

            # Desenha os bots atuais
            DesenhaBots(self.bot_atual, self.screen)
                
            # Desenhando personagem
            pygame.draw.circle(self.screen, player.color, (player.x, player.y), player.raio)

            # Mostra o nº de pessoas na sala
            N = self.SimaFont.render(f'Nº de pessoas na sala: {self.NP}', True, (255, 255, 255))
            self.screen.blit(N, (10, 5))

            # Mostra o nº máximo de Bots na Sala
            NM = self.SimaFont.render(f'Nº máximo de pessoas na sala: {int((self.sala_atual).nmax)}', True, (255, 255, 255))
            self.screen.blit(NM, (880, 5))

            # Exibe os alertas de
            AlertaAglo(self.screen, self.NP, self.sala_atual, player)

    Simulação = SIMA()
    return(Simulação.SimaMain())
