# -*- coding: utf-8 -*-
#SQL

import sqlite3
import math

connection = sqlite3.connect('banco/bancoCAB.db', check_same_thread = False)
c = connection.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS Cabecalho (id INTEGER PRIMARY KEY AUTOINCREMENT, identificador text, instituicao text, fantasia text, cpfcnpj text, email text, fone text, uf text, cidade text, bairro text, rua text, numero text, complemento text, cep text, logo text)")
    c.execute('CREATE TABLE IF NOT EXISTS idDeletados (idDeletados integer)')
    c.execute("CREATE TABLE IF NOT EXISTS escolha (id)")

def data_entry():
    try:
        c.execute("INSERT INTO Cabecalho VALUES (0, '(Default)', 'UFRB - UNIVERSIDADE FEDERAL DO RECÔNCAVO DA BAHIA', 'EDP - Ensaios Dinâmicos para Pavimentação' ,'xxx.xxx.xxx-xx', 'ensaios.labpav.ufrb@gmail.com', '(xx) x.xxxx-xxxx', 'Ba', 'Cruz das Almas', 'Centro', 'R. Rui Barbosa', 'sn', 'Pavilhão de Engenharias, UFRB', '44.380-000', 'logo\logoEDP.png')")
        c.execute("INSERT INTO escolha VALUES (0)")
        connection.commit()
    except Exception:
        pass

create_table()
data_entry()

'''Cria uma Lista Index de visualização dos Cabecalhos Cadastrados'''
def ListaVisualizacaoCab():
    a = idsCab()
    b = data_identificadores()
    cont = 0
    id = len(a) - 1
    c = []
    while cont <= id:
        c.append(a[cont] + [[b[cont]]])
        cont = cont + 1

    return c

'''Lista com os ids dos Cabecalhos cadastrados'''
def idsCab():
    lista_id = []
    tupla=c.execute('SELECT * FROM Cabecalho')
    for row in tupla:
        lista_id.append([row[0]])

    return lista_id


'''Retorna uma lista com o identificadores dos Cabeçalhos já Cadastrados'''
def data_identificadores():
    list_idCab = []
    tupla=c.execute('SELECT * FROM Cabecalho')
    for row in tupla:
        list_idCab.append(row[1])

    return list_idCab

'''Salva os dados de um novo Cabeçalho'''
def data_save_dados(identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, complemento, cep, logo):
    c.execute("INSERT INTO Cabecalho (id, identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, complemento, cep, logo) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, cep, complemento, logo))
    connection.commit()

'''Captura o id do Cabeçalho escolhido para impressão'''
def idEscolha():
    escolha = []
    tupla=c.execute('SELECT * FROM escolha')
    for row in tupla:
        escolha.append(row[0])

    return escolha[0]

'''Compara a String identificador para encontrar o id'''
def identificador_id(ident):
    ult = []
    tupla=c.execute('SELECT * FROM Cabecalho WHERE identificador = ?', (ident,))
    for row in tupla:
        ult.append(row[0])

    return ult[0] #retorna com id

'''Entra com a id para encontrar o identificador'''
def id_identificador(id):
    ult = []

    for row in c.execute('SELECT * FROM Cabecalho WHERE id = ?', (id,)):
        ult.append(row[1])

    return ult[0] #retorna com identificador

'''Altera o Cabeçalho de escolha no banco de dados'''
def updateEscolha(id):
    c.execute("UPDATE escolha SET id = ?", (id,))
    connection.commit()

'''Retorna uma lista com os dados cadastrados no cabeçalho dado o id'''
def ListaDadosCab(id):
    lista = []
    ListaFormatada=[]
    tupla=c.execute('SELECT * FROM Cabecalho WHERE id = ?', (id,))
    for row in tupla:
        lista.append(row[1])
        lista.append(row[2])
        lista.append(row[3])
        lista.append(row[4])
        lista.append(row[5])
        lista.append(row[6])
        lista.append(row[7])
        lista.append(row[8])
        lista.append(row[9])
        lista.append(row[10])
        lista.append(row[11])
        lista.append(row[12])
        lista.append(row[13])
        lista.append(row[14])
    
    for i in range(13):
        ListaFormatada.append(str(lista[i+1]))


    return ListaFormatada

'''Deleta um Cabeçalho no banco de dados de acordo com o id'''
def deleteCAB(id):
    c.execute("DELETE FROM Cabecalho WHERE id = ?", (id,))
    c.execute("INSERT INTO idDeletados (idDeletados) VALUES (?)", (id,))
    connection.commit()

'''Ver a quantidade de cabeçalhos que já foram deletados'''
def quant_CAB_deletados():
    identificador = []
    tupla=c.execute('SELECT * FROM idDeletados')
    for rows in tupla:
        identificador.append(rows[0])

    id = len(identificador)
    return id

'''Ver os id dos cabeçalhos que foram deletados'''
def ler_ID_CAB_deletados():
    identificador = []
    tupla=c.execute('SELECT * FROM idDeletados')
    for rows in tupla:
        identificador.append(rows[0])

    return identificador

'''Retorna uma lista com os dados do cabeçalho de acordo com o id'''
def ListaDadosCabecalhos(id):
    lista = []
    tupla=c.execute('SELECT * FROM Cabecalho WHERE id = ?', (id,))
    for row in tupla:
        lista.append(row[1])
        lista.append(row[2])
        lista.append(row[3])
        lista.append(row[4])
        lista.append(row[5])
        lista.append(row[6])
        lista.append(row[7])
        lista.append(row[8])
        lista.append(row[9])
        lista.append(row[10])
        lista.append(row[11])
        lista.append(row[12])
        lista.append(row[13])
        lista.append(row[14])

    return lista

'''Atualiza os dados de um Cabeçalho de acordo com o id'''
def data_update_dados(id, identificador, instituicao, fantasia, cpfcnpj, email, fone, uf, cidade, bairro, rua, numero, complemento, cep, logo):
    c.execute("UPDATE Cabecalho SET identificador = ?, instituicao = ?, fantasia = ?, cpfcnpj = ?, email = ?, fone = ?, uf = ?, cidade = ?, bairro = ?, rua = ?, numero = ?, complemento = ?, cep = ?, logo = ?    WHERE id = ?",(identificador,instituicao,fantasia,cpfcnpj,email,fone,uf,cidade,bairro,rua,numero,complemento,cep,logo, id,))
    connection.commit()
