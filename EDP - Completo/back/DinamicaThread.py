# -*- coding: utf-8 -*-
import wx
import time
import banco.bdConfiguration as bdConfiguration
import back.connection as con
import math
from pubsub import publish
from threading import Thread

global A2 #área do corpo de prova, vinda do banco de dados do Ensaio
global A1 #área da seção do cilindro pneumático

'''DinamicaThreadTwo'''
class DinamicaThreadTwo(Thread): #define a pressão confinate
    #-------------------------------------------------------------------
    def __init__(self, p2, p2Ant):
        Thread.__init__(self)
        self.p2 = p2
        self.p2Ant = p2Ant
        self._return = True
        self.start()

    #-------------------------------------------------------------------
    def run(self):
        F = bdConfiguration.DadosD2()
        AF2= float(F[1])
        BF2= float(F[2])

        presao2 = (10000*self.p2)*AF2+BF2
        pressao2Ant = (10000*self.p2Ant)*AF2+BF2

        con.modeS()
        wx.CallAfter(publish.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(.5)
        con.modeF()
        wx.CallAfter(publish.sendMessage, "update", msg="       Regulando...")
        time.sleep(.5)
        valor2 = con.modeDIN(presao2, pressao2Ant)
        if valor2 == 'p_ok':
            print ('PRESSAO CAMARA OK')
            wx.CallAfter(publish.sendMessage, "update", msg="            σ3 - ok")
            time.sleep(1)

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

'''DinamicaThreadTwoZero'''
class DinamicaThreadTwoZero(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p2, p2Sen):
        Thread.__init__(self) 
        self.p2 = p2
        self.p2Sen = p2Sen
        self._return = True
        self.start()

    #-------------------------------------------------------------------
    def run(self):
        F = bdConfiguration.DadosD2()
        AF2= float(F[1])
        BF2= float(F[2])
        
        presao2 = (10000*self.p2)*AF2+BF2
        pressao2Sen = (10000*self.p2Sen)*AF2+BF2

        con.modeS()
        wx.CallAfter(publish.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(.5)
        con.modeFS()
        wx.CallAfter(publish.sendMessage, "update", msg="         Zerando...")
        time.sleep(.5)
        valor2 = con.modeDINZERO(presao2, pressao2Sen)
        if valor2 == 'p_ok':
            print ('PRESSAO CAMARA ZERADO')
            wx.CallAfter(publish.sendMessage, "update", msg="       σ3 - Zerado!")
            time.sleep(1)
            wx.CallAfter(publish.sendMessage, "update", msg="")

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

########################################################################
########################################################################
########################################################################
'''DinamicaThreadOne'''
class DinamicaThreadOne(Thread): # define a pressão do golpe sigmad
    #-------------------------------------------------------------------
    def __init__(self, p1, p1Ant, Diametro):
        Thread.__init__(self)
        self.p1 = p1
        self.p1Ant = p1Ant
        self.Diam = Diametro
        self._return = True
        self.start()

    #-------------------------------------------------------------------
    def run(self):
        E = bdConfiguration.DadosD1()
        A1 = bdConfiguration.DadosCL()
        pi = math.pi
        A2 = (self.Diam*self.Diam)*(pi/4)

        const = abs(round(A2/A1,3))
        if(const > 1.05 or const < 0.95):
            const = 1

        AE2= float(E[1])
        BE2= float(E[2])

        pressao1 = (10000*(const)*self.p1)*AE2+BE2
        pressao1Ant = (10000*(const)*self.p1Ant)*AE2+BE2

        con.modeS()
        wx.CallAfter(publish.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(.5)
        con.modeE()
        wx.CallAfter(publish.sendMessage, "update", msg="       Regulando...")
        time.sleep(.5)
        valor1 = con.modeDIN(pressao1, pressao1Ant)
        if valor1 == 'p_ok':
            print ('PRESSAO GOLPE OK')
            wx.CallAfter(publish.sendMessage, "update", msg="            σd - ok")
            time.sleep(1)

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return

'''DinamicaThreadOneZero'''
class DinamicaThreadOneZero(Thread):
    #-------------------------------------------------------------------
    def __init__(self, p1, p1Sen):
        Thread.__init__(self)
        self.p1 = p1
        self.p1Sen = p1Sen
        self._return = True
        self.start()

    #-------------------------------------------------------------------
    def run(self):
        E = bdConfiguration.DadosD1()
   
        AE2= float(E[1])
        BE2= float(E[2])

        pressao1 = (10000*self.p1)*AE2+BE2
        pressao1Sen = (10000*self.p1Sen)*AE2+BE2

        con.modeS()
        wx.CallAfter(publish.sendMessage, "update", msg="Ativando válvula...")
        time.sleep(.5)
        con.modeES()
        wx.CallAfter(publish.sendMessage, "update", msg="         Zerando...")
        time.sleep(.5)
        valor1 = con.modeDINZERO(pressao1, pressao1Sen )
        if valor1 == 'p_ok':
            print ('PRESSAO GOLPE ZERADO')
            wx.CallAfter(publish.sendMessage, "update", msg="       σd - Zerado!")
            time.sleep(1)
            wx.CallAfter(publish.sendMessage, "update", msg="")

    #-------------------------------------------------------------------
    def ret(self):
        Thread.join(self)
        return self._return
