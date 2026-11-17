from datetime import date

def linha():
    print("=" * 62)

def titulo(texto):
    linha()
    print(texto.center(62))
    linha()

def pausar():
    input("\nPressione ENTER para continuar...")

def ler_texto(mensagem):
    texto = input(mensagem).strip()
    while texto == "":
        print("Este campo nao pode ficar vazio.")
        texto = input(mensagem).strip()
    return texto

def ler_valor(mensagem):
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
            if valor <= 0:
                print("Digite um valor maior que zero.")
            else:
                return round(valor, 2)
        except ValueError:
            print("Valor invalido. Exemplo: 1250,50")

def ler_numero(mensagem, minimo=1):
    while True:
        try:
            numero = int(input(mensagem))
            if numero < minimo:
                print("Digite um numero igual ou maior que {}.".format(minimo))
            else:
                return numero
        except ValueError:
            print("Digite apenas numeros inteiros.")

def ler_data(mensagem="Data (AAAA-MM-DD) ou ENTER para hoje: "):
    texto = input(mensagem).strip()
    if texto == "":
        return date.today().isoformat()
    try:
        ano, mes, dia = texto.split("-")
        date(int(ano), int(mes), int(dia))
        return texto
    except ValueError:
        print("Data invalida. Usando a data de hoje.")
        return date.today().isoformat()

def formatar_dinheiro(valor):
    texto = "{:,.2f}".format(valor)
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto
