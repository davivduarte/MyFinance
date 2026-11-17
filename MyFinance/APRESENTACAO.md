# Guia rápido para apresentar o MyFinance

## 1. Problema e proposta
"O MyFinance organiza diferentes contas bancárias em um único ambiente. Em vez de acompanhar cada saldo separadamente, o usuário consegue visualizar suas contas e movimentações no mesmo programa."

## 2. Tela principal
"Na tela inicial mostramos o patrimônio total e o resumo de cada conta. O saldo é calculado com base no saldo inicial, nas receitas, despesas e transferências."

## 3. Entrar em uma conta
"Ao selecionar um banco, o usuário acessa as operações daquela conta. Assim, cada movimentação fica associada ao banco correto."

## 4. Receitas e despesas
"Uma transação possui tipo, descrição, valor, data, conta e categoria. Esses dados permitem consultar o histórico e gerar relatórios."

## 5. Transferências
"Transferências são diferentes de receitas e despesas. O dinheiro não entrou nem saiu do patrimônio total; apenas mudou de uma conta para outra."

## 6. Recorrências
"O usuário pode cadastrar, por exemplo, salário, aluguel ou mensalidade. O cadastro representa um compromisso recorrente. O lançamento do mês é confirmado manualmente, evitando duplicidade."

## 7. Banco de dados
"Utilizamos SQLite3. As tabelas são relacionadas por chaves primárias e estrangeiras. Por exemplo, uma conta pode possuir várias transações."

## 8. Programação
"Organizamos o programa em arquivos: models representam objetos, controllers concentram operações e views cuidam dos menus. Essa separação facilita entender e manter o código."

## Demonstração sugerida
1. Criar o perfil.
2. Cadastrar duas contas com saldos iniciais.
3. Registrar uma receita e uma despesa.
4. Consultar o histórico e o relatório.
5. Fazer uma transferência.
6. Voltar à tela principal e observar os saldos.
7. Mostrar as tabelas no SQLite.

## Limites do protótipo
O MyFinance é um simulador/organizador financeiro local. Não acessa bancos reais nem efetua transferências bancárias.