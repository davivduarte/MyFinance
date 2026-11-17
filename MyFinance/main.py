from database.conexao import criar_tabelas, obter_usuario
from views.menus import menu_principal

def main():
    criar_tabelas()
    usuario = obter_usuario()
    print("\nBem-vindo(a) ao MyFinance, {}!".format(usuario["nome"]))
    menu_principal(usuario)

if __name__ == "__main__":
    main()
