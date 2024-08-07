import csv
from datetime import datetime
import math

# olha essas variaveis e checa se está correto os valores
redbull_price = 5.15
brownie_price = 3.25
file_path = 'extrato.csv'
new_file_path = 'extrato-identified.csv'

def update_extrato(new_ids):
    reader = []
    headers = []
    # new_id = {"brownies": b, "redbulls": r, "row": index, "col": Identificação}
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = list(csv.DictReader(file))
        headers = reader[0].keys()
        print(reader)

    for new_id in new_ids:
        row_index = new_id['row']
        col_name = new_id['col']
        brownies = new_id['brownies']
        redbulls = new_id['redbulls']
        if new_id['message'] != '':
            identification_value = new_id['message']
        else:
            redbulls_message = f"Redbulls: {redbulls}"
            brownies_message = f"Brownies: {brownies}"
            if brownies == 0:
                identification_value = redbulls_message
            elif redbulls == 0:
                identification_value = brownies_message
            else:
                identification_value = ', '.join([brownies_message, redbulls_message])
        reader[row_index][col_name] = identification_value

    with open(new_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(reader)
        

def process_transactions(unknown_transactions, big_transactions, explained_transactions, explanations, new_ids):
    current_date = datetime.now()
    epsilon = 1e-6 # margem de erro para comparação de floats

    # coisas especiais
    # ----------
    marmita_price = 15
    marmita_date_begin = datetime.strptime("11/06/2024", "%d/%m/%Y")
    marmita_date_end = datetime.strptime("14/06/2024", "%d/%m/%Y")
    # ----------

    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for index, row in enumerate(reader):
            if row['Tipo Transação'] != 'CRÉDITO' or row['Transação'] != 'Transf Pix recebida':
                continue

            transaction_date = datetime.strptime(row['Data'], "%d/%m/%Y")
            value = float(row['Valor'])
            register = {'Data': row['Data'], 'Identificação': row['Identificação'], 'Valor': value}

            # coisas especiais
            if marmita_date_begin <= transaction_date <= marmita_date_end and value == marmita_price:
                new_ids.append({
                    "brownies": 0,
                    "redbulls": 0,
                    "row": index,
                    "col": "Identificação",
                    'message': 'Marmita para sábado júnior'
                })
                continue
            # ----------

            if register in explained_transactions:
                exp_id = explained_transactions.index(register)
                new_ids.append({
                    "brownies": 0,
                    "redbulls": 0,
                    "row": index,
                    "col": "Identificação",
                    'message': explanations[exp_id]
                })
                continue

            # imagino q ninguém vai gastar 100 reais de uma vez
            if value > 100:
                # mas vai q
                big_transactions.append(register)
                continue
            
            max_brownies = math.ceil(value / brownie_price)
            max_redbulls = math.ceil(value / redbull_price)
            
            found = False
            for b in range(max_brownies + 1):
                for r in range(max_redbulls + 1):
                    if abs(b * brownie_price + r * redbull_price - value) < epsilon:
                        new_ids.append({"brownies": b, "redbulls": r, "row": index, "col": "Identificação", "message": ''})
                        found = True
                        break
                if found:
                    break
            
            if not found:
                unknown_transactions.append(register)


def print_transactions(transactions, name):
    if transactions:
        print(f"Transações {name}:")
        for transaction in transactions:
            print(transaction)
    else:
        print(f"Nenhuma transação {name} encontrada.")

    print()

unknown_transactions = []
big_transactions = []
new_ids = []

# Sempre que for adicionar uma transação explicada, adicione uma explicação
explanations = [
    # insira as explicações aqui, por exemplo: "Brownies: 0, Redbulls: 1"
]
# insira as transações explicadas aqui
explained_transactions = [
    # exemplo de transação: {'Data': '01/01/2024', 'Identificação': 'nome do membro', 'Valor': 5.16}
]

process_transactions(
    unknown_transactions, big_transactions, explained_transactions, explanations, new_ids)

update_extrato(new_ids)

print_transactions(unknown_transactions, 'desconhecida')
print_transactions(big_transactions, 'grande')

members_unknown = [unknown_transaction['Identificação'] for unknown_transaction in unknown_transactions]

while True:
    member_input = input('Filter para algum membro ("exit" para sair): ')

    if member_input in members_unknown:
        for unknown_transaction in unknown_transactions:
            if member_input == unknown_transaction['Identificação']:
                print(unknown_transaction)
    elif member_input == 'exit':
        break
    else:
        print('Membro não encontrado')
        print()
        print('Digite o nome do membro igual o que está no registro')
        print()
        print()

print()
print('bye bye')
