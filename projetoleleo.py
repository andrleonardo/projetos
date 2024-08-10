import mysql.connector
import datetime
pegadia=datetime.date.today().weekday() 
diassemana=['Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira','Sábado','Domingo']
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='P1zzaateotalo',
    database='bancodoleo'
)
cursor = conexao.cursor()

def calcular_notas(idquemfaz):
    print("Nenhuma prova futura encontrada.")

def adicionar_pessoa():
    cpf = input('Digite o CPF: ')
    nome = input('Digite o nome: ')
    ultimnome = input('Digite o último nome: ')
    email = input('Digite o email: ')
    senha = input('Digite a senha: ')
    nascimento = input('Digite a data de nascimento (YYYY-MM-DD): ')
    altura = input('Digite a altura: ')
    peso = input('Digite o peso: ')
    sexo = input('Digite o sexo (masculino/feminino): ')
    escolaridade = input('Digite a escolaridade: ')
    emprego = input('Digite o emprego: ')
    permissao = input('Digite o nível de permissão (1-5): ')

    comando = '''
    INSERT INTO pessoas (CPF, nome, ultimonome, email, senha, nascimento, altura, peso, sexo, Escolaridade, emprego, permission)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''
    cursor.execute(comando, (cpf, nome, ultimnome, email, senha, nascimento, altura, peso, sexo, escolaridade, emprego, permissao))
    conexao.commit()
    print('Pessoa adicionada com sucesso!')

def adicionar_prova():
    
    cursor.execute('SELECT id, nome FROM pessoas')
    pessoas_disponiveis = cursor.fetchall()

    print("Pessoas disponíveis:")
    for pessoa in pessoas_disponiveis:
        print(f"ID: {pessoa[0]}, Nome: {pessoa[1]}")

    usuario_id = None
    while not usuario_id:
        usuario_input = input('Digite o ID do usuário para a prova: ')
        if any(str(pessoa[0]) == usuario_input for pessoa in pessoas_disponiveis):
            usuario_id = usuario_input
        else:
            print("Usuário inválido, tente novamente.")

    cursor.execute('SELECT id, materias FROM materiasfacul')
    materias_disponiveis = cursor.fetchall()

    print("Matérias disponíveis:")
    for materia in materias_disponiveis:
        print(f"ID: {materia[0]}, Nome: {materia[1]}")

    materia_id = None
    while not materia_id:
        materia_input = input('Digite o ID da matéria: ')
        if any(str(materia[0]) == materia_input for materia in materias_disponiveis):
            materia_id = materia_input
        else:
            print("Matéria inválida, tente novamente.")

    tipos_prova_validos = [
        "APOL", "APOL Objetiva", "APOL Prática", "APOL Discursiva",
        "Objetiva", "Prática", "Discursiva"
    ]
    print("Tipos de prova disponíveis:")
    for tipo in tipos_prova_validos:
        print(f"- {tipo}")

    tipo_prova = None
    while not tipo_prova:
        tipo_input = input('Digite o tipo de prova: ')
        if tipo_input in tipos_prova_validos:
            tipo_prova = tipo_input
        else:
            print("Tipo de prova inválido, tente novamente.")

    pesos_validos = ["15", "40", "30", "0"]
    peso = None
    while not peso:
        peso_input = input('Digite o peso da prova (15, 40, 30, 0): ')
        if peso_input in pesos_validos:
            peso = peso_input
        else:
            print("Peso inválido, tente novamente.")

    data_fazer = input('Digite a data para fazer a prova (YYYY-MM-DD): ')
    data_fim = input('Digite a data final para a prova (YYYY-MM-DD): ')

    comando = '''
    INSERT INTO provas (idquemfaz, materia, tipoprova, peso, datafazer, datafim)
    VALUES (%s, %s, %s, %s, %s, %s);
    '''
    cursor.execute(comando, (usuario_id, materia_id, tipo_prova, peso, data_fazer, data_fim))
    conexao.commit()
    print('Prova adicionada com sucesso!')

def listar_provas_usuario(idquemfaz):
    query = """
    SELECT mf.materias, p.tipoprova, p.peso, p.datafazer, p.datafim
    FROM provas p
    JOIN materiasfacul mf ON p.materia = mf.id
    WHERE p.datafazer >= CURDATE() AND p.idquemfaz = %s
    ORDER BY p.datafazer ASC;
    """
    
    cursor.execute(query, (idquemfaz,))
    resultados = cursor.fetchall()
    
    if resultados:
        print("Próximas provas:")
        for row in resultados:
            print(f"{row[0]}, {row[1]}, VALE {row[2]}, DATAFAZER {row[3].strftime('%d/%m/%Y')}, DATAFIM {row[4].strftime('%d/%m/%Y')}")
    else:
        print("Nenhuma prova futura encontrada.")

def modificar_pessoa():
    cpf = input('Digite o CPF da pessoa que deseja modificar: ')
    print('Quais atributos deseja modificar?')
    print('''
    [1] Nome
    [2] Último Nome
    [3] Email
    [4] Senha
    [5] Data de Nascimento
    [6] Altura
    [7] Peso
    [8] Sexo
    [9] Escolaridade
    [10] Emprego
    [11] Permissão
    ''')
    opcao = input('Escolha uma opção: ')

    campos = {
        '1': ('nome', 'Digite o novo nome: '),
        '2': ('ultimnome', 'Digite o novo último nome: '),
        '3': ('email', 'Digite o novo email: '),
        '4': ('senha', 'Digite a nova senha: '),
        '5': ('nascimento', 'Digite a nova data de nascimento (YYYY-MM-DD): '),
        '6': ('altura', 'Digite a nova altura: '),
        '7': ('peso', 'Digite o novo peso: '),
        '8': ('sexo', 'Digite o novo sexo (masculino/feminino): '),
        '9': ('Escolaridade', 'Digite a nova escolaridade: '),
        '10': ('emprego', 'Digite o novo emprego: '),
        '11': ('permission', 'Digite o novo nível de permissão: ')
    }

    if opcao in campos:
        campo, mensagem = campos[opcao]
        novo_valor = input(mensagem)
        comando = f'UPDATE pessoas SET {campo} = %s WHERE CPF = %s;'
        cursor.execute(comando, (novo_valor, cpf))
        conexao.commit()
        print(f'{campo.capitalize()} modificado com sucesso!')
    else:
        print('Opção inválida.')

def deletar_pessoa():
    cpf = input('Digite o CPF da pessoa que deseja deletar: ')
    comando = 'DELETE FROM pessoas WHERE CPF = %s;'
    cursor.execute(comando, (cpf,))
    conexao.commit()
    print('Pessoa deletada com sucesso!')

def listar_pessoas():
    comando = 'SELECT * FROM pessoas;'
    cursor.execute(comando)
    pessoas = cursor.fetchall()

    if pessoas:
        for pessoa in pessoas:
            print(f'CPF: {pessoa[1]}, Nome: {pessoa[2]}, Último Nome: {pessoa[3]}, Email: {pessoa[4]}, '
                  f'Senha: {pessoa[5]}, Nascimento: {pessoa[6]}, Altura: {pessoa[7]}, '
                  f'Peso: {pessoa[8]}, Sexo: {pessoa[9]}, Escolaridade: {pessoa[10]}, '
                  f'Emprego: {pessoa[11]}, Permissão: {pessoa[12]}')
    else:
        print('Nenhuma pessoa encontrada.')

def gerenciar_pessoas():
    while True:
        print('''
