menu = """
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        print("Depósito")
        valor= float(input("informe o valor que você deseja depositar: "))

        if valor > 0:
            saldo += valor
            extrato += f"deposito: R${valor:.2f}\n"
        else:
            print("operação falhou, o valor informado é inválido, por favor, tente novamente!")

    elif opcao == "2":
        print("Saque")
        valor= float(input("Digite o valor a ser sacado: "))
        
        Excedeu_saldo= valor>saldo
        Excedeu_limite= valor>limite
        Execedeu_saques= valor>LIMITE_SAQUES

        if Excedeu_saldo:
            print("Falha na operação, saldo insuficiente.")

        elif Excedeu_limite:
            print("Falha na operação, o valor do saque excedeu o limite.")

        elif Execedeu_saques:
            print("Falha na operação, você excedeu o número de saques diários, tente novamente amanhã!")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Falha na operação! Valor informado é inválido")

    elif opcao == "3":
        print("Extrato")
        print("\n================ EXTRATO ================")
        print("Sem movimentações realizadas." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")


    elif opcao == "4":
        break

    else:
        print("operação inválida, por favor selecione novamente a operação desejada")