class Ambiente:
    def __init__(self, quadrados):
        self.quadrados = quadrados

    def is_sujo(self, local):
        return self.quadrados.get(local, False)

    def limpar(self, local):
        if local in self.quadrados:
            self.quadrados[local] = False


class Aspirador:
    def __init__(self, ambiente, posicao_inicial):
        self.ambiente = ambiente
        self.posicao = posicao_inicial
        self.pontuacao = 0

    def perceber(self):
        return self.ambiente.is_sujo(self.posicao)

    def aspirar(self):
        if self.perceber():
            self.ambiente.limpar(self.posicao)
            self.pontuacao += 1

    def mover(self, direcao):
        if direcao == "Direita" and self.posicao == "A":
            self.posicao = "B"
        elif direcao == "Esquerda" and self.posicao == "B":
            self.posicao = "A"
        self.pontuacao -= 1


class Simulador:
    def __init__(self, ambiente, aspirador):
        self.ambiente = ambiente
        self.aspirador = aspirador

    def executar(self, passos):
        for passo in range(passos):
            print(f"Passo {passo + 1}:")
            print(f"Posição do aspirador: {self.aspirador.posicao}")
            print(f"Estado do ambiente: {self.ambiente.quadrados}")
            print(f"Pontuação: {self.aspirador.pontuacao}")
            print("-" * 20)

            if self.aspirador.perceber():
                self.aspirador.aspirar()
            else:
                if self.aspirador.posicao == "A":
                    self.aspirador.mover("Direita")
                else:
                    self.aspirador.mover("Esquerda")

        print(f"Pontuação final: {self.aspirador.pontuacao}")
        print(f"Estado final do ambiente: {self.ambiente.quadrados}")


ambiente = Ambiente(quadrados={"A": True, "B": True})

aspirador = Aspirador(ambiente=ambiente, posicao_inicial="A")

simulador = Simulador(ambiente=ambiente, aspirador=aspirador)

simulador.executar(passos=10)