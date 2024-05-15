# -*- coding: utf-8 -*-
#SQL

import sqlite3

connection = sqlite3.connect('bdPreferences.db', check_same_thread = False)
c = connection.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS colors (id INTEGER PRIMARY KEY AUTOINCREMENT, card text, textCtrl text, Background text, lineGrafic text,  BackgroundGrafic text)")

def data_entry():
    try:
        c.execute("INSERT INTO colors VALUES (0, '#D7D7D7', '#777672', '#F0F0F0', 'r-', '#D7D7D7')")
        connection.commit()
    except Exception:
        pass

create_table()
data_entry()

def getCteAnel():
    list=[]
    tupla=c.execute('SELECT * FROM configEnsaio')
    for row in tupla:
        list.append(row[1])
        list.append(row[2])
    
    return list


'''Retorna uma lista de cores'''
def ListColors():
    lista = []
    for row in c.execute('SELECT * FROM colors'):
        lista.append(row[1])
        lista.append(row[2])
        lista.append(row[3])
        lista.append(row[4])
        lista.append(row[5])
        
    return lista

'''Atualiza as cores no banco de dados'''
def colors_update(card, textCtrl, Background, lineGrafic, BackgroundGrafic):
    id = 0;
    c.execute("UPDATE colors SET card = ? WHERE id = ?", (card, id,))
    c.execute("UPDATE colors SET textCtrl = ? WHERE id = ?", (textCtrl, id,))
    c.execute("UPDATE colors SET Background = ? WHERE id = ?", (Background, id,))
    c.execute("UPDATE colors SET lineGrafic = ? WHERE id = ?", (lineGrafic, id,))
    c.execute("UPDATE colors SET BackgroundGrafic = ? WHERE id = ?", (BackgroundGrafic, id,))
    connection.commit()

def update_back(back):
    c.execute("UPDATE colors SET Background = ? WHERE id = ?", (back, 0,))
    connection.commit()

def update_card(color):
    c.execute("UPDATE colors SET card = ? WHERE id = ?", (color, 0,))
    connection.commit()

def update_textctrl(color):
    c.execute("UPDATE colors SET textCtrl = ? WHERE id = ?", (color, 0,))
    connection.commit()