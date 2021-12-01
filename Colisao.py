# Colisão

import numpy as np

class GCollider:
    """
    Classe que determina os parâmetro de colisão
    """
    # flag que indica se ocorreu colisão
    has = False
    # informa o último objeto a colidir
    last_id = -1
    # se é um objeto de swap (faz a troca da velocidade)
    swap = False
    # guarda a direção em relação ao último objeto colidido (overlay)
    dir = [0, 0]

def Colisao(ListaBots): # Função que viabiliza a colisão
    """
    Função que executa a colisão e altera o movimento
    """
    colliderLogic(ListaBots) # Obtém-se os Bots colididos

    # Verifica as colisões e faz a troca das velocidades
    for Bot1 in ListaBots:
        # Se há colisão
        if(Bot1.collider.has):
            # Pega o ultimo objeto que foi colidido
            Bot2 = getCircleById(Bot1.collider.last_id, ListaBots)

            # Remove a sobreposição
            overlapLogic(Bot1, Bot2)

            # Verifica se os dois objetos são swap, se sim, faz a troca
            # Se não for swap, simplesmente reverte sua movimentação
            if(Bot1.collider.swap and Bot2.collider.swap):
                # swap das velocidades
                v_x = Bot1.v_x
                v_y = Bot1.v_y

                Bot1.v_x = Bot2.v_x
                Bot1.v_y = Bot2.v_y

                Bot2.v_x = v_x
                Bot2.v_y = v_y
            elif(Bot1.collider.swap):
                v = np.sqrt(np.power(Bot1.v_x, 2) + np.power(Bot1.v_y, 2))
                # reverte a movimentação
                Bot1.v_x = Bot1.collider.dir[0] * v
                Bot1.v_y = (-1) * Bot1.collider.dir[1] * v

            elif(Bot2.collider.swap):
                v = np.sqrt(np.power(Bot2.v_x, 2) + np.power(Bot2.v_y, 2))
                # reverte a movimentação
                Bot2.v_x = Bot2.collider.dir[0] * v
                Bot2.v_y = (-1) * Bot2.collider.dir[1] * v

            # Limpa os dados da colisão para verificar a próxima no próximo loop
            Bot2.collider.has = False
            Bot1.collider.has = False

            Bot2.collider.last_id = -1
            Bot1.collider.last_id = -1
    
def checkColision(Bot1, Bot2): # Verifica se houve colisão
    # Calcula a distância entre os dois circulos
    d = np.sqrt(np.power(Bot2.x - Bot1.x, 2) + np.power(Bot2.y - Bot1.y, 2))
    # Verifica se a distância entre os dois é menor que a soma dos dois raios + o distanciamento, se sim, ocorreu uma colisão
    if(d < (Bot1.raio + Bot2.raio + Bot1.dist)):
        return True
    # Caso não tenha colisão, retorna falso
    return False

def colliderLogic(ListaBots): # Armazena quem colidiu
    """
    Função responsável por armazenar as colisões entre os Bots
    """
    for Bot1 in ListaBots:
        for Bot2 in ListaBots:
            if(Bot1.id != Bot2.id and Bot1.collider.has == False):
                if(checkColision(Bot1, Bot2)):
                    # Os dois guardam os ids um do outro
                    Bot1.collider.last_id = Bot2.id
                    Bot2.collider.last_id = Bot1.id

                    # Indica para os dois que houve colisão
                    Bot1.collider.has = Bot2.collider.has = True

def overlapLogic(Bot1, Bot2): # Evita sobreposição
    """
    Função responsável por evitar a colisão e impedir o travamento
    """
    # Salva Bot1 e Bot2 
    BotA = Bot1
    BotB = Bot2

    # Verifica se BotB é maior que BotA e se BotA pode trocar, se sim, faz a troca (move-se sempre o menor raio)
    if(BotA.raio < BotB.raio and Bot1.collider.swap):
        BotA = Bot2
        BotB = Bot1

    # Cria um vetor que liga A e B b Vetor = Ponto(B) - Ponto(A)
    v = [BotB.x - BotA.x, BotA.y - BotB.y]
        
    # Normaliza-se o vetor para saber a direção que se deve mover os Bots
    v_mod = np.sqrt(np.power(v[0], 2) + np.power(v[1], 2))
    v[0] = v[0] / v_mod
    v[1] = v[1] / v_mod
        
    # Com o vetor normalizado, multiplica-se pelo raio A + raio B + distanciamento
    # Depois, soma-se com a coordenada do A (o outro circulo ficará tangente ao circulo maior ou igual)
    BotB.x = BotA.x + v[0] * (BotB.raio + BotA.raio + Bot1.dist) * 1.05
    BotB.y = BotA.y + (-1)*v[1] * (BotB.raio + BotA.raio + Bot1.dist) * 1.05
    # Será movido o que tem o menor raio

    # Salva-se o vetor direção nos dois circulos que corresponde a direção em relação aos circulos
    BotA.collider.dir = v
    BotB.collider.dir = v

    # Retorna o objeto referente ao id passado

def getCircleById(id, ListaBots): # Pega o ultimo Bot colidido
    """
    Função responsável por informar qual Bot colidiu
    """
    for Bot in ListaBots:
        if(Bot.id == id):
            return Bot
    return None
