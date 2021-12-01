from tkinter import *
from Estrutura import *

###########  Iniciando o programa  ####
TBots, TMapas, TSalas = CriaMapa(player) # Inicia a função que define os parâmetros das salas

###########  Interface ################

def ChamarBotao():                       # Inicia Simulação
    """
    Define a função que determina a ação do botão quando o usuário clica nele
    Quando o usuário clica no botão, a função Estrutura() é chamada e inicia a simulação
    
    """
    Estrutura(TMapas, TBots, TSalas, player)

def Interface():                         # Define a função que cria a interface do programa

    # Cria a janela e importa a imagem de fundo
    janela = Tk()

    img = PhotoImage(file="Imagens/Projeto.png")

    # Define os parâmetros da janela
    janela.geometry("1300x700")
    janela.title("S.I.M.A")
    janela.configure(bg="black")

    # Cria e posiciona o botão (além de definir o comando que ele executará)
    botao = Button(janela, text="Iniciar", font=("Arialle, 20"), command=ChamarBotao)
    botao.grid(column=0, row=0, padx=0, pady=10)

    # Posiciona a imagem na tela
    label_image = Label(janela, image=img, border="0")
    label_image.grid(padx=30, pady=0)
    
    # Inicia a janela e mantem ela funcionando
    janela.mainloop()

Interface()                              # Executa a interface inicial do programa