*************************************************************************
[1] Adicionar Pessoa
[2] Modificar Pessoa
[3] Deletar Pessoa
[4] Listar Pessoas
[5] Sair do Gerenciador de Pessoas
**************************************************************************
''')
        opcao = input('Escolha uma opção: ')
        
        if opcao == '1':
            adicionar_pessoa()
        elif opcao == '2':
            modificar_pessoa()
        elif opcao == '3':
            deletar_pessoa()
        elif opcao == '4':
            listar_pessoas()
        elif opcao == '5':
            print('Saindo do Gerenciador de Pessoas...')
            break
        else:
            print('Opção inválida. Tente novamente.')

try:
    askmenu = int(input('''
*************************************************************************
[1] GERENCIADOR PESSOAS:
[2] CACETINHOS PADARIA SUP:
[3] Historico Cacetinho:
[4] Datas Provas Dos usuarios:
[5] Data Provas Por Usuario:
[6] Adicionar Provas :
[7] Sistema Calculo Notas:
[8]
**************************************************************************
Digite o número da opção desejada: '''))
except ValueError:
    print('Digite um valor válido.')
else:
    if askmenu == 1:
        user = input('Qual Seu Usuário? ')
        passw = input('Qual Sua Senha? ')

        comando = '''
        SELECT * FROM pessoas
        WHERE CPF = %s AND senha = %s AND permission = '5';
        '''
        
        cursor.execute(comando, (user, passw))
        resultado = cursor.fetchone()

        if resultado is None:
            print('Usuário ou senha incorretos ou permissão insuficiente.')
        else:
            print('Login realizado com sucesso! Acessando o Gerenciador de Pessoas...')
            gerenciar_pessoas()
    if askmenu==2:
            if pegadia <=4:
                askquantiacacete=int(input('''
