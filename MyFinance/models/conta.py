class Conta:
    def __init__(self, id_conta, banco, tipo, saldo):
        self.id_conta = id_conta
        self.banco = banco
        self.tipo = tipo
        self.saldo = saldo

    def exibir_resumo(self):
        print("{} - {}".format(self.banco.upper(), self.tipo))
        print("Saldo atual: R$ {:.2f}".format(self.saldo))
