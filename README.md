MyFinance — Gerenciamento Financeiro Pessoal
Projeto acadêmico desenvolvido em Python e SQLite3. O MyFinance permite organizar diferentes contas bancárias em um único programa de terminal.

Funcionalidades
Perfil local do usuário
Cadastro e gerenciamento de contas bancárias
Visão geral do patrimônio e dos saldos
Registro de receitas e despesas por conta
Categorias financeiras
Transferências entre contas
Cadastro de receitas fixas e gastos mensais
Registro manual de recorrências por mês
Histórico de movimentações
Relatórios por conta e relatório geral
Metas financeiras e aportes
Requisitos
Python 3.9 ou superior
Não precisa instalar bibliotecas externas: o projeto utiliza módulos que já acompanham o Python (sqlite3, datetime).
Como executar
Extraia a pasta MyFinance.
Abra a pasta no VS Code ou em outro editor.
Abra o terminal dentro da pasta.
Execute:
python main.py
O arquivo myfinance.db será criado automaticamente na primeira execução.

Como o sistema organiza o dinheiro
Cada conta possui um saldo inicial. O saldo atual é calculado considerando:

saldo inicial;
receitas registradas;
despesas registradas;
transferências recebidas;
transferências enviadas.
Uma transferência não é considerada receita nem despesa no relatório geral: ela apenas move dinheiro de uma conta para outra.

Organização dos arquivos
main.py: ponto de entrada do programa.
database/conexao.py: conexão e criação das tabelas SQLite.
models/: classes que representam objetos do sistema.
controllers/: operações de cadastro, consulta e movimentação.
views/menus.py: menus e interação com o usuário.
utils.py: funções auxiliares para entrada e apresentação de dados.
Modelo de dados
usuarios: perfil local.
contas: bancos e tipos de conta.
categorias: categorias de receitas e despesas.
transacoes: receitas e despesas realizadas.
transferencias: movimentações entre contas.
recorrencias: receitas e despesas que se repetem.
recorrencias_lancadas: controle para evitar lançar a mesma recorrência duas vezes no mesmo mês.
metas: objetivos financeiros.
aportes_meta: valores adicionados às metas.
Observações importantes
O programa é um controle financeiro manual e local. Ele não se conecta a bancos reais, não consulta saldos bancários e não realiza transferências via Pix.
As recorrências são cadastradas como planejamento. O usuário escolhe quando registrar o lançamento do mês.
A desativação de uma conta preserva seu histórico no banco de dados.
Este projeto é didático. Para uso real, seriam necessários recursos adicionais de segurança, validação e proteção de dados.
Sugestão de demonstração em aula
Criar o perfil.
Cadastrar Nubank e Itaú com saldos iniciais.
Entrar no Nubank e registrar uma receita.
Registrar uma despesa de alimentação.
Mostrar o histórico e o relatório da conta.
Transferir um valor do Nubank para o Itaú.
Voltar à tela principal e demonstrar a atualização dos saldos.
Mostrar as tabelas do SQLite e explicar as chaves primárias e estrangeiras.
