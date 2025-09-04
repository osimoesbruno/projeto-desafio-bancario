# Importa datetime para registrar data e hora das operações
from datetime import datetime

# ======================= FUNÇÃO MENU ===========================
def menu():
    """
    Exibe o menu principal e retorna a opção escolhida pelo usuário.
    """
    menu = """
    ================= MENU ==================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova conta
    [5] Listar contas
    [6] Novo usuário
    [7] Sair
    => """
    return input(menu)  # Captura a escolha do usuário


# ======================= FUNÇÃO DE DEPÓSITO ===========================
def depositar(saldo, valor, extrato, /):
    """
    Função para realizar depósitos.
    - Se o valor for positivo, adiciona ao saldo e registra no extrato.
    - Caso contrário, mostra mensagem de erro.
    """
    if valor > 0:
        saldo += valor  # Atualiza saldo
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Registra no extrato com data e hora
        extrato += f"{data_hora} - Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou, o valor informado é inválido, por favor, tente novamente!")

    return saldo, extrato


# ======================= FUNÇÃO DE SAQUE ===========================
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Função para realizar saques.
    Valida:
    - Se há saldo suficiente
    - Se valor não excede o limite por saque
    - Se o número máximo de saques já foi atingido
    Caso esteja tudo certo, atualiza saldo e registra no extrato.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Falha na operação: saldo insuficiente.")
    elif excedeu_limite:
        print("Falha na operação: valor do saque excedeu o limite.")
    elif excedeu_saques:
        print("Falha na operação: você excedeu o número de saques diários, tente novamente amanhã!")
    elif valor > 0:
        saldo -= valor  # Atualiza saldo
        numero_saques += 1  # Incrementa contador de saques
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{data_hora} - Saque: R$ {valor:.2f}\n"
    else:
        print("Falha na operação: valor informado é inválido.")

    return saldo, extrato


# ======================= FUNÇÃO DE EXIBIR EXTRATO ===========================
def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato de movimentações e o saldo atual.
    """
    data_hora_extrato = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("======= EXTRATO (gerado em {}) =======".format(data_hora_extrato))
    print(extrato if extrato else "Sem movimentações realizadas.")  # Mostra extrato ou mensagem padrão
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


# ======================= FUNÇÃO DE CRIAR USUÁRIO ===========================
def criar_usuario(usuarios):
    """
    Cria um novo usuário no sistema.
    Cada usuário é representado como um dicionário dentro da lista 'usuarios'.
    """
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")


# ======================= FUNÇÃO AUXILIAR DE BUSCA DE USUÁRIO ===========================
def filtrar_usuario(cpf, usuarios):
    """
    Busca um usuário pelo CPF dentro da lista 'usuarios'.
    Retorna o usuário se encontrado, caso contrário retorna None.
    """
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


# ======================= FUNÇÃO DE CRIAR CONTA ===========================
def criar_conta(agencia, numero_conta, usuarios):
    """
    Cria uma nova conta vinculada a um usuário existente.
    Cada conta é representada como um dicionário dentro da lista 'contas'.
    """
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


# ======================= FUNÇÃO DE LISTAR CONTAS ===========================
def listar_contas(contas):
    """
    Lista todas as contas existentes no sistema, mostrando:
    - Agência
    - Número da conta
    - Nome do titular
    """
    for conta in contas:
        print("=" * 100)
        print(f"Agência:\t{conta['agencia']}")
        print(f"C/C:\t\t{conta['numero_conta']}")
        print(f"Titular:\t{conta['usuario']['nome']}")


# ======================= FUNÇÃO PRINCIPAL ===========================
def main():
    """
    Função principal do sistema bancário.
    Controla o loop principal do programa e chama as funções de acordo com a opção escolhida no menu.
    """
    LIMITE_SAQUES = 3   # Constante: limite máximo de saques por usuário
    AGENCIA = "0001"    # Agência fixa para todas as contas

    # Variáveis principais do sistema
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []  # Lista para armazenar os usuários
    contas = []    # Lista para armazenar as contas

    while True:  # Loop principal do programa
        opcao = menu()  # Exibe o menu e captura a escolha

        if opcao == "1":
            valor = float(input("Informe o valor que você deseja depositar: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Digite o valor a ser sacado: "))
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            numero_conta = len(contas) + 1  # Gera número sequencial para conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_usuario(usuarios)

        elif opcao == "7":
            break  # Sai do sistema

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


# ======================= EXECUÇÃO DO PROGRAMA ===========================
main()
