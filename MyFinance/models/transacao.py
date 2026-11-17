class Transacao:
    def __init__(self, tipo, descricao, valor, data):
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.data = data

    def exibir(self):
        sinal = "+" if self.tipo == "receita" else "-"
        print("{} | {} | {}R$ {:.2f} | {}".format(
            self.data, self.descricao, sinal, self.valor, self.tipo.upper()
        ))