********************************
Dia De Semana são 110 Esteiras

    1 = Manter      2 = Alterar          
*********************************
>> '''))
                if askquantiacacete ==1:
                    catedia=110
                else:
                    try:
                     catedia=int(input('Qual A Quantia de esteiras hoje ?? '))
                    except ValueError:
                        print('Valor Valido por favor')    
                        
            
                        

            else:
                askquantiacacete=int(input('''
********************************
Dia Final de Semana são 140 Esteiras

    1 = Manter      2 = Alterar          
*********************************
>> '''))
                if askquantiacacete ==1:
                    catedia=140
                else:
                    try:
                        catedia=int(input('Qual A Quantia de esteiras hoje ?? '))
                    except ValueError:
                        print('Valor Valido por favor')
            askcrua=int(input('Quantas Massas Crescidas Crua sobrou? '))
            askassada=int(input('Quantas Massas Assadas Sobrou? '))
            try:
                askestufa=int(input('A Quantia Na Estufa Se Mantem 18? 1 = SIM 2 = NÃO  '))
            except ValueError:
                print('VALOR ENTRE 1 E 2')
            if askestufa ==1:
                paoestufa=18
            else:
                try:
                 paoestufa=int(input('Quantas Na estufa? '))
                    
                except ValueError:
                 print('Valor Correto Por favor')
            try:       
                askgrande=int(input('Quantia no grandão = 36 SE MANTEM? 1 = SIM  2 = NÃO  '))
            except ValueError:
                print('Valor Entre 1 e 2')
            if askgrande==1:
                paogrande=36
            else:
                try:
                    paogrande=int(input('Qual A Quantia vai ser colocado no grandão? '))
                except ValueError:
                    print('Valor Correto Por favor')
            askadicional=int(input('Qual A Quantia de esteiras Adicionais? '))
            soma=(catedia -askcrua - paoestufa - paogrande) + askadicional

            print(f'''
***********************************
        Relatorio Cacetinho
[{catedia}] Esteiras Para O DIA
[{askcrua}] Esteiras Sobra Crua
[{askassada}] Esteiras Sobra Assada
[{paoestufa}] Esteiras Estufa
[{paogrande}] Esteiras Grandão
[{askadicional}] Esteiras Adicionais

          [{soma}] ESTEIRAS PARA TIRAR
************************************           
''')
            
            comando= f'INSERT INTO padaria_sup (quantiadia,quantiasobracrua,quantiasobraassada,sobraestufa,adicionais,nograndao,pratirar) VALUES ({catedia},{askcrua},{askassada},{paoestufa},{askadicional},{paogrande},{soma})'    
            cursor.execute(comando)
            conexao.commit()
    if askmenu==3:            
            comando = 'SELECT * FROM padaria_sup WHERE dia >= CURDATE() - INTERVAL 7 DAY ORDER BY quantiadia ASC;'
            #comando= ''
            cursor.execute(comando)
            resultado=cursor.fetchall()
            for linha in resultado:
               print(linha)  

    if askmenu==4:
            query = """
            SELECT mf.materias, p.tipoprova, p.peso, p.datafazer, p.datafim
            FROM provas p
            JOIN materiasfacul mf ON p.materia = mf.id
            WHERE p.datafazer >= CURDATE()
            ORDER BY p.datafazer ASC;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()
            
            if resultados:
                print("Próximas provas:")
                for row in resultados:
                    print(f"{row[0]}, {row[1]}, VALE {row[2]}, DATAFAZER {row[3].strftime('%d/%m/%Y')}, DATAFIM {row[4].strftime('%d/%m/%Y')}")
              
            else:
                print("Nenhuma prova futura encontrada.")
    elif askmenu == 5:
        user = input('Qual Seu Usuário? ')
        passw = input('Qual Sua Senha? ')

        comando = '''
        SELECT id FROM pessoas
        WHERE CPF = %s AND senha = %s;
        '''
        
        cursor.execute(comando, (user, passw))
        resultado = cursor.fetchone()

        if resultado is None:
            print('Usuário ou senha incorretos.')
        else:
            idquemfaz = resultado[0]
            listar_provas_usuario(idquemfaz)
    
    elif askmenu == 6:
        adicionar_prova()
    elif askmenu == 7:
        user = input('Qual Seu Usuário? ')
        passw = input('Qual Sua Senha? ')

        comando = '''
        SELECT id FROM pessoas
        WHERE CPF = %s AND senha = %s;
        '''
        
        cursor.execute(comando, (user, passw))
        resultado = cursor.fetchone()

        if resultado is None:
            print('Usuário ou senha incorretos.')
        else:
            idquemfaz = resultado[0]
            calcular_notas(idquemfaz)
        
cursor.close()
conexao.close()

