# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
from ensaio import Ensaio
# import bancodedados
import bancodedadosnovo
import bdPreferences

'''Tela Novo Ensaio'''
class TelaNovoEnsaio(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, ensaio, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'Software Marshall - Novo Ensaio', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            self.ensaio = ensaio
            self.panel = wx.Panel(self)
            self.SetSize((550,500))
            self.Centre()
            self.Show()

            if(ensaio[0:4] == 'DNIT'):
                ensaio = ensaio[0:18]
            else:
                ensaio = ensaio[0:15]

            if(ensaio[8:-1] == "043/95"):
                self.temperatura_norma = "60"
            elif(ensaio[8:-1] == "107/94"):
                self.temperatura_norma = "40"
            else:
                self.temperatura_norma = "25"

            '''Conexão com o banco, lendo capsula'''
            # self.capCadastradas = bancodedados.ler_cap()
            self.FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            self.title = wx.StaticText(self.panel, -1, 'Dados do Ensaio', (20,20), (530,-1), wx.ALIGN_CENTER)
            self.title.SetFont(self.FontTitle)
            self.textIdentificador = wx.StaticText(self.panel, -1, 'Identificador',(20,62.5), (80,-1), wx.ALIGN_LEFT)
            self.identificador = wx.TextCtrl(self.panel, -1, ensaio, (100,60),(150,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textRodovia = wx.StaticText(self.panel, -1, 'Rodovia',(20,92.5), (80,-1), wx.ALIGN_LEFT)
            self.rodovia = wx.TextCtrl(self.panel, -1, '', (100,90),(150,-1), wx.TE_RIGHT)
            self.textTrecho = wx.StaticText(self.panel, -1, 'Trecho',(20,122.5), (80,-1), wx.ALIGN_LEFT)
            self.trecho = wx.TextCtrl(self.panel, -1, '', (100,120),(150,-1), wx.TE_RIGHT)
            self.textOperador = wx.StaticText(self.panel, -1, 'Operador',(20,152.5), (80,-1), wx.ALIGN_LEFT)
            self.operador = wx.TextCtrl(self.panel, -1, '', (100,150),(150,-1), wx.TE_RIGHT)
            self.textCPn = wx.StaticText(self.panel, -1, 'C.P.n°',(300,62.5), (80,-1), wx.ALIGN_LEFT)
            self.CPn = wx.TextCtrl(self.panel, -1, '', (380,60),(150,-1), wx.TE_RIGHT)
            self.textOrigem = wx.StaticText(self.panel, -1, 'Origem',(300,92.5), (80,-1), wx.ALIGN_LEFT)
            self.origem = wx.TextCtrl(self.panel, -1, '', (380,90),(150,-1), wx.TE_RIGHT)
            self.textEstKm = wx.StaticText(self.panel, -1, 'Est/km',(300,122.5), (80,-1), wx.ALIGN_LEFT)
            self.estKm = wx.TextCtrl(self.panel, -1, '', (380,120),(150,-1), wx.TE_RIGHT)
            self.textInteresse = wx.StaticText(self.panel, -1, 'Interesse',(300,152.5), (80,-1), wx.ALIGN_LEFT)
            self.interesse = wx.TextCtrl(self.panel, -1, '', (380,150),(150,-1), wx.TE_RIGHT)
            self.textPesoSub = wx.StaticText(self.panel, -1, 'Peso sub.(g)*',(20,202.5), (80,-1), wx.ALIGN_LEFT)
            self.pesoSub = wx.TextCtrl(self.panel, -1, '', (100,200),(60,-1), wx.TE_RIGHT)
            self.textPesoAr = wx.StaticText(self.panel, -1, 'Peso ao ar(g)*',(175,202.5), (80,-1), wx.ALIGN_LEFT)
            self.pesoAr = wx.TextCtrl(self.panel, -1, '', (260,200),(60,-1), wx.TE_RIGHT)
            self.textTemp = wx.StaticText(self.panel, -1, 'Temp.(°C)*',(380,202.5), (80,-1), wx.ALIGN_LEFT)
            self.temp = wx.TextCtrl(self.panel, -1, self.temperatura_norma, (460,200),(60,-1), wx.TE_RIGHT)
            self.textAsfalto = wx.StaticText(self.panel, -1, 'Asfalto (%)*',(20,232.5), (80,-1), wx.ALIGN_LEFT)
            self.asfalto = wx.TextCtrl(self.panel, -1, '', (100,230),(60,-1), wx.TE_RIGHT)
            self.textDMT = wx.StaticText(self.panel, -1, 'DMT*',(175,232.5), (80,-1), wx.ALIGN_LEFT)
            self.DMT = wx.TextCtrl(self.panel, -1, '', (260,230),(60,-1), wx.TE_RIGHT)
            self.textVv = wx.StaticText(self.panel, -1, 'Vv (%)*',(380,232.5), (80,-1), wx.ALIGN_LEFT)
            self.Vv= wx.TextCtrl(self.panel, -1, '', (460,230),(60,-1), wx.TE_RIGHT)
            self.textCteAnel = wx.StaticText(self.panel, -1, 'Cte Anel*',(20,262.5), (80,-1), wx.ALIGN_LEFT)
            self.const_anel=bdPreferences.getCteAnel()
            self.CteAnel = wx.TextCtrl(self.panel, -1, str(self.const_anel[0]), (100,260),(60,-1), wx.TE_RIGHT) #1490,5 1938.4
            # self.textTemp = wx.StaticText(self.panel, -1, 'Temp.(°C)*',(380,232.5), (80,-1), wx.ALIGN_LEFT)
            # self.temp = wx.TextCtrl(self.panel, -1, '', (460,230),(60,-1), wx.TE_RIGHT)
            self.textDiametro = wx.StaticText(self.panel, -1, 'Diâmetro C.P.(mm)*',(20,302.5), (120,-1), wx.ALIGN_LEFT)
            self.diametro1 = wx.TextCtrl(self.panel, -1, '', (140,300),(60,-1), wx.TE_RIGHT)
            self.diametro2 = wx.TextCtrl(self.panel, -1, '', (210,300),(60,-1), wx.TE_RIGHT)
            self.diametro3 = wx.TextCtrl(self.panel, -1, '', (280,300),(60,-1), wx.TE_RIGHT)
            self.diametro4 = wx.TextCtrl(self.panel, -1, '', (350,300),(60,-1), wx.TE_RIGHT)
            self.diametro5 = wx.TextCtrl(self.panel, -1, '', (420,300),(60,-1), wx.TE_RIGHT)
            self.repetir_diametro = wx.Button(self.panel, -1, 'Repetir', (480, 300), (60,-1), wx.ALIGN_LEFT)
            self.textAltura = wx.StaticText(self.panel, -1, 'Altura C.P.(mm)*',(20,332.5), (120,-1), wx.ALIGN_LEFT)
            self.altura1 = wx.TextCtrl(self.panel, -1, '', (140,330),(60,-1), wx.TE_RIGHT)
            self.altura2 = wx.TextCtrl(self.panel, -1, '', (210,330),(60,-1), wx.TE_RIGHT)
            self.altura3 = wx.TextCtrl(self.panel, -1, '', (280,330),(60,-1), wx.TE_RIGHT)
            self.altura4 = wx.TextCtrl(self.panel, -1, '', (350,330),(60,-1), wx.TE_RIGHT)
            self.altura5 = wx.TextCtrl(self.panel, -1, '', (420,330),(60,-1), wx.TE_RIGHT)
            self.repetir_altura = wx.Button(self.panel, -1, 'Repetir', (480, 330), (60,-1), wx.ALIGN_LEFT)
            self.textObs = wx.StaticText(self.panel, -1, 'Observações',(20,362.5), (80,-1), wx.ALIGN_LEFT)
            self.obs = wx.TextCtrl(self.panel, -1, '', (140,360),(340,-1), wx.TE_RIGHT)
            self.continuar = wx.Button(self.panel, -1, 'Continuar', (20, 430), (510,-1), wx.ALIGN_LEFT)
            self.aviso = wx.StaticText(self.panel, -1, '*Campos de preenchimento obrigatório',(340,410), (200,-1), wx.ALIGN_LEFT)
            self.aviso.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))

            self.Bind(wx.EVT_BUTTON, self.Prosseguir, self.continuar)
            self.Bind(wx.EVT_BUTTON, self.Repetir_Diametro, self.repetir_diametro)
            self.Bind(wx.EVT_BUTTON, self.repetir_Altura, self.repetir_altura)
    #--------------------------------------------------
        def Repetir_Diametro(self, event):
            self.media_diametro = self.diametro1.GetValue()
            self.diametro2.Clear()
            self.diametro2.AppendText(self.media_diametro)
            self.diametro3.Clear()
            self.diametro3.AppendText(self.media_diametro)
            self.diametro4.Clear()
            self.diametro4.AppendText(self.media_diametro)
            self.diametro5.Clear()
            self.diametro5.AppendText(self.media_diametro)
    #--------------------------------------------------
        def repetir_Altura(self, event):
            self.media_altura = self.altura1.GetValue()
            self.altura2.Clear()
            self.altura2.AppendText(self.media_altura)
            self.altura3.Clear()
            self.altura3.AppendText(self.media_altura)
            self.altura4.Clear()
            self.altura4.AppendText(self.media_altura)
            self.altura5.Clear()
            self.altura5.AppendText(self.media_altura)
    #--------------------------------------------------
        def Prosseguir(self, event):
            norma = self.identificador.GetValue()
            a = self.rodovia.GetValue()
            b = self.trecho.GetValue()
            c = self.operador.GetValue()
            d = self.CPn.GetValue()
            e = self.origem.GetValue()
            f = self.estKm.GetValue()
            g = self.interesse.GetValue()
            h = self.pesoSub.GetValue()
            h = format(h).replace(',','.')
            i = self.pesoAr.GetValue()
            i = format(i).replace(',','.')
            j = self.temp.GetValue()
            j = format(j).replace(',','.')
            k0 = self.asfalto.GetValue()
            k0 = format(k0).replace(',','.')
            k00 = self.DMT.GetValue()
            k00 = format(k00).replace(',','.')
            k000 = self.Vv.GetValue()
            k000 = format(k000).replace(',','.')
            k1 = self.diametro1.GetValue()
            k1 = format(k1).replace(',','.')
            k2 = self.diametro2.GetValue()
            k2 = format(k2).replace(',','.')
            k3 = self.diametro3.GetValue()
            k3 = format(k3).replace(',','.')
            k4 = self.diametro4.GetValue()
            k4 = format(k4).replace(',','.')
            k5 = self.diametro5.GetValue()
            k5 = format(k5).replace(',','.')
            l1 = self.altura1.GetValue()
            l1 = format(l1).replace(',','.')
            l2 = self.altura2.GetValue()
            l2 = format(l2).replace(',','.')
            l3 = self.altura3.GetValue()
            l3 = format(l3).replace(',','.')
            l4 = self.altura4.GetValue()
            l4 = format(l4).replace(',','.')
            l5 = self.altura5.GetValue()
            l5 = format(l5).replace(',','.')
            n = self.CteAnel.GetValue()
            n = format(n).replace(',','.')
            m = self.obs.GetValue()

    #--------------------------------------------------
            try:
                h = float(h)
                i = float(i)
                j = float(j)
                k0 = float(k0)
                k00 = float(k00)
                k000 = float(k000)
                k1 = float(k1)
                k2 = float(k2)
                k3 = float(k3)
                k4 = float(k4)
                k5 = float(k5)
                l1 = float(l1)
                l2 = float(l2)
                l3 = float(l3)
                l4 = float(l4)
                l5 = float(l5)
                n = float(n)*self.const_anel[1]
                k_medio = (k1+k2+k3+k4+k5)/5
                l_medio = (l1+l2+l3+l4+l5)/5
                id = bancodedadosnovo.get_id() + 1

                bancodedadosnovo.write_table_dadosEnsaio(id, norma, a, b, c, d, e, f, g, m, n)
                bancodedadosnovo.write_table_dadosAmostra(id, h, i, j, k_medio, l_medio, k0, k00, k000)
                con = Ensaio(1, 1, True)
                resultado = con.ShowModal()
                self.Close(True)

            except ValueError:
                menssagError = wx.MessageDialog(self, 'Um campo ou mais apresenta incoerência', 'Software de Marshall', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                h = -1
