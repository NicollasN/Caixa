'''
Caixa com a função de depositar um valor e armazenar no banco de dados, depois o cliente pode sacar o dinheiro se ele estiver disponível
'''
#importando banco de dados 
import sqlite3
banco = sqlite3.connect('banco_caixa.db')
cursor = banco.cursor() 

# Criando Tabela no banco com os dados requisitados
#cursor.execute('CREATE TABLE banco_caixa(cpf integer, deposito integer)') # Confirmando a inserção dos produtos no banco

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11 # Validar que o cpf terá 11 digitos

# Função para cadastrar CPF
def cadastrar_cpf():
    while True: # While para verificar se o CPF tem 11 digitos
        cpf = input('Digite o seu CPF para cadastro (11 digitos): ')
        if validar_cpf(cpf):
            break
        else:
            print('CPF inválido, digite o CPF com 11 digítos')

    banco = sqlite3.connect('banco_caixa.db')
    cursor = banco.cursor() 
    try:
        cursor.execute('INSERT INTO banco_caixa (cpf) VALUES (?)', (cpf,)) # Registrar CPF no banco de dados
        banco.commit()
        print('CPF cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        print('Erro: CPF já está cadastrado')
    finally:
        banco.close()

# Função para acessar a conta
def login():
    cpf = input('Digite o seu CPF para acessar a sua conta (11 digitos): ')
    banco = sqlite3.connect('banco_caixa.db')
    cursor = banco.cursor() 
    cursor.execute('SELECT cpf FROM banco_caixa WHERE cpf = ?', (cpf,)) # Verificar se o CPF está já registrado no banco
    resultado = cursor.fetchone()
    banco.close()

    if resultado:
        print('Login realizado com sucesso! Acesso concedido ao sistema')
        return True
    else:
        print('Erro: CPF não cadastrado. Acesso negado')
        return False

# Realizar as ações para acessar a sua conta ou para cadastrar um CPF
while True:
    print('Bem- vindo ao BancoN')
    print()
    print('Opções do que fazer')
    print('Para cadastrar um cpf - digite[1]')
    print('Para acessar a sua conta - digite[2]')
    digite = input('1 ou 2: ')

    if digite == '1':
        cadastrar_cpf() # Chamando a função cadastrar CPF
    elif digite == '2': # Chamando função logar
        if login(): 
            break # Se o CPF estiver cadastrado o loop para
    else:
        print('Opção incorreta, tente novamente.')

while True:

    # Realizar as ações para as operações dentro do caixa
    print('Operações:')
    print('Fazer um deposito - digite [1]')
    print('Sacar algum dinheiro - digite [2]')
    print('Sair da conta - digite [3]')

    digitar = int(input('O que voce deseja fazer agora:'))
    if digitar != 3:
        cpf = int(input('Digite seu cpf novamente: ')) # Digitar o CPF para poder realizar a operação selecionada 

    if digitar == 1: # Despositar um valor em reais
        depositar = int(input('Quanto você deseja depositar: '))
        deposito = depositar    
        print(f'Depósito realizado com sucesso! Agora voce tem um saldo de R${deposito} na sua conta.')
        # Inserindo dados do deposito no banco 
        cursor.execute('INSERT INTO banco_caixa (cpf, deposito) VALUES (?, ?)', (cpf, deposito))
        banco.commit()

    elif digitar == 3: # Sair do caixa
        print('Obrigado e volte sempre!')
        break

    elif digitar == 2 and digitar != 3: # Sacar o dinheiro depositado
        sacar = int(input('Quanto você deseja sacar: '))
        
        if sacar > 0 and sacar == deposito:
            print(f'O total sacado foi de R${sacar}.') # O dinheiro é tirado do banco de dados
            deposito -= sacar
            print(f'Você agora possui R${deposito} na sua conta.') # mostra o saldo que você tem
            cursor.execute('UPDATE banco_caixa SET deposito = ? WHERE cpf = ?', (deposito, cpf)) # Atualizando os dados sobre o saldo da conta
            banco.commit()
        elif sacar > deposito: # Se você quiser sacar um valor maior do que você tem depositado, isso não será possível
            print('Saldo indiponível para saque')

print('Obrigado, e volte sempre!') 