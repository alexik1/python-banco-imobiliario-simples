import random

partidas_timeout = []
media_partidas = []
vencedores = []


class Propriedade:
    def __init__(self, custo, aluguel):
        self.custo = custo
        self.aluguel = aluguel
        self.proprietario = None

    def pagar_aluguel(self, jogador):
        if self.proprietario is not None and self.proprietario != jogador:
            jogador.saldo -= self.aluguel
            self.proprietario.saldo += self.aluguel


class Jogador:
    def __init__(self, perfil):
        self.saldo = 300
        self.posicao_tabuleiro = 0
        self.propriedades = []
        self.perfil = perfil

    def comprar_propriedade(self, jogador, propriedade):
        jogador.perfil.comprar_propriedade(jogador, propriedade)

    def avancar_tabuleiro(self, jogador):
        dado_de_quantos_lados = 6
        dado = random.randint(1, dado_de_quantos_lados)
        posicao_avancando = (jogador.posicao_tabuleiro + dado)
        if posicao_avancando > 19:
            jogador.posicao_tabuleiro = (posicao_avancando - 19)
            jogador.saldo += 100
        else:
            jogador.posicao_tabuleiro = posicao_avancando


class Perfil:
    def __init__(self):
        pass

    def comprar_propriedade(self, jogador, propriedade):
        pass


class Impulsivo(Perfil):
    def comprar_propriedade(self, jogador, propriedade):
        if jogador.saldo >= propriedade.custo:
            jogador.saldo -= propriedade.custo
            propriedade.proprietario = jogador
            jogador.propriedades.append(propriedade)


class Exigente(Perfil):
    def comprar_propriedade(self, jogador, propriedade):
        if jogador.saldo >= propriedade.custo and propriedade.aluguel > 50:
            jogador.saldo -= propriedade.custo
            propriedade.proprietario = jogador
            jogador.propriedades.append(propriedade)


class Cauteloso(Perfil):
    def comprar_propriedade(self, jogador, propriedade):
        if jogador.saldo >= propriedade.custo and jogador.saldo - propriedade.custo >= 80:
            jogador.saldo -= propriedade.custo
            propriedade.proprietario = jogador
            jogador.propriedades.append(propriedade)


class Aleatorio(Perfil):
    def comprar_propriedade(self, jogador, propriedade):
        if random.random() > 0.5 and jogador.saldo >= propriedade.custo:
            jogador.saldo -= propriedade.custo
            propriedade.proprietario = jogador
            jogador.propriedades.append(propriedade)


class Jogo:
    def __init__(self):
        self.simulacoes = 1
        self.jogadores = [Jogador(Impulsivo()), Jogador(Exigente()), Jogador(Cauteloso()), Jogador(Aleatorio())]
        self.jogador_atual_index = 0
        self.turno = 1
        self.propriedades = [
            Propriedade(60, 10), Propriedade(60, 10), Propriedade(80, 20), Propriedade(100, 30),
            Propriedade(120, 40), Propriedade(60, 10), Propriedade(140, 50), Propriedade(150, 60),
            Propriedade(60, 10), Propriedade(180, 70), Propriedade(200, 80), Propriedade(60, 10),
            Propriedade(220, 90), Propriedade(60, 10), Propriedade(250, 100), Propriedade(250, 100),
            Propriedade(60, 10), Propriedade(300, 150), Propriedade(320, 160), Propriedade(200, 100)
        ]

    def simular(self):
        while self.simulacoes <= 300:
            Jogo().jogar()
            self.simulacoes += 1

        print("Partidas Finalizadas por Timeout - " + str(media_partidas.count(1000)))
        print("Média de Turnos por Partida - " + str(sum(media_partidas) / len(media_partidas)))
        print("--------")
        print("% de Vitórias por Comportamento")
        print("Impulsivo - " + str((vencedores.count('Impulsivo') * 100) / 300))
        print("Exigente - " + str((vencedores.count('Exigente') * 100) / 300))
        print("Cauteloso - " + str((vencedores.count('Cauteloso') * 100) / 300))
        print("Aleatório - " + str((vencedores.count('Aleatorio') * 100) / 300))
        print("-----")
        print("Comportamento com Maior # de Vitórias - " + str(max(set(vencedores), key=vencedores.count)))



    def jogar(self):
        while len(self.jogadores) > 1 and self.turno < 1000:
            jogador_atual = self.jogadores[self.jogador_atual_index]
            jogador_atual.avancar_tabuleiro(jogador_atual)
            propriedade_atual = self.propriedades[jogador_atual.posicao_tabuleiro]

            if propriedade_atual.proprietario == None:
                jogador_atual.comprar_propriedade(jogador_atual, propriedade_atual)
            else:
                propriedade_atual.pagar_aluguel(jogador_atual)

            if jogador_atual.saldo < 0:
                self.jogadores.pop(self.jogador_atual_index)

            if self.jogador_atual_index >= len(self.jogadores) - 1:
                self.jogador_atual_index = 0
                self.turno = (self.turno + 1)
            else:
                self.jogador_atual_index = (self.jogador_atual_index + 1)

        if len(self.jogadores) == 1:
            vencedores.append(str(self.jogadores[0].perfil.__class__.__name__))
            media_partidas.append(self.turno)
        else:
            media_partidas.append(self.turno)



Jogo().simular()
