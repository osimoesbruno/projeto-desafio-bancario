from datetime import datetime
from abc import ABC, abstractmethod

# ===========================================================
# CLASSE HISTORICO
# ===========================================================
# Responsável por armazenar as transações de uma conta.
# Esse é um exemplo de "composição": uma Conta possui um Histórico.
# O histórico guarda as informações, mas não toma decisões (SRP - princípio da responsabilidade única).
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


# ===========================================================
# CLASSE ABSTRATA TRANSACAO
# ===========================================================
# Usamos uma classe abstrata (ABC) para representar a ideia genérica de transação.
# Tanto "Saque" quanto "Depósito" são transações, logo herdam dela.
# Isso mostra o conceito de POLIMORFISMO (várias formas de executar "registrar").
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


# ===========================================================
# CLASSE DEPOSITO
# ===========================================================
# Herda de Transacao e implementa o método registrar.
# Aplicamos polimorfismo: tanto Saque quanto Depósito têm a mesma interface,
# mas cada um executa sua própria lógica.
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta._saldo += self.valor
            conta.historico.adicionar_transacao(
                f"{datetime.now()} - Depósito: R$ {self.valor:.2f}"
            )
            return True
        return False


# ===========================================================
# CLASSE SAQUE
# ===========================================================
# Também herda de Transacao. Mostra a lógica inversa do depósito.
# Aqui aplicamos ENCAPSULAMENTO ao usar atributos internos da conta.
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor <= conta._saldo and self.valor <= conta.limite:
            conta._saldo -= self.valor
            conta.historico.adicionar_transacao(
                f"{datetime.now()} - Saque: R$ {self.valor:.2f}"
            )
            return True
        return False


# ===========================================================
# CLASSE CONTA
# ===========================================================
# Representa uma conta bancária genérica.
# Aplica ABSTRAÇÃO: esconde detalhes (saldo, histórico) e expõe operações (depositar, sacar).
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0  # Encapsulamento: atributo privado (só pode ser alterado via métodos)
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo  # Getter controlado (não existe setter, só alteramos com métodos)

    def sacar(self, valor):
        return Saque(valor).registrar(self)

    def depositar(self, valor):
        return Deposito(valor).registrar(self)


# ===========================================================
# CLASSE CONTA CORRENTE
# ===========================================================
# Subclasse de Conta que adiciona restrições específicas (limite de saque, limite diário).
# HERANÇA: ContaCorrente herda atributos e métodos de Conta, mas estende o comportamento.
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3, agencia="0001"):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    # Polimorfismo: sobrescrevemos o método sacar
    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if super().sacar(valor):
            self.saques_realizados += 1
            return True
        return False


# ===========================================================
# CLASSE CLIENTE
# ===========================================================
# Representa um cliente genérico (poderíamos ter Pessoa Física e Jurídica).
# Mostra a COMPOSIÇÃO: Cliente possui contas.
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# ===========================================================
# SUBCLASSE PESSOA FISICA
# ===========================================================
# Herda de Cliente e adiciona atributos específicos de pessoa física.
# Exemplo claro de HERANÇA + ESPECIALIZAÇÃO.
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# ===========================================================
# FUNÇÃO MENU
# ===========================================================
def menu():
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
    return input(menu)


# ===========================================================
# FUNÇÃO PRINCIPAL (MAIN)
# ===========================================================
# O main é o "controlador" do sistema, não contém lógica de negócio.
# Ele apenas orquestra objetos (Cliente, Conta, Transação).
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    clientes = []   # lista de PessoaFisica
    contas = []     # lista de ContaCorrente

    while True:
        opcao = menu()

        # DEPÓSITO
        if opcao == "1":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado!")
                continue

            valor = float(input("Informe o valor do depósito: "))
            conta = cliente.contas[0]  # simplificação: pega a primeira conta do cliente
            cliente.realizar_transacao(conta, Deposito(valor))

        # SAQUE
        elif opcao == "2":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado!")
                continue

            valor = float(input("Informe o valor do saque: "))
            conta = cliente.contas[0]
            cliente.realizar_transacao(conta, Saque(valor))

        # EXTRATO
        elif opcao == "3":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado!")
                continue

            conta = cliente.contas[0]
            print("======= EXTRATO =======")
            for t in conta.historico.transacoes:
                print(t)
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
            print("========================")

        # NOVA CONTA
        elif opcao == "4":
            cpf = input("Informe o CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if not cliente:
                print("Cliente não encontrado!")
                continue

            numero_conta = len(contas) + 1
            conta = ContaCorrente(cliente, numero_conta, limite=500, limite_saques=LIMITE_SAQUES)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print("Conta criada com sucesso!")

        # LISTAR CONTAS
        elif opcao == "5":
            for conta in contas:
                print("=" * 50)
                print(f"Agência: {conta.agencia}")
                print(f"C/C: {conta.numero}")
                print(f"Titular: {conta.cliente.nome}")

        # NOVO CLIENTE
        elif opcao == "6":
            cpf = input("Informe o CPF: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)

            if cliente:
                print("Já existe cliente com esse CPF!")
                continue

            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço: ")

            novo_cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            clientes.append(novo_cliente)
            print("Cliente criado com sucesso!")

        # SAIR
        elif opcao == "7":
            break

        else:
            print("Operação inválida. Tente novamente.")


# Executa o sistema
main()
