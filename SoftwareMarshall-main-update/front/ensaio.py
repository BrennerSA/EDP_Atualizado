# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import time
import datetime
import math
import serial
import threading
import front.tela
# import bancodedados
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from sys import *
from serial.tools import list_ports
from telagrafico import TelaRealizacaoEnsaioDNER04395

'''Variaveis Globais'''
rate = 115200
opcaoC = "C"
opcaoD = "D"
opcaoI = "I"
pi = math.pi
vetor = []

'''Tela Cadastrar Cápsula'''
class Ensaio(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, id, y, Assentamento, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'Software Marshall - Conexão com Arduino', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)

            self.panel = wx.Panel(self)
            self.SetSize((620,100))
            self.Centre()
            self.Show()

            '''ComboBox Port Serial'''
            portlist = [port for port,desc,hwin in list_ports.comports()]

            try:
                self.cboCPort = wx.ComboBox(self.panel, -1, portlist[0] , (80,20), (60, -1), choices=portlist)
            except IndexError:
                self.cboCPort = wx.ComboBox(self.panel, -1, '', (80,20), (60, -1), choices=portlist)
                self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.onCheck, self.cboCPort)

            self.text00 = wx.StaticText(self.panel, -1, "COM Port", (20,24), (60,-1), wx.ALIGN_LEFT)

            self.FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            self.continuar = wx.Button(self.panel, -1, 'Iniciar', (140, 20), (400,-1), wx.ALIGN_LEFT)
            self.Bind(wx.EVT_BUTTON, self.proximo, self.continuar)


    #--------------------------------------------------
        def onCheck(self, event):
            '''Atualiza os COM Port quando clica-se no ComboBox'''
            '''ComboBox Port Serial'''
            portlist = [port for port,desc,hwin in list_ports.comports()]

            self.cboCPort.Destroy()
            try:
                self.cboCPort = wx.ComboBox(self.panel, -1, portlist[0] , (80,20), (60, -1), choices=portlist)
                self.cboCPort.Update()
            except IndexError:
                self.cboCPort = wx.ComboBox(self.panel, -1, '', (80,20), (60, -1), choices=portlist)
                self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.onCheck, self.cboCPort)
                self.cboCPort.Update()


    #--------------------------------------------------
        def plot(self,leituras):
            y = leituras
            x = range(len(leituras))
            fig = plt.figure()
            ax = fig.add_subplot(1,1,1)
            ax.plot(x,y)
            plt.show()
            plt.savefig('foo.png')
    #--------------------------------------------------
        def proximo(self,event):
		 	# frame = TelaRealizacaoEnsaioDNER04395(1)
            porta = self.cboCPort.GetValue()
            self.conexao = serial.Serial(porta,rate)
            if(self.conexao.isOpen() == True):
                self.Close(True)
                frame = TelaRealizacaoEnsaioDNER04395(self.conexao).ShowModal()
            if(self.conexao.isOpen() == False):
                print("Conexão falhou!")
