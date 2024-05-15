# -*- coding: utf-8 -*-
#SQL

import os
import sqlite3
import time
from datetime import datetime
import math

pi = math.pi

connection = sqlite3.connect('bancomarshall.db', check_same_thread = False)
c = connection.cursor()

def date():
    now = datetime.now()
    data = now.strftime("%d/%m/%Y, %H:%M:%S")
    return data

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS dadosensaio (id integer, identificador text, rodovia text, trecho text, operador text, CP text, origem text, km text, interesse text, observacao text, data text, cteanel integer);""")
    c.execute("""CREATE TABLE IF NOT EXISTS dadosamostra (id integer, pesosub real, pesoar real, temp real, diametro real, altura real, asfalto real, DMT real, Vv real);""")
    c.execute("""CREATE TABLE IF NOT EXISTS leituraEnsaio (id integer, deformacao real, estabilidade real);""")
create_table()

def write_table_dadosEnsaio(id, identificador, rodovia, trecho, operador, cpn, origem, km, interesse, observacao, cteanel):
    c.execute("""
    INSERT INTO dadosensaio (id,identificador, rodovia, trecho, operador, CP, origem, km, interesse, observacao, data, cteanel)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (id, identificador, rodovia, trecho, operador, cpn, origem, km, interesse, observacao, date(), cteanel))
    connection.commit()

def write_table_dadosAmostra(id, pesosub, pesoar, temp, diametro, altura, asfalto, DMT, Vv):
    c.execute("""
    INSERT INTO dadosamostra (id, pesosub, pesoar, temp, diametro, altura, asfalto, DMT, Vv)
    VALUES (?,?,?,?,?,?,?,?,?)
    """, (id, pesosub, pesoar, temp, diametro, altura, asfalto, DMT, Vv))
    connection.commit()

def write_table_Ensaio(id, vetor1, vetor2):
    i = 0
    print ("vet1:"+str(len(vetor1))+" vet2:"+str(len(vetor2)))
    while i < len(vetor1) and i<len(vetor2):
        # print("i:"+str(i))
        c.execute("""
        INSERT INTO leituraEnsaio (id, deformacao, estabilidade)
        VALUES (?,?,?)
        """, (id,round(vetor1[i],3),round(vetor2[i],4)))
        i +=1
    connection.commit()

def get_id():
        vetor = []
        c.execute("""
        SELECT * FROM dadosensaio;
        """)
        vetor = c.fetchall()
        if(len(vetor) == 0):
            return -1
        else:
            return vetor[-1][0]

def get_values():
    vetor = []
    dados = []
    enviar_dados = []
    c.execute("""
    SELECT * FROM dadosensaio;
    """)
    vetor = c.fetchall()
    for linha in vetor:
        auxiliar = []
        codigo = linha[0]
        dados.append(codigo)
        data = linha[10]
        operador = linha[4]
        norma = linha[1]
        auxiliar.append(data)
        auxiliar.append(operador)
        auxiliar.append(norma)
        dados.append(auxiliar)
    alcance = range(len(dados)/2 + (len(dados)/2 - 1))
    for i in alcance:
        if(i%2 == 0):
            auxiliar = []
            auxiliar.append(dados[i])
            auxiliar.append(dados[i+1])
            enviar_dados.append(auxiliar)
    return enviar_dados[::-1]

def delete(id):
    c.execute("""
    DELETE FROM dadosensaio
    WHERE id = ?
    """, (id,))
    c.execute("""
    DELETE FROM dadosamostra
    WHERE id = ?
    """, (id,))
    c.execute("""
    DELETE FROM leituraEnsaio
    WHERE id = ?
    """, (id,))
    connection.commit()

def get_dadosEnsaio(id):
    c.execute("""
    SELECT * FROM dadosensaio WHERE id = ?;
    """,(id,))
    dados_ensaio = c.fetchall()
    return dados_ensaio

def get_dadosAmostra(id):
    c.execute("""
    SELECT * FROM dadosamostra WHERE id = ?;
    """,(id,))
    dados_amostra = c.fetchall()
    return dados_amostra

def get_leituraEnsaio(id):
    c.execute("""
    SELECT * FROM leituraEnsaio WHERE id = ?;
    """,(id,))
    leituras_auxiliar = c.fetchall()
    return leituras_auxiliar

def update_dadosEnsaio(id,a,b,d,e,f,g,h):
    c.execute("""
    UPDATE dadosensaio SET rodovia = ?, trecho = ?, CP = ?, origem = ?, km = ?, interesse = ?, observacao = ? WHERE id = ?
    """, (a, b, d, e, f, g, h, id,))
    connection.commit()

# def teste():
#     c.execute("""
#     INSERT INTO dadosensaio (id, operador)
#     VALUES (?,?)
#     """, (id, oper))
#     connection.commit()

def clean():
    c.execute("""
    DELETE FROM dadosensaio
    WHERE identificador IS NULL
    """)
    connection.commit()
