import random

from Enderecos import QUANTIDADE_JOGADAS


class Jogada(object):

    listaAngulos =[]
    listaForca = []
    fitness = None
    jogadasInvalidas = None
    jogadaAtual=0

    def __init__(self):
        self.listaAngulos =[]
        self.listaForca = []
        self.fitness = 0
        self.jogadasInvalidas = 0
        self.jogadaAtual = 0
        self.inicializaJogadasIniciais()

    def inicializaJogadasIniciais(self):
        for i in range (0,QUANTIDADE_JOGADAS):
            self.listaAngulos.append(random.randint(0,255))
            self.listaForca.append(random.randint(0,33))


    def obterJogadaAtual(self):
        jogadaAtual = self.jogadaAtual
        if (self.jogadaAtual < QUANTIDADE_JOGADAS):
            self.jogadaAtual = self.jogadaAtual + 1
        return jogadaAtual

    def limparIndividuo(self):
        self.jogadaAtual=0
        self.jogadasInvalidas=0
        self.fitness=0
        self.listaForca=[]
        self.listaAngulos=[]
