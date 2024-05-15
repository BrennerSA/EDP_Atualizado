# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import bancodedadosnovo
import unicodecsv
import csv
import math

pi = math.pi

'''Class Export CSV'''
class Csv(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, id, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EAU - CSV')
        self.id = id
        frame = self.basic_gui()
    #--------------------------------------------------
     def basic_gui(self):
        id = self.id
        self.createCSV("teste")

    #--------------------------------------------------
     def createCSV(self, name):
          id = self.id
          DE = bancodedadosnovo.get_dadosEnsaio(self.id)
          DA = bancodedadosnovo.get_dadosAmostra(self.id)
          leituras = bancodedadosnovo.get_leituraEnsaio(self.id)
          with wx.FileDialog(self, name, wildcard="CSV files(*.csv)|*.csv*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
               if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

               pathname = fileDialog.GetPath()

               try:
                    with open(fileDialog.GetPath() + '.csv', 'wb') as file:
                         editor = csv.writer(file)
                         editor.writerow(["","","","","","","","","","","","","","","",""])
                         editor.writerow(["","","Dados do Ensaio"])
                         editor.writerow(["","","Ensaio n.","Identificador", "Rodovia", "Trecho", "Operador", "CP", "Origem","Est/km","Interesse","Observacao","Data e hora"])
                         editor.writerow(["","",DE[0][0], DE[0][1], DE[0][2], DE[0][3], DE[0][4], DE[0][5], DE[0][6], DE[0][7], DE[0][8], DE[0][9], DE[0][10]])
                         editor.writerow(["","","Dados da Amostra"])
                         editor.writerow(["","","Peso submerso", "Peso ao ar", "Temperatura", "Diametro", "altura"])
                         editor.writerow(["","",DA[0][1], DA[0][2], DA[0][3], DA[0][4], DA[0][5]])
                         editor.writerow(["","","","","","","","","","","","","","","",""])
                         editor.writerow(["","","deslocamento","forca"])
                         for leitura in leituras:
                             #leitura = format(leitura).replace('.',',')
                             editor.writerow(["","",leitura[1],leitura[2]])
               except IOError:
                    wx.LogError("O arquivo não pôde ser salvo em '%s'." % pathname)
