# -*- coding: utf-8 -*-
import wx
import time
import banco.bdConfiguration as bdConfiguration
import back.connection as con
import math
import wx.adv
from pubsub import publish

class SetarPressaoGolpe():

    def __init__(self,pressGolpe,PressaoAtual,diametro):
        self.pressGolpe=pressGolpe
        self.diametro=diametro
        self.p1Ant=PressaoAtual
        self.run()

    def run(self):
        E = bdConfiguration.DadosD1()
        # A1 = bdConfiguration.DadosCL()
        pi = math.pi
        A2 = (self.diametro*self.diametro)*(pi/4)

        # const = abs(round(A2/A1,3))
        # if(const > 1.05 or const < 0.95):
        #     const = 1

        AE2= float(E[1])
        BE2= float(E[2])

        pressao1 = (10000*self.pressGolpe)*AE2+BE2
        pressao1Ant = (10000*self.p1Ant)*AE2+BE2

        time.sleep(.5)
        con.modeE() #envia para o arduino o codigo para alterar a pressão
        time.sleep(.5)
        valor1 = con.modeDIN(pressao1, pressao1Ant) #envia para o arduino o valor de pressão do golpe de modo incremental
        if valor1 == 'p_ok':
            print ('PRESSAO GOLPE OK')
            time.sleep(1)


class ZerarPressaoGolpe():

    def __init__(self, p1Sen):
        self.p1Sen = p1Sen
        self.run()

    def run(self):
        E = bdConfiguration.DadosD1()
   
        AE2= float(E[1])
        BE2= float(E[2])

        pressao1 = 0
        pressao1Sen = (10000*self.p1Sen)*AE2+BE2

        time.sleep(5)
        con.modeES()
        time.sleep(0.5)
        valor1 = con.modeDINZERO(0, pressao1Sen )
        if valor1 == 'p_ok':
            print ('PRESSAO GOLPE ZERADO')
            time.sleep(1)
            

class SetarPressaoCamara():
    def __init__(self,pressaoCamara,PressaoAtual):
        self.pressao=pressaoCamara
        self.pressAtual=PressaoAtual
        self.run()

    def run(self):
        F = bdConfiguration.DadosD2()
        AF2= float(F[1])
        BF2= float(F[2])

        presao2 = (10000*self.pressao)*AF2+BF2
        pressAnt=(10000*self.pressAtual)*AF2+BF2

        time.sleep(.5)
        con.modeF()
        time.sleep(.5)
        valor2 = con.modeDIN(presao2, pressAnt)
        if valor2 == 'p_ok':
            print ('PRESSAO CAMARA OK')
            time.sleep(1) 

class ZerarPressaoCamara():
    def __init__(self,pressaoCamara):
        self.pressao=pressaoCamara
        self.run()

    def run(self):
        F = bdConfiguration.DadosD2()
        AF2= float(F[1])
        BF2= float(F[2])

        presao2 = (10000*self.pressao)*AF2+BF2

        time.sleep(.5)
        con.modeFS()
        time.sleep(.5)
        valor2 = con.modeDINZERO(0, presao2)
        if valor2 == 'p_ok':
            print ('PRESSAO CAMARA ZERADA')
            time.sleep(1) 


