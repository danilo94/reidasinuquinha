from operator import attrgetter
from MemoryHandler import *
from KeyController import *
from time import *
from Jogada import *
from copy import *
from os import path

class GamePlayer(object):
    processo = "zsnesw.exe"
    gameManager = None
    controladorTeclado = None
    populacao = []
    pontosComputados = True
    jafezJogada = False
    melhorIndividuo = None

    def __init__(self):
        self.obterIndividuoExistente()
        sleep(3)
        self.gameManager = MemoryHandler(self.processo)
        self.controladorTeclado = keyController()
        self.criarPopulacaoInicial()

    def Player(self):
        individuoSelecionado = 0
        while True:
            individuo = self.populacao[individuoSelecionado]
            statusJogo = self.estadoJogo()
            quantidadeBolasAntesJogada = self.obterQuantidadeBolas()
            if statusJogo == AGUARDANDO_JOGADA and self.pontosComputados :
                quantidadeBolasAntesJogada = self.obterQuantidadeBolas()
                if (individuo.jogadaAtual < QUANTIDADE_JOGADAS):
                    self.executarJogada(individuo)
                else:
                    individuo.jogadasInvalidas = LIMITEJOGADASSEMPONTO

            statusJogo = self.estadoJogo()

            if statusJogo == AGUARDANDO_JOGADA and self.pontosComputados == False:
                self.computarPontoIndividuo(quantidadeBolasAntesJogada,individuo)

            if individuo.jogadasInvalidas >= LIMITEJOGADASSEMPONTO:
                individuo.jogadasInvalidas = 0
                individuo.fitness = individuo.fitness - 2
                individuoSelecionado = individuoSelecionado + 1
                print ("Pula Individuo "+ str(individuoSelecionado) )
                print ("Fitness: "+str(individuo.fitness))
                self.controladorTeclado.pressionar(2,0.4)
                if (individuoSelecionado >= len(self.populacao)):
                    individuoSelecionado = 0
                    self.gerarNovaPopulacao()


    def executarJogada(self,individuo):
        self.controladorTeclado.pressionar(1,0.5)
        self.controladorTeclado.pressionar(0,0.5)
        jogadaAtual = individuo.obterJogadaAtual()
        angulo,forca = self.obterForcaEAngulo(individuo.listaAngulos[jogadaAtual],individuo.listaForca[jogadaAtual])
        self.gameManager.escreverByte(ANGULO,angulo)
        self.gameManager.escreverByte(FORCA,forca)
        sleep(0.08)
        self.controladorTeclado.pressionar(0,0.5)
        sleep(1.1)
        self.pontosComputados = False
        while (self.estadoJogo()== EM_MOVIMENTO):
            sleep(0.01)

    def obterForcaEAngulo(self,forca,angulo):
        angulo_byte = angulo.to_bytes(1,byteorder="little")
        forca_byte = forca.to_bytes(1,byteorder="little")
        return forca_byte,angulo_byte

    def estadoJogo(self):
        movimento = self.gameManager.lerByte(BALL_MOVING)
        if movimento == 0:
          return AGUARDANDO_JOGADA
        if movimento == 1:
          return AGUARDANDO_TACADA
        if movimento == 2:
          return EM_MOVIMENTO

    def jogadasRestantes(self):
        jogadas_restantes = self.gameManager.lerByte(TENTATIVAS)
        print(jogadas_restantes)
        return self.gameManager.lerByte(TENTATIVAS)

    def obterQuantidadeBolas(self):
        return self.gameManager.lerByte(BOLAS_ENCACAPADAS)

    def computarPontoIndividuo(self,bolasAntesdaJogada,individuo):
        bolasDepoisJogada = self.obterQuantidadeBolas()
        delta = bolasDepoisJogada - bolasAntesdaJogada
        if (delta > 0):
            individuo.fitness = FATORPONTOS * delta + individuo.fitness
            individuo.jogadasInvalidas = 0
        else:
            individuo.jogadasInvalidas = individuo.jogadasInvalidas + 1
            self.pontosComputados = True

    def criarPopulacaoInicial(self):
        self.populacao =[]
        populacaoTotal = TAMANHOPOPULACAO
        if (self.melhorIndividuo != None):
            self.populacao.append(copy(self.melhorIndividuo))
            populacaoTotal = populacaoTotal - 1
        for i in range(0,populacaoTotal):
            individuo = Jogada()
            self.populacao.append(individuo)

    def gerarNovaPopulacao(self):
        print("Construindo nova populacao")
        todosZerados = True
        for individuo in self.populacao:
            if (individuo.fitness != 0):
                todosZerados = False
        if todosZerados:
            self.criarPopulacaoInicial()
        else:
            self.obterMelhorInividuo()
            self.construirNovaPopulacao()

    def construirNovaPopulacao(self):
        listaNovosIndividuos = []
        for i in range (0, int(TAMANHOPOPULACAO*TAXAINDIVIDUOSPERSISTENTES)):
            novoIndividuo = self.crossingOver(self.populacao[i],self.melhorIndividuo)
            listaNovosIndividuos.append(novoIndividuo)

        quantidadeRestante = int(TAMANHOPOPULACAO - (TAMANHOPOPULACAO*TAXAINDIVIDUOSPERSISTENTES))

        for i in range (0,quantidadeRestante):
            novoIndividuo = Jogada()
            listaNovosIndividuos.append(novoIndividuo)

        self.populacao = listaNovosIndividuos

    def obterMelhorInividuo(self):
        self.populacao.sort(key=attrgetter('fitness'), reverse=True)
        if (self.melhorIndividuo == None):
            self.melhorIndividuo = copy(self.populacao[0])
        else:
            if (self.melhorIndividuo.fitness < self.populacao[0].fitness):
                f = open("best.txt","w")

                self.melhorIndividuo = copy(self.populacao[0])
                for i in range (0,len(self.melhorIndividuo.listaForca)):
                    f.write(str(self.melhorIndividuo.listaForca[i])+" "+str(self.melhorIndividuo.listaAngulos[i])+"\n")
        print("Fitness Melhor Invidiuo: "+str(self.melhorIndividuo.fitness))



    def crossingOver(self,individuoA,individuoB):
        novoIndividuo = Jogada()
        novoIndividuo.limparIndividuo()
        for i in range (0,QUANTIDADE_JOGADAS):
         percentual = random.uniform(0,1)
         if (percentual > 0.5):
             novoIndividuo.listaAngulos.append(individuoA.listaAngulos[i])
             novoIndividuo.listaForca.append(individuoA.listaForca[i])
         else:
             novoIndividuo.listaAngulos.append(individuoB.listaAngulos[i])
             novoIndividuo.listaForca.append(individuoB.listaForca[i])
         mutacao = random.uniform(0,1)
         if (mutacao <= TAXAMUTACAO):
             novoIndividuo.listaAngulos[i] = random.randint(0,255)
             novoIndividuo.listaForca[i] = random.randint(0,33)
        return novoIndividuo


    def obterIndividuoExistente(self):
        if (path.exists("best.txt")):
            f = open("best.txt",'r')
            linhas = f.readlines()
            individuo = Jogada()
            individuo.limparIndividuo()
            for linha in linhas:
                forca,angulo = linha.split(' ')
                individuo.listaAngulos.append(int(angulo))
                individuo.listaForca.append(int(forca))
            self.melhorIndividuo = copy(individuo)
