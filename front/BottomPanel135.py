# -*- coding: utf-8 -*-

import wx
import time
import threading
import matplotlib
import numpy as np
import banco.bancodedados as bancodedados
import banco.bdConfiguration as bdConfiguration
import back.connection as con
import matplotlib.pyplot as plt
import back.MyProgressDialog as My
import back.SaveThread as SaveThread
import back.MotorThread as MotorThread
import back.DinamicaThread as DinamicaThread
import back.ConexaoThread as ConexaoThread
import back.HexForRGB as HexRGB
import banco.bdPreferences as bdPreferences
import back.ThreadLeituraDados as ThreadLeituraDados
import back.SetarPressoes as SetarPressoes
from drawnow import *
from front.quadrotensoes import quadro
from front.dialogoDinamico import dialogoDinamico
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

frequencias = ['1','2','3']




class BottomPanel(wx.Panel):
        threadLeituraDados=ThreadLeituraDados.Thread
        Fase=''
        Main=None
        def __init__(self,main, parent, NomeEnsaio, top):
            self.Nome=NomeEnsaio
            self.TopPanel=top
            self.mult=0
            self.Main=main
            wx.Panel.__init__(self, parent = parent)
            self.ensaio=bancodedados.tipo_ensaio(NomeEnsaio)
            if self.ensaio[0]=='135' :
                self.resistencia=float(self.ensaio[25])
                self.glpCOND=50
                self.glpMR=15
                self.glpRT=5
                self.condRT=False
                self.onlyMR=False
                if self.resistencia==0:
                    self.resistencia=0.05
                else:
                    self.TopPanel.PressaoAtualGolpe=self.resistencia*float(self.ensaio[26])
            elif self.ensaio[0]=='134':
                pressoes = bdConfiguration.QD_134_MOD() # OBTEM AS PRESSÕES PARA O CONDICIONAMENTO E O ENSAIO
                self.pressoesCONDICIONAMENTO=pressoes[0]
                self.pressoesMR=pressoes[1]
                self.tipo=self.ensaio[3]
                self.glpCOND = 500
                self.glpMR = 10
                self.DISCREP= 1.05 
            elif self.ensaio[0]=='181':
                self.pressoes = bdConfiguration.QD_181()
                self.glpCOND=0
                self.glpMR=50
            elif self.ensaio[0]=='179':
                self.pressoes=bdConfiguration.QD_179_MOD()  
                self.config = bdConfiguration.CONFIG_179()
                self.VETOR_COND = self.pressoes[0]
                self.VETOR_DP =  [self.pressoes[1][int(self.ensaio[3])]]
                self.glpDP=30000
                self.glpCOND=50
                
            self.diametro=self.ensaio[14]
            self.altura=self.ensaio[15]

            colors = bdPreferences.ListColors()
            colorCard = colors[0]
            colorTextCtrl = colors[1]
            colorBackground = colors[2]
            colorLineGrafic = colors[3]
            colorBackgroundGrafic = colors[4]

            colorStaticBox = HexRGB.RGB(colorCard)
            colorTextBackground = HexRGB.RGB(colorCard)
            colorTextCtrl = HexRGB.RGB(colorTextCtrl)

            self.graph = top

            self.SetBackgroundColour(colorBackground)         

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontTitle1 = wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD)
            Fonttext = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            staticbox1 = wx.StaticBox(self, -1, '')
            staticbox2 = wx.StaticBox(self, -1, '')
            staticbox3 = wx.StaticBox(self, -1, '')
            staticbox4 = wx.StaticBox(self, -1, '')
            staticbox5 = wx.StaticBox(self, -1, '')
            staticbox6 = wx.StaticBox(self, -1, '')

            staticboxSizer1 = wx.StaticBoxSizer(staticbox1, wx.VERTICAL)
            staticboxSizer2 = wx.StaticBoxSizer(staticbox2, wx.VERTICAL)
            staticboxSizer3 = wx.StaticBoxSizer(staticbox3, wx.VERTICAL)
            staticboxSizer4 = wx.StaticBoxSizer(staticbox4, wx.VERTICAL)
            staticboxSizer5 = wx.StaticBoxSizer(staticbox5, wx.VERTICAL)
            staticboxSizer6 = wx.StaticBoxSizer(staticbox6, wx.VERTICAL)

            staticbox1.SetBackgroundColour(colorStaticBox)
            staticbox2.SetBackgroundColour(colorStaticBox)
            staticbox3.SetBackgroundColour(colorStaticBox)
            staticbox4.SetBackgroundColour(colorStaticBox)
            staticbox5.SetBackgroundColour(colorStaticBox)
            staticbox6.SetBackgroundColour(colorStaticBox)

            self.condic = wx.Button(self, -1, 'CONDIC.')
            self.Bind(wx.EVT_BUTTON, self.CONDIC, self.condic)
            if self.ensaio[0]=='179':
                self.gDP = wx.Button(self, -1, 'GOLPE\nX\nD. P.')
                self.Bind(wx.EVT_BUTTON, self.GDP, self.gDP)
                self.dp=wx.Button(self, -1, 'D. P.')
                self.Bind(wx.EVT_BUTTON, self.MR, self.dp)
                self.dp.Disable()
                self.dp.SetFont(FontTitle1)
            elif self.ensaio[0]=='134':   
                self.qTensoes = wx.Button(self, -1, 'Q. Tensões')
                self.Bind(wx.EVT_BUTTON, self.QT, self.qTensoes)     
                self.mr = wx.Button(self, -1, 'M. R.')
                self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
                self.mr.Disable()
                self.mr.SetFont(FontTitle1)
            elif self.ensaio[0]=='135':
                self.mr = wx.Button(self, -1, 'M. R.')
                self.Bind(wx.EVT_BUTTON, self.MR, self.mr)
                self.mr.Disable()
                self.mr.SetFont(FontTitle1)
            self.LTeste = wx.Button(self, -1, "CONECTAR", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LTESTE, self.LTeste)
            self.LZero = wx.Button(self, -1, "L. ZERO", size = wx.DefaultSize)
            self.Bind(wx.EVT_BUTTON, self.LZERO, self.LZero)
            self.DialogCarregamento = wx.Button(self,-1,"dialog")
            self.Bind(wx.EVT_BUTTON,self.dialogoCarregamento,self.DialogCarregamento)
            

            self.DialogCarregamento.Hide()

            if self.ensaio[0]=='134':
                self.qTensoes.Disable()
                self.qTensoes.SetFont(FontTitle1)
            elif self.ensaio[0]=='179':
                self.gDP.Disable()     
                self.gDP.SetFont(FontTitle1)
            self.condic.Disable()
            self.LZero.Disable()

            
            self.condic.SetFont(FontTitle1)
            self.LTeste.SetFont(FontTitle1)
            self.LZero.SetFont(FontTitle1)


            #--------------------------------------------------
            '''Static Box 1'''
            if self.ensaio[0]!='135':               
                texto_eixo_y = wx.StaticText(self, label = "EIXO Y", style = wx.ALIGN_CENTRE)
                texto_y1_V = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
                texto_y2_V = wx.StaticText(self, label = "Y2 (V)", style = wx.ALIGN_CENTER)
                texto_y1 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)
                texto_y2 = wx.StaticText(self, label = "Y2 (mm)", style = wx.ALIGN_CENTER)

                texto_eixo_y.SetFont(FontTitle)
                texto_y1_V.SetFont(Fonttext)
                texto_y2_V.SetFont(Fonttext)
                texto_y1.SetFont(Fonttext)
                texto_y2.SetFont(Fonttext)

                texto_eixo_y.SetBackgroundColour(colorTextBackground )
                texto_y1_V.SetBackgroundColour(colorTextBackground )
                texto_y2_V.SetBackgroundColour(colorTextBackground )
                texto_y1.SetBackgroundColour(colorTextBackground )
                texto_y2.SetBackgroundColour(colorTextBackground )

                self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y2V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y2mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

                self.y1V.SetFont(Fonttext)
                self.y2V.SetFont(Fonttext)
                self.y1mm.SetFont(Fonttext)
                self.y2mm.SetFont(Fonttext)

                self.y1V.SetForegroundColour(colorTextCtrl)
                self.y2V.SetForegroundColour(colorTextCtrl)
                self.y1mm.SetForegroundColour(colorTextCtrl)
                self.y2mm.SetForegroundColour(colorTextCtrl)

                self.y1V.Disable()
                self.y2V.Disable()
                self.y1mm.Disable()
                self.y2mm.Disable()

                self.v16_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v17_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v18_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v19_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v20_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v21_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h19_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h20_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h21_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h22_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.v16_sizer.Add(texto_y2, 1, wx.CENTER)
                self.v16_sizer.Add(self.y2mm, 2, wx.CENTER)

                self.v17_sizer.Add(texto_y2_V, 1, wx.CENTER)
                self.v17_sizer.Add(self.y2V, 2, wx.CENTER)

                self.v18_sizer.Add(texto_y1, 1, wx.CENTER)
                self.v18_sizer.Add(self.y1mm, 2, wx.CENTER)

                self.v19_sizer.Add(texto_y1_V, 1, wx.CENTER)
                self.v19_sizer.Add(self.y1V, 2, wx.CENTER)

                self.h19_sizer.Add(self.v17_sizer, 5, wx.ALL | wx.CENTER)
                self.h19_sizer.AddStretchSpacer(1)
                self.h19_sizer.Add(self.v16_sizer, 5, wx.ALL | wx.CENTER)

                self.h20_sizer.Add(self.v19_sizer, 5, wx.ALL | wx.CENTER)
                self.h20_sizer.AddStretchSpacer(1)
                self.h20_sizer.Add(self.v18_sizer, 5, wx.ALL | wx.CENTER)

                self.h21_sizer.Add(self.LTeste, 5, wx.EXPAND)
                self.h21_sizer.AddStretchSpacer(2)
                self.h21_sizer.Add(self.LZero, 5, wx.EXPAND)

                self.v20_sizer.Add(self.h20_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(1)
                self.v20_sizer.Add(self.h19_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(2)
                self.v20_sizer.Add(self.h21_sizer, 2, wx.CENTER)

                self.v21_sizer.Add(texto_eixo_y, 1, wx.CENTER)
                self.v21_sizer.Add(self.v20_sizer, 7, wx.CENTER)

                self.h22_sizer.Add(self.v21_sizer, 1, wx.CENTER)
                staticboxSizer1.Add(self.h22_sizer, 0,  wx.ALL | wx.EXPAND  | wx.CENTER, 10)
            elif self.ensaio[0]=='135':
                texto_eixo_y = wx.StaticText(self, label = "EIXO Y", style = wx.ALIGN_CENTRE)
                texto_y1_V = wx.StaticText(self, label = "Y1 (V)", style = wx.ALIGN_CENTER)
                texto_y1 = wx.StaticText(self, label = "Y1 (mm)", style = wx.ALIGN_CENTER)

                texto_eixo_y.SetFont(FontTitle)
                texto_y1_V.SetFont(Fonttext)
                texto_y1.SetFont(Fonttext)

                texto_eixo_y.SetBackgroundColour(colorTextBackground )
                texto_y1_V.SetBackgroundColour(colorTextBackground )
                texto_y1.SetBackgroundColour(colorTextBackground )

                self.y1V = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.y1mm = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

                self.y1V.SetFont(Fonttext)
                self.y1mm.SetFont(Fonttext)

                self.y1V.SetForegroundColour(colorTextCtrl)
                self.y1mm.SetForegroundColour(colorTextCtrl)

                self.y1V.Disable()
                self.y1mm.Disable()

                self.v16_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v17_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v18_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v19_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v20_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v21_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h19_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h20_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h21_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h22_sizer = wx.BoxSizer(wx.HORIZONTAL)

                # self.v16_sizer.Add(texto_y2, 1, wx.CENTER)
                # self.v16_sizer.Add(self.y2mm, 2, wx.CENTER)

                # self.v17_sizer.Add(texto_y2_V, 1, wx.CENTER)
                # self.v17_sizer.Add(self.y2V, 2, wx.CENTER)

                self.v18_sizer.Add(texto_y1, 1, wx.CENTER)
                self.v18_sizer.Add(self.y1mm, 2, wx.CENTER)

                self.v19_sizer.Add(texto_y1_V, 1, wx.CENTER)
                self.v19_sizer.Add(self.y1V, 2, wx.CENTER)

                self.h19_sizer.Add(self.v17_sizer, 5, wx.ALL | wx.CENTER)
                self.h19_sizer.AddStretchSpacer(1)
                self.h19_sizer.Add(self.v16_sizer, 5, wx.ALL | wx.CENTER)

                self.h20_sizer.Add(self.v19_sizer, 5, wx.ALL | wx.CENTER)
                self.h20_sizer.AddStretchSpacer(1)
                self.h20_sizer.Add(self.v18_sizer, 5, wx.ALL | wx.CENTER)

                self.h21_sizer.Add(self.LTeste, 5, wx.EXPAND)
                self.h21_sizer.AddStretchSpacer(2)
                self.h21_sizer.Add(self.LZero, 5, wx.EXPAND)

                self.v20_sizer.Add(self.h20_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(1)
                self.v20_sizer.Add(self.h19_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(2)
                self.v20_sizer.Add(self.h21_sizer, 2, wx.CENTER)

                self.v21_sizer.Add(texto_eixo_y, 1, wx.CENTER)
                self.v21_sizer.Add(self.v20_sizer, 7, wx.CENTER)

                self.h22_sizer.Add(self.v21_sizer, 1, wx.CENTER)
                staticboxSizer1.Add(self.h22_sizer, 0,  wx.ALL | wx.EXPAND  | wx.CENTER, 10)
            else:

                self.v16_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v17_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v18_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v19_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v20_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v21_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h19_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h20_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h21_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h22_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.h19_sizer.Add(self.v17_sizer, 5, wx.ALL | wx.CENTER)
                self.h19_sizer.AddStretchSpacer(1)
                self.h19_sizer.Add(self.v16_sizer, 5, wx.ALL | wx.CENTER)

                self.h20_sizer.Add(self.v19_sizer, 5, wx.ALL | wx.CENTER)
                self.h20_sizer.AddStretchSpacer(1)
                self.h20_sizer.Add(self.v18_sizer, 5, wx.ALL | wx.CENTER)

                self.h21_sizer.Add(self.LTeste, 5, wx.EXPAND)
                self.h21_sizer.AddStretchSpacer(2)
                self.h21_sizer.Add(self.LZero, 5, wx.EXPAND)

                self.v20_sizer.Add(self.h20_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(1)
                self.v20_sizer.Add(self.h19_sizer, 3, wx.CENTER)
                self.v20_sizer.AddStretchSpacer(2)
                self.v20_sizer.Add(self.h21_sizer, 2, wx.CENTER)

                # self.v21_sizer.Add(texto_eixo_y, 1, wx.CENTER)
                self.v21_sizer.Add(self.v20_sizer, 7, wx.CENTER)

                self.h22_sizer.Add(self.v21_sizer, 1, wx.CENTER)
                staticboxSizer1.Add(self.h22_sizer, 0,  wx.ALL | wx.EXPAND  | wx.CENTER, 10)


            #--------------------------------------------------
            '''Static Box 2'''
            

            #--------------------------------------------------
            '''Static Box 3'''
            if self.ensaio[0] == '134' or self.ensaio[0] == '179':
                texto_sigma3 = wx.StaticText(self, label = "σ3 - Tensão confinante (MPa)", style = wx.ALIGN_CENTRE)
                texto_real1 = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
                texto_alvo1 = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
                
                texto_sigma3.SetFont(FontTitle)
                texto_real1.SetFont(Fonttext)
                texto_alvo1.SetFont(Fonttext)
                
                texto_real1.SetBackgroundColour(colorTextBackground )
                texto_alvo1.SetBackgroundColour(colorTextBackground )
                texto_sigma3.SetBackgroundColour(colorTextBackground )
                
                self.PCreal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.PCalvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

                self.PCreal.Disable()
                self.PCalvo.Disable()

                self.PCreal.SetFont(Fonttext)
                self.PCalvo.SetFont(Fonttext)

                self.PCreal.SetForegroundColour(colorTextCtrl)
                self.PCalvo.SetForegroundColour(colorTextCtrl)

                self.v12_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v13_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v14_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h12_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.v12_sizer.Add(texto_alvo1, 1, wx.ALL | wx.CENTER)
                self.v12_sizer.Add(self.PCalvo, 2, wx.ALL | wx.CENTER)

                self.v13_sizer.Add(texto_real1, 1, wx.ALL | wx.CENTER)
                self.v13_sizer.Add(self.PCreal, 2, wx.ALL | wx.CENTER)

                self.h11_sizer.Add(self.v13_sizer, 6, wx.CENTER)
                self.h11_sizer.AddStretchSpacer(1)
                self.h11_sizer.Add(self.v12_sizer, 6, wx.CENTER)

                self.v14_sizer.Add(texto_sigma3, 1, wx.ALL | wx.CENTER)
                self.v14_sizer.Add(self.h11_sizer, 3, wx.ALL | wx.CENTER)

                self.h12_sizer.Add(self.v14_sizer, 1, wx.CENTER)
                staticboxSizer3.Add(self.h12_sizer, 0, wx.ALL | wx.CENTER, 10)

            elif self.ensaio[0]=='135':
                texto_sigma3 = wx.StaticText(self, label = "Modulos", style = wx.ALIGN_CENTRE)
                textoMI     = wx.StaticText(self, label = "MI", style = wx.ALIGN_CENTER)
                texto_real1 = wx.StaticText(self, label = "MR", style = wx.ALIGN_CENTER)
                texto_alvo1 = wx.StaticText(self, label = "MT", style = wx.ALIGN_CENTER)
                
                texto_sigma3.SetFont(FontTitle)
                textoMI.SetFont(Fonttext)
                texto_real1.SetFont(Fonttext)
                texto_alvo1.SetFont(Fonttext)
                
                texto_real1.SetBackgroundColour(colorTextBackground )
                textoMI.SetBackgroundColour(colorTextBackground )
                texto_alvo1.SetBackgroundColour(colorTextBackground )
                texto_sigma3.SetBackgroundColour(colorTextBackground )
                
                self.PCreal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 21), style = wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER)
                self.textoMI = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 21), style = wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER)
                self.PCalvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 21), style = wx.TE_READONLY | wx.TE_CENTER | wx.TEXT_ALIGNMENT_CENTER)

                self.PCreal.Disable()
                self.PCalvo.Disable()
                self.textoMI.Disable()

                self.PCreal.SetFont(Fonttext)
                self.PCalvo.SetFont(Fonttext)
                self.textoMI.SetFont(Fonttext)

                self.PCreal.SetForegroundColour(colorTextCtrl)
                self.PCalvo.SetForegroundColour(colorTextCtrl)
                self.textoMI.SetForegroundColour(colorTextCtrl)

                self.v12_sizer = wx.BoxSizer(wx.VERTICAL)
                self.extra_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v13_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v14_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h12_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.v12_sizer.Add(texto_alvo1, 1, wx.ALL | wx.CENTER)
                self.v12_sizer.Add(self.PCalvo, 2, wx.ALL | wx.CENTER)

                self.v13_sizer.Add(texto_real1, 1, wx.ALL | wx.CENTER)
                self.v13_sizer.Add(self.PCreal, 2, wx.ALL | wx.CENTER)

                self.extra_sizer.Add(textoMI, 1, wx.ALL | wx.CENTER)
                self.extra_sizer.Add(self.textoMI, 2, wx.ALL | wx.CENTER)

                self.h11_sizer.Add(self.extra_sizer, 6, wx.CENTER)
                self.h11_sizer.AddStretchSpacer(1)
                self.h11_sizer.Add(self.v13_sizer, 6, wx.CENTER)
                self.h11_sizer.AddStretchSpacer(1)
                self.h11_sizer.Add(self.v12_sizer, 6, wx.CENTER)
                
                

                self.v14_sizer.Add(texto_sigma3, 1, wx.ALL | wx.CENTER)
                self.v14_sizer.Add(self.h11_sizer, 3, wx.ALL | wx.CENTER)

                self.h12_sizer.Add(self.v14_sizer, 1, wx.CENTER)
                staticboxSizer3.Add(self.h12_sizer, 0, wx.ALL | wx.CENTER, 10)
            

            #--------------------------------------------------
            '''Static Box 4'''


            texto_altura = wx.StaticText(self, label = "Altura (mm)", style = wx.ALIGN_LEFT)
            texto_diametro = wx.StaticText(self, label = "Diâmetro (mm)", style = wx.ALIGN_LEFT)
            if self.ensaio[0]!='135':
                texto_altura_final = wx.StaticText(self, label = "Altura Final (mm)", style = wx.ALIGN_LEFT)
            else:
                texto_altura_final = wx.StaticText(self, label = "Diametro Final (mm)", style = wx.ALIGN_LEFT)

            texto_altura.SetFont(Fonttext)
            texto_diametro.SetFont(Fonttext)
            texto_altura_final.SetFont(FontTitle)

            texto_altura.SetBackgroundColour(colorTextBackground )
            texto_diametro.SetBackgroundColour(colorTextBackground )
            texto_altura_final.SetBackgroundColour(colorTextBackground )

            self.AlturaFinal = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.AlturaMM = wx.TextCtrl(self, -1, str(self.altura), size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)
            self.DiametroMM = wx.TextCtrl(self, -1, str(self.diametro), size = (80, 41), style = wx.TE_READONLY | wx.TE_CENTER)

            self.AlturaMM.Disable()
            self.DiametroMM.Disable()
            self.AlturaFinal.Disable()

            self.AlturaMM.SetFont(Fonttext)
            self.DiametroMM.SetFont(Fonttext)
            self.AlturaFinal.SetFont(Fonttext)

            self.AlturaMM.SetForegroundColour(colorTextCtrl)
            self.DiametroMM.SetForegroundColour(colorTextCtrl)
            self.AlturaFinal.SetForegroundColour(colorTextCtrl)

            self.v11_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h10_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.h7_sizer.Add(texto_altura, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h7_sizer.AddStretchSpacer(1)
            self.h7_sizer.Add(self.AlturaMM, 5, wx.CENTER)

            self.h8_sizer.Add(texto_diametro, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h8_sizer.AddStretchSpacer(1)
            self.h8_sizer.Add(self.DiametroMM, 5, wx.CENTER)

            self.h9_sizer.Add(texto_altura_final, 7, wx.ALIGN_CENTER_VERTICAL)
            self.h9_sizer.AddStretchSpacer(1)
            self.h9_sizer.Add(self.AlturaFinal, 5, wx.CENTER)

            self.v11_sizer.Add(self.h7_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v11_sizer.AddStretchSpacer(1)
            self.v11_sizer.Add(self.h8_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)
            self.v11_sizer.AddStretchSpacer(1)
            self.v11_sizer.Add(self.h9_sizer, 5, wx.ALL | wx.EXPAND  | wx.CENTER)

            self.h10_sizer.Add(self.v11_sizer, 1, wx.CENTER)
            staticboxSizer4.Add(self.h10_sizer, 0, wx.ALL | wx.EXPAND  | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 5'''
            if self.ensaio[0] == '134' or self.ensaio[0] == '179':
                texto_sigmad = wx.StaticText(self, label = "σd - Tensão desvio (MPa)", style = wx.ALIGN_CENTRE)
                texto_real = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
                texto_alvo = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
                            
                texto_sigmad.SetFont(FontTitle)
                texto_real.SetFont(Fonttext)
                texto_alvo.SetFont(Fonttext)

                texto_sigmad.SetBackgroundColour(colorTextBackground )
                texto_real.SetBackgroundColour(colorTextBackground )
                texto_alvo.SetBackgroundColour(colorTextBackground )

                self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

                self.SigmaReal.Disable()
                self.SigmaAlvo.Disable()

                self.SigmaReal.SetFont(Fonttext)
                self.SigmaAlvo.SetFont(Fonttext)

                self.SigmaReal.SetForegroundColour(colorTextCtrl)
                self.SigmaAlvo.SetForegroundColour(colorTextCtrl)

                self.v8_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v9_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v10_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h6_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.v8_sizer.Add(texto_alvo, 1, wx.ALL | wx.CENTER)
                self.v8_sizer.Add(self.SigmaAlvo, 2, wx.ALL | wx.CENTER)

                self.v9_sizer.Add(texto_real, 1, wx.ALL | wx.CENTER)
                self.v9_sizer.Add(self.SigmaReal, 2, wx.ALL | wx.CENTER)

                self.h5_sizer.Add(self.v9_sizer, 6, wx.CENTER)
                self.h5_sizer.AddStretchSpacer(1)
                self.h5_sizer.Add(self.v8_sizer, 6, wx.CENTER)

                self.v10_sizer.Add(texto_sigmad, 1, wx.ALL | wx.CENTER)
                self.v10_sizer.Add(self.h5_sizer, 3, wx.ALL | wx.CENTER)

                self.h6_sizer.Add(self.v10_sizer, 1, wx.CENTER)
                staticboxSizer5.Add(self.h6_sizer, 0, wx.ALL | wx.CENTER, 10)
            
            elif self.ensaio[0] in ['135','181']: 
                texto_sigma1 = wx.StaticText(self, label = "σ1 - Tensão Golpe (MPa)", style = wx.ALIGN_CENTRE)
                texto_real = wx.StaticText(self, label = "REAL", style = wx.ALIGN_CENTER)
                texto_alvo = wx.StaticText(self, label = "ALVO", style = wx.ALIGN_CENTER)
                            
                texto_sigma1.SetFont(FontTitle)
                texto_real.SetFont(Fonttext)
                texto_alvo.SetFont(Fonttext)

                texto_sigma1.SetBackgroundColour(colorTextBackground )
                texto_real.SetBackgroundColour(colorTextBackground )
                texto_alvo.SetBackgroundColour(colorTextBackground )

                self.SigmaReal = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)
                self.SigmaAlvo = wx.TextCtrl(self, -1, wx.EmptyString, size = (100, 41), style = wx.TE_READONLY | wx.TE_CENTER)

                self.SigmaReal.Disable()
                self.SigmaAlvo.Disable()

                self.SigmaReal.SetFont(Fonttext)
                self.SigmaAlvo.SetFont(Fonttext)

                self.SigmaReal.SetForegroundColour(colorTextCtrl)
                self.SigmaAlvo.SetForegroundColour(colorTextCtrl)

                self.v8_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v9_sizer = wx.BoxSizer(wx.VERTICAL)
                self.v10_sizer = wx.BoxSizer(wx.VERTICAL)
                self.h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
                self.h6_sizer = wx.BoxSizer(wx.HORIZONTAL)

                self.v8_sizer.Add(texto_alvo, 1, wx.ALL | wx.CENTER)
                self.v8_sizer.Add(self.SigmaAlvo, 2, wx.ALL | wx.CENTER)

                self.v9_sizer.Add(texto_real, 1, wx.ALL | wx.CENTER)
                self.v9_sizer.Add(self.SigmaReal, 2, wx.ALL | wx.CENTER)

                self.h5_sizer.Add(self.v9_sizer, 6, wx.CENTER)
                self.h5_sizer.AddStretchSpacer(1)
                self.h5_sizer.Add(self.v8_sizer, 6, wx.CENTER)

                self.v10_sizer.Add(texto_sigma1, 1, wx.ALL | wx.CENTER)
                self.v10_sizer.Add(self.h5_sizer, 3, wx.ALL | wx.CENTER)

                self.h6_sizer.Add(self.v10_sizer, 1, wx.CENTER)
                staticboxSizer5.Add(self.h6_sizer, 0, wx.ALL | wx.CENTER, 10)

            #--------------------------------------------------
            '''Static Box 6'''
            
            texto_fase = wx.StaticText(self, label = "FASE", style = wx.ALIGN_CENTER)
            texto_numero_ciclos = wx.StaticText(self, label = "Nº de CICLOs", style = wx.ALIGN_CENTER)
            texto_frequencia = wx.StaticText(self, label = "Freq. (Hz)", style = wx.ALIGN_CENTER)
            texto_ciclo_atual = wx.StaticText(self, label = "CICLO Atual", style = wx.ALIGN_CENTER)

            texto_fase.SetFont(FontTitle)
            texto_numero_ciclos.SetFont(Fonttext)
            texto_frequencia.SetFont(Fonttext)
            texto_ciclo_atual.SetFont(Fonttext)

            texto_fase.SetBackgroundColour(colorTextBackground )
            texto_numero_ciclos.SetBackgroundColour(colorTextBackground )
            texto_frequencia.SetBackgroundColour(colorTextBackground )
            texto_ciclo_atual.SetBackgroundColour(colorTextBackground )

            self.fase = wx.TextCtrl(self, -1, '1', size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.NGolpes = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTER)
            self.GolpeAtual = wx.TextCtrl(self, -1, wx.EmptyString, size = (50, 35), style = wx.TE_READONLY | wx.TE_CENTRE)
            self.freq = wx.ComboBox(self, -1, frequencias[0], choices = frequencias, size = (50, 35), style = wx.CB_READONLY)
            self.ensaioAuto = wx.CheckBox(self, -1, 'Ensaio automático', (20,0), (260,-1), style = wx.ALIGN_LEFT)
            
            self.fase.Disable()
            self.NGolpes.Disable()
            self.GolpeAtual.Disable()
            self.freq.Disable()
            
            self.fase.SetFont(Fonttext)
            self.NGolpes.SetFont(Fonttext)
            self.GolpeAtual.SetFont(Fonttext)
            self.freq.SetFont(Fonttext)
            
            self.fase.SetForegroundColour(colorTextCtrl)
            self.NGolpes.SetForegroundColour(colorTextCtrl)
            self.GolpeAtual.SetForegroundColour(colorTextCtrl)
            
            self.v3_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v4_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v5_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v6_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v7_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h4_sizer = wx.BoxSizer(wx.HORIZONTAL)

            self.v3_sizer.Add(texto_ciclo_atual, 1, wx.ALL | wx.CENTER)
            self.v3_sizer.Add(self.GolpeAtual, 2, wx.ALL | wx.CENTER, 5)

            self.v4_sizer.Add(texto_frequencia, 1, wx.ALL | wx.CENTER)
            self.v4_sizer.Add(self.freq, 2, wx.ALL | wx.CENTER, 5)

            self.v5_sizer.Add(texto_numero_ciclos, 1, wx.ALL | wx.CENTER)
            self.v5_sizer.Add(self.NGolpes, 2, wx.ALL | wx.CENTER, 5)

            self.v6_sizer.Add(texto_fase, 1, wx.ALL | wx.CENTER)
            self.v6_sizer.Add(self.fase, 2, wx.ALL | wx.CENTER, 5)

            self.h2_sizer.Add(self.v4_sizer, 3, wx.CENTER)
            self.h2_sizer.AddStretchSpacer(1)
            self.h2_sizer.Add(self.v3_sizer, 4, wx.CENTER)

            self.h3_sizer.Add(self.v6_sizer, 3, wx.CENTER)
            self.h3_sizer.AddStretchSpacer(1)
            self.h3_sizer.Add(self.v5_sizer, 4, wx.CENTER)

            self.v7_sizer.Add(self.h3_sizer, 3, wx.ALL | wx.CENTER)
            self.v7_sizer.AddStretchSpacer(1)
            self.v7_sizer.Add(self.h2_sizer, 3, wx.ALL | wx.CENTER)

            self.h4_sizer.Add(self.v7_sizer, 1, wx.CENTER)
            staticboxSizer6.Add(self.h4_sizer, 0, wx.ALL | wx.CENTER, 10)
            

            #--------------------------------------------------
            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v1_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v2_sizer = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h1_sizer = wx.BoxSizer(wx.HORIZONTAL)

            
            self.v_sizer.Add(self.condic, 1, wx.EXPAND | wx.ALL, 5)
            if self.ensaio[0]=='179':
                self.v_sizer.Add(self.dp, 1, wx.EXPAND | wx.ALL, 5)
                self.v_sizer.Add(self.gDP, 1, wx.EXPAND | wx.ALL, 5)
            elif self.ensaio[0]=='134' or '135':
                self.v_sizer.Add(self.mr, 1, wx.EXPAND | wx.ALL, 5)
                if self.ensaio[0]=='134':
                    self.v_sizer.Add(self.qTensoes, 1, wx.EXPAND | wx.ALL, 5)

            self.v1_sizer.Add(staticboxSizer3, 15, wx.EXPAND | wx.ALL)
            self.v1_sizer.AddStretchSpacer(1)
            self.v1_sizer.Add(staticboxSizer4, 20, wx.EXPAND | wx.ALL)

            self.v2_sizer.Add(staticboxSizer5, 15, wx.EXPAND | wx.ALL)
            self.v2_sizer.AddStretchSpacer(1)
            self.v2_sizer.Add(staticboxSizer6, 20, wx.EXPAND | wx.ALL)

            self.h1_sizer.Add(staticboxSizer1, 1, wx.EXPAND | wx.ALL, 3)
            
            self.h1_sizer.Add(self.v1_sizer, 1, wx.EXPAND | wx.ALL, 3)
            self.h1_sizer.Add(self.v2_sizer, 1, wx.EXPAND | wx.ALL, 3)

            self.h_sizer.Add(self.h1_sizer, 12, wx.EXPAND | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)
            self.h_sizer.AddStretchSpacer(4)

            self.sizer.Add(self.h_sizer, 0,  wx.EXPAND | wx.ALL, 10)
            self.SetSizer(self.sizer)

            self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.ensaioAuto)
            self._fase = 0  #condicao dos fases inicia com zero
            self.erro = False  #indica se há erros na execução
            self.Automatico = True  #inicia  com o ensaio Automatico sendo true
            self.ensaioAuto.SetValue(True)
            

    #--------------------------------------------------
        '''Função CheckBox'''
        def onCheck(self, event):
            print ('\nBottomPanel - onCheck')
            global Automatico
            if  self.ensaioAuto.GetValue() == False:
                self.Automatico = False
            else:
                self.Automatico = True

    #--------------------------------------------------
        '''Função responsável em realizar a CONEXÃO'''
        def LTESTE(self, event):
            print ('\nBottomPanel - LTESTE')
            global DISCREP,valorleitura0,valorleitura1
            DISCREP=1.05
            valorleitura0=0
            valorleitura1=0
            try: 
                teste=ConexaoThread.ConexaoThread(DISCREP) #roda thread de conexão
                status=teste.getStatus()
                if status == 'connectado':
                    menssagError = wx.MessageDialog(self, 'CONECTADO!', 'EDP', wx.OK|wx.ICON_AUTH_NEEDED)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    if self.ensaio[0]!='135':
                        con.modeConectDNIT134() #acessa o ensaio da 134 no arduino
                    else:
                        con.modeConectDNIT135() #acessa o ensaio da 135 no arduino
                    self.LTeste.Disable()
                    self.LZero.Enable()
                    self.threadLeituraDados=ThreadLeituraDados.LeituraDados(self,0,0)
                    self.threadLeituraDados.start()
                else:
                    menssagError = wx.MessageDialog(self, 'Não é possível manter uma conexão serial!', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
            except Exception as e:
                print("Exceção:", type(e).__name__)
                menssagError = wx.MessageDialog(self, 'ERRO AO EXECUTAR O CONECTAR', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()

    #--------------------------------------------------
        '''Função responsável pela leitura zero'''
        def LZERO(self, event):
            print ('\nBottomPanel - LZERO')
            # self.threadLeituraDados.stop()
            if self.ensaio[0]!='135':
                self.freq.Enable()
            self.condic.Enable()
            if self.ensaio[0]=='179':
                self.dp.Enable()
                self.gDP.Disable()
            elif self.ensaio[0] in ['134','181','135']:
                if self.ensaio[0]!='135':
                    self.qTensoes.Enable()
                self.mr.Enable()
            self.LTeste.Disable()
            valores = [0,0,0,0,0,0,0,0,0,0]
            self.threadLeituraDados.pause()
            if self.ensaio[0]!='135':
                while valores[1]==0 and valores[2]==0:
                    con.modeJ()
                    valores=con.ColetaI(valores,self.ensaio[0])
                self.leituraZerob1 = float(valores[1]) #salva os valores para subtrair no momento de atualizar os campos y1 e y2
                self.leituraZerob2 = float(valores[2])
                self.threadLeituraDados.updateValor(self.leituraZerob1,self.leituraZerob2)
                self.threadLeituraDados.pause()
                print (self.leituraZerob1)
                print (self.leituraZerob2)
            elif self.ensaio[0]=='135':
                while valores[1]==0:
                    con.modeJ()
                    valores=con.ColetaI(valores,self.ensaio[0])
                self.leituraZerob1 = float(valores[1])
                self.threadLeituraDados.updateValor(self.leituraZerob1,0)
                self.threadLeituraDados.pause()
                print (self.leituraZerob1)
                if self.resistencia==0.05:
                    menssagError = wx.MessageDialog(self, 'RT desconhecida, o software ira determinar os valores de pressão referentes ao ensaio', 'EDP', wx.OK|wx.ICON_EXCLAMATION)
                    aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                    menssagError.ShowModal()
                    menssagError.Destroy()
                    self.Bind(wx.EVT_BUTTON, self.RT, self.condic)
                    evt=wx.PyCommandEvent(wx.EVT_BUTTON.typeId,self.condic.GetId())
                    wx.PostEvent(self.condic,evt)
                    

            else:
                self.threadLeituraDados.pause()
                

    #--------------------------------------------------
        '''Função responsável em mostrar o quadro dinâmico de tensões'''
        def QT(self, event):
            print ('\nBottomPanel - QT')
            dlg = quadro().ShowModal()

    #--------------------------------------------------

        def GDP(self, event):
            print ('\nBottomPanel - GDP')
            xy = bancodedados.dados_GDP_179(self.Nome)
            self.X = xy[0]
            self.Y = xy[1]
            try:
                self.window.Close()
            except:
                pass

            self.window = wx.MiniFrame(self, title="", size=(600,400), style= wx.CLOSE_BOX | wx.CAPTION | wx.STAY_ON_TOP)
            fig = plt.figure(constrained_layout=True)  
            axes = fig.add_subplot(111) 
            axes.set_xlabel("GOLPE")
            axes.set_ylabel("D. P. (mm)")
            axes.plot(self.X, self.Y, 'r-')
            canvas = FigureCanvas(self.window, -1, fig)   
            canvas.draw()
            self.window.Show() 




        def RT(self,event):
            self.Fase = 'RT'
            self.LZero.Disable()
            self.freq.Disable()
            self.mr.Disable()
            self.condic.Disable()
            self.SigmaAlvo.SetLabelText("%.3f" % (self.resistencia))
            self.NGolpes.SetLabelText(str(self.glpRT))
            self.fase.SetLabelText(str(0))# fase 0:fase de condicionamento
            self.GolpeAtual.SetLabelText(str(0))
            self.TopPanel.cond135=0

            self.Raise()
            self.TopPanel.fim_inicio.Disable()
            self.threadLeituraDados.pause()
            dialog = wx.ProgressDialog("Aguarde", "Aguarde, calibrando pressões", maximum=100)
            time.sleep(.5)
            dialog.Update(33)
            press=SetarPressoes.SetarPressaoGolpe(self.resistencia,self.TopPanel.PressaoAtualGolpe,float(self.DiametroMM.GetValue()))
            self.TopPanel.PressaoAtualGolpe=self.resistencia
            time.sleep(0.5)
            dialog.Update(66)
            dialog.Update(100)
            dialog.Close()
            self.TopPanel._self.Raise()
            self.TopPanel._self.Maximize()
            gl = self.NGolpes.GetValue()
            freq = self.freq.GetValue()
            con.modeG()
            time.sleep(0.5)
            con.modeGOLPES135(int(gl), int(freq),self.TopPanel.cond135)
            self.TopPanel.pausa.Enable()
            self.TopPanel.fim_inicio.SetLabel('FIM')
            self.TopPanel.fim_inicio.Enable()
            self.TopPanel.Bind(wx.EVT_BUTTON, self.TopPanel.FIM, self.TopPanel.fim_inicio)
            self.threadLeituraDados.inicioEnsaio()
            self.threadLeituraDados.setEnsaio()
            self.threadLeituraDados.pause()
            self.TopPanel._self.Raise()
            self.condRT=True


    
    
    
    #--------------------------------------------------
        '''Função responsável em realizar o CONDICIONAMENTO'''
        
        
        def CONDIC(self, event):
            print ('\nBottomPanel - CONDIC')
            self.Main.Raise()
            self.Main.RequestUserAttention()
            self.Fase = 'CONDICIONAMENTO'
            self.erro = False

            
            if self.ensaio[0]=='134':
                if int(self.tipo)==1:
                    fase=3
                else:
                    self.tipo=0
                    fase=1
                self._fase+=1
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.condic.Disable()
                self.PCalvo.SetLabelText("%.3f" % (self.pressoesCONDICIONAMENTO[self._fase-1][0]))
                self.SigmaAlvo.SetLabelText("%.3f" % (self.pressoesCONDICIONAMENTO[self._fase-1][1]))
                self.NGolpes.SetLabelText(str(self.glpCOND))
                self.fase.SetLabelText(str(self._fase))# fase 0:fase de condicionamento
                self.GolpeAtual.SetLabelText(str(0))

                if self._fase==1:
                    info = "EDP 134/2018ME"
                    titulo = "Preparação da câmara triaxial."
                    message1 = "Verifique se está tudo certo!"
                    message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                    dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                    if dlg.ShowModal() == wx.ID_OK:
                        freq = self.freq.GetValue()
                        bancodedados.Update_freq(self.Nome, int(freq))
                        bancodedados.data_inicio_Update_idt(self.Nome)
                        if self.Automatico == True:
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                            wx.PostEvent(self.graph.fim_inicio, evt)
                        elif self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
                            
                            
                elif self._fase>1 and self._fase<=3:
                    if self.Automatico == True:
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)
                    elif self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
            
            elif self.ensaio[0]=='179':
                self.LZero.Disable()
                self.freq.Disable()
                self.dp.Disable()
                self.condic.Disable()
                self.PCalvo.SetLabelText("%.3f" % self.VETOR_COND[0][0])
                self.SigmaAlvo.SetLabelText("%.3f" % (self.VETOR_COND[0][1]))
                self.NGolpes.SetLabelText(str(self.glpCOND))
                self.fase.SetLabelText('1')
                self.GolpeAtual.SetLabelText(str(0))


                info = "EDP 134/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
                    freq = self.freq.GetValue()
                    bancodedados.Update_freq(self.Nome, int(freq))
                    bancodedados.data_inicio_Update_idt(self.Nome)
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()
                    if self.Automatico == True:
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)
                    elif self.Automatico == False:
                        self.graph.fim_inicio.SetLabel('INICIO')
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        self.graph.fim_inicio.Enable()
            
            
            
            elif self.ensaio[0]=='135':
                fase=3
                self.LZero.Disable()
                self.freq.Disable()
                self.mr.Disable()
                self.condic.Disable()
                if self.condRT:
                    self.SigmaAlvo.SetLabelText("%.3f" % (self.TopPanel.PressaoAtualGolpe))
                else:
                    self.SigmaAlvo.SetLabelText("%.3f" % (self.resistencia*float(self.ensaio[26])))
                self.NGolpes.SetLabelText(str(self.glpCOND))
                self.fase.SetLabelText(str(0))# fase 0:fase de condicionamento
                self.GolpeAtual.SetLabelText(str(0))
                self.TopPanel.cond135=0

        
                info = "EDP 135/2018ME"
                titulo = "Preparação da câmara triaxial."
                message1 = "Verifique se está tudo certo!"
                message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                if dlg.ShowModal() == wx.ID_OK:
                    freq = self.freq.GetValue()
                    bancodedados.Update_freq(self.Nome, int(freq))
                    bancodedados.data_inicio_Update_idt(self.Nome)
                    self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                    self.graph.fim_inicio.Enable()
                    if self.Automatico == True:
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)
                    elif self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
    
    
    #--------------------------------------------------
        '''Função responsável em realizar o MODULO RESILIENTE'''
        def MR(self, event):
            print ('\nBottomPanel - MR')
            self.Main.Raise()
            self.Main.RequestUserAttention()
            self.erro = False
            

            if self.ensaio[0]=='135':
            
                if self._fase ==0:
                    self._fase=1
                    

                if self._fase <= 3:
                    print ('\nFASE.MR='+str(self._fase)+'\n')
                    self.LZero.Disable()
                    self.freq.Disable()
                    self.mr.Disable()
                    self.condic.Disable()
                    self.SigmaAlvo.Clear()
                    self.fase.Clear()
                    self.NGolpes.Clear()
                    self.GolpeAtual.Clear()
                    self.SigmaAlvo.SetLabelText("%.3f" % (self.TopPanel.PressaoAtualGolpe*self.graph.PRESSOES[self._fase-1]))
                    self.NGolpes.SetLabelText(str(15))
                    self.fase.SetLabelText(str(self._fase))
                    self.GolpeAtual.SetLabelText(str(0))
                    self.TopPanel.cond135=1

                if self.Fase == '' or self.Fase=='RT':
                    info = "EDP 134/2018ME"
                    titulo = "Preparação da câmara triaxial."
                    message1 = "Verifique se está tudo certo!"
                    message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                    dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                    freq = self.freq.GetValue()
                    bancodedados.Update_freq(self.Nome, int(freq))
                    bancodedados.data_inicio_Update_idt(self.Nome)
                    if self.Fase=='':
                        self.onlyMR=True
                    # SetarPressoes.SetarPressaoGolpe(self.TopPanel.PressaoAtualGolpe,0,float(self.DiametroMM.GetValue()))
                    if dlg.ShowModal() == wx.ID_OK:
                        self.Fase = 'MR'
                        if self._fase == 0:
                            self._fase+=1
                            

                        if self._fase >= 0 and self._fase <= 3 and self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
                            self.graph.avanca.Enable()

                        if self._fase >= 0 and self._fase <= 3 and self.Automatico == True:
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                            wx.PostEvent(self.graph.fim_inicio, evt)

                else:
                    self.Fase = 'MR'
                    if self._fase >= 0 and self._fase <= 3 and self.Automatico == False:
                        self.graph.fim_inicio.SetLabel('INICIO')
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        self.graph.fim_inicio.Enable()

                    elif self._fase >= 0 and self._fase <= 3 and self.Automatico == True:
                        self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                        wx.PostEvent(self.graph.fim_inicio, evt)

                    elif self._fase > 3 and self.erro == False:
                        self.mr.Disable()
                        self.threadLeituraDados.pause()
                        self.threadLeituraDados.stop()
                        self._fase = 0
                        SetarPressoes.ZerarPressaoGolpe(self.TopPanel.PressaoAtualGolpe)
                        bancodedados.data_final_Update_idt(self.Nome)
                        dlg3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                        if dlg3.ShowModal() == wx.ID_OK:
                        # dlg3.Show()
                            time.sleep(3)
                            time.sleep(.3)
                            con.modeB()
                            time.sleep(.3)
                            con.modeD()
                            time.sleep(0.3)
                            self.Main.Destroy()
            
            elif self.ensaio[0]=='134':
                if self.ensaio[3]=='1':
                    fase=18
                else:
                    fase=12
                if self._fase <= fase:
                    print ('\nFASE.MR='+str(self._fase)+'\n')
                    

                    if self.Fase == '':
                        info = "EDP 134/2018ME"
                        titulo = "Preparação da câmara triaxial."
                        message1 = "Verifique se está tudo certo!"
                        message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                        dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                        if dlg.ShowModal() == wx.ID_OK:
                            self.Fase = 'MR'
                            self._fase=1
                            self.LZero.Disable()
                            self.freq.Disable()
                            self.mr.Disable()
                            self.condic.Disable()
                            self.PCalvo.SetLabelText("%.3f" % (self.pressoesMR[self._fase-1][0]))
                            self.SigmaAlvo.SetLabelText("%.3f" % (self.pressoesMR[self._fase-1][1]))
                            self.NGolpes.SetLabelText(str(self.glpMR))
                            self.fase.SetLabelText(str(self._fase))
                            self.GolpeAtual.SetLabelText(str(0))
                            freq = self.freq.GetValue()
                            bancodedados.Update_freq(self.Nome, int(freq))
                            bancodedados.data_inicio_Update_idt(self.Nome) 
                                
                            if self._fase >= 0 and self._fase < fase and self.Automatico == True:
                                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                                wx.PostEvent(self.graph.fim_inicio, evt)
                            elif self._fase >= 0 and self._fase < fase and self.Automatico == False:
                                self.graph.fim_inicio.SetLabel('INICIO')
                                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                                self.graph.fim_inicio.Enable() 
                    
                    
                
                    elif self.Fase=='MR' or self.Fase=='CONDICIONAMENTO':
                        self.Fase='MR'
                        self.LZero.Disable()
                        self.freq.Disable()
                        self.mr.Disable()
                        self.condic.Disable()
                        self.PCalvo.SetLabelText("%.3f" % (self.pressoesMR[self._fase-1][0]))
                        self.SigmaAlvo.SetLabelText("%.3f" % (self.pressoesMR[self._fase-1][1]))
                        self.NGolpes.SetLabelText(str(self.glpMR))
                        self.fase.SetLabelText(str(self._fase))
                        self.GolpeAtual.SetLabelText(str(0))
                       
                        if self._fase >= 0 and self._fase <= fase and self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
                            self.graph.avanca.Enable()

                        elif self._fase >= 0 and self._fase <= fase and self.Automatico == True:
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                            wx.PostEvent(self.graph.fim_inicio, evt)

                elif self._fase > fase and self.erro == False:
                    self.mr.Disable()
                    self.threadLeituraDados.pause()
                    self.threadLeituraDados.stop()
                    time.sleep(3)
                    # print self.pressoesMR[self._fase-1][1]
                    # print self.TopPanel.PressaoAtualGolpe
                    SetarPressoes.ZerarPressaoGolpe(self.TopPanel.PressaoAtualGolpe)
                    time.sleep(1)
                    # print self.pressoesMR[self._fase-1][0]
                    print (self.TopPanel.PressaoAtualCamara)
                    SetarPressoes.ZerarPressaoCamara(self.TopPanel.PressaoAtualCamara)
                    bancodedados.data_final_Update_idt(self.Nome)
                    dlg3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                    dlg3.ShowModal()
                    time.sleep(.3)
                    con.modeB()
                    time.sleep(.3)
                    con.modeD()
                    time.sleep(0.3)
                    self.Main.Destroy()
            
            elif self.ensaio[0]=='181':
                faseTotal=5
                if self._fase <= faseTotal and self.erro == False:
                    if self.Fase == '':
                        info = "EDP 181/2018ME"
                        titulo = "Preparação da câmara triaxial."
                        message1 = "Verifique se está tudo certo!"
                        message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                        dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                        if dlg.ShowModal() == wx.ID_OK:
                            self.Fase = 'MR'
                            self._fase=1
                            self.LZero.Disable()
                            self.freq.Disable()
                            self.mr.Disable()
                            self.SigmaAlvo.SetLabelText("%.3f" % (self.pressoes[self._fase-1]))
                            self.NGolpes.SetLabelText(str(self.glpMR))
                            self.fase.SetLabelText(str(self._fase))
                            self.GolpeAtual.SetLabelText(str(0))
                            freq = self.freq.GetValue()
                            bancodedados.Update_freq(self.Nome, int(freq))
                            bancodedados.data_inicio_Update_idt(self.Nome) 
                                
                            if self._fase >= 0 and self._fase <= faseTotal and self.Automatico == True:
                                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                                evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                                wx.PostEvent(self.graph.fim_inicio, evt)
                            elif self._fase >= 0 and self._fase < faseTotal and self.Automatico == False:
                                self.graph.fim_inicio.SetLabel('INICIO')
                                self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                                self.graph.fim_inicio.Enable()
                                self.graph.avanca.Enable()
                    else:
                        self.LZero.Disable()
                        self.freq.Disable()
                        self.mr.Disable()
                        self.SigmaAlvo.SetLabelText("%.3f" % (self.pressoes[self._fase-1]))
                        self.NGolpes.SetLabelText(str(self.glpMR))
                        self.fase.SetLabelText(str(self._fase))
                        self.GolpeAtual.SetLabelText(str(0))
                        freq = self.freq.GetValue()
                        bancodedados.Update_freq(self.Nome, int(freq))
                        bancodedados.data_inicio_Update_idt(self.Nome) 
                        if self._fase >= 0 and self._fase <= faseTotal and self.Automatico == True:
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                            wx.PostEvent(self.graph.fim_inicio, evt)
                        elif self._fase >= 0 and self._fase < faseTotal and self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
                            self.graph.avanca.Enable()
                else:
                    self.mr.Disable()
                    self._fase = 0
                    self.threadLeituraDados.pause()
                    self.threadLeituraDados.stop()
                    time.sleep(3)
                    SetarPressoes.ZerarPressaoGolpe(self.pressoes[self._fase-1])
                    bancodedados.data_final_Update_idt(self.Nome)
                    dlg3 = dialogoDinamico(3, "EDP DNIT181/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                    if dlg3.ShowModal() == wx.ID_OK:
                        con.modeB()
                        time.sleep(0.3)
                        con.modeD()
                        time.sleep(0.3)
                        self.Main.Destroy()
                        
            elif self.ensaio[0]=='179':
                self.LZero.Disable()
                self.freq.Disable()
                self.dp.Disable()
                self.condic.Disable()
                self.PCalvo.SetLabelText("%.3f" % self.VETOR_DP[0][0])
                self.SigmaAlvo.SetLabelText("%.3f" % (self.VETOR_DP[0][1]))
                self.NGolpes.SetLabelText(str(self.glpDP))
                self.fase.SetLabelText('1')
                self.GolpeAtual.SetLabelText(str(0))

                if self.Fase == '':
                    info = "EDP 179/2018ME"
                    titulo = "Preparação da câmara triaxial."
                    message1 = "Verifique se está tudo certo!"
                    message2 = "Se as válvulas de escape estão fechadas, se as válvulas reguladoras de pressão estão devidamentes conectadas, se a passagem de ar comprimido para o sistema está liberado e se a câmara triaxial está totalmente fechada e com o fluido de atrito para o suporte vertical."
                    dlg = dialogoDinamico(2, info, titulo, message1, message2, "", None)
                    if dlg.ShowModal() == wx.ID_OK:
                        self.Fase = 'DP'
                        freq = self.freq.GetValue()
                        bancodedados.Update_freq(self.Nome, int(freq))
                        bancodedados.data_inicio_Update_idt(self.Nome)
                        if self.Automatico == True:
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                            wx.PostEvent(self.graph.fim_inicio, evt)
                        
                        elif self.Automatico == False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
                
                else:
                    self.Fase = 'DP'
                    if self._fase <= 1:
                        if self.Automatico==True:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, self.graph.fim_inicio.GetId())
                            wx.PostEvent(self.graph.fim_inicio, evt)
                        elif self.Automatico==False:
                            self.graph.fim_inicio.SetLabel('INICIO')
                            self.graph.Bind(wx.EVT_BUTTON, self.graph.INICIO, self.graph.fim_inicio)
                            self.graph.fim_inicio.Enable()
                    else:
                        self.dp.Disable()
                        self.threadLeituraDados.pause()
                        self.threadLeituraDados.stop()
                        time.sleep(3)
                        SetarPressoes.ZerarPressaoGolpe(self.VETOR_DP[0][1])
                        time.sleep(1)
                        SetarPressoes.ZerarPressaoCamara(self.VETOR_DP[0][0])
                        bancodedados.data_final_Update_idt(self.Nome)
                        dlg3 = dialogoDinamico(3, "EDP DNIT134/2018ME", "O ENSAIO FOI FINALIZADO!", "Os relatório de extração são gerados na tela inicial.", "FIM!", "", None)
                        if dlg3.ShowModal() == wx.ID_OK:
                            con.modeB()
                            time.sleep(0.3)
                            con.modeD()
                            time.sleep(0.3)
                            self.Main.Destroy()
                        



    #--------------------------------------------------
        '''Função responsável pela plotagem'''
        def TimeInterval(self):
            print ('\nBottomPanel - TimeInterval')
            self.mult += 1
            self.graph.draw()
        
    #-----------------------------------------------------
    # Funções responsáveis por dialogo de carregamento
        def dialogoCarregamento(self, event):
            self.dialog=wx.ProgressDialog("Aguarde", "Configurando pressões", 100)
            self.num = 0
        
        def updateDialogoCarregamento(self, event):
            self.num += 33
            self.dialog.Update(self.num)
        
        def destroyDialogoCarregamento(self, event):
            self.dialog.Destroy()