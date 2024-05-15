# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
# import bancodedados
import bancodedadosnovo
import matplotlib
import matplotlib.pyplot as plt
import calculo

'''Tela Novo Ensaio'''
class EditarEnsaio(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, ensaio, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'Software Marshall - Editar Ensaio', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            global id_ensaio
            id_ensaio = ensaio
            self.panel = wx.Panel(self)
            self.SetSize((550,500))
            self.Centre()
            self.Show()

            dados_ensaio = bancodedadosnovo.get_dadosEnsaio(id_ensaio)
            self.rodovia = dados_ensaio[0][2]
            self.trecho = dados_ensaio[0][3]
            self.operador = dados_ensaio[0][4]
            self.cp = dados_ensaio[0][5]
            self.origem = dados_ensaio[0][6]
            self.est = dados_ensaio[0][7]
            self.interesse = dados_ensaio[0][8]
            self.obs = dados_ensaio[0][9]
            self.cteAnel = dados_ensaio[0][11]/0.00062676

            '''Conexão com o banco, lendo capsula'''
            # self.capCadastradas = bancodedados.ler_cap()
            self.FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            self.title = wx.StaticText(self.panel, -1, 'Dados do Ensaio', (20,20), (530,-1), wx.ALIGN_CENTER)
            self.title.SetFont(self.FontTitle)
            self.textIdentificador = wx.StaticText(self.panel, -1, 'Identificador',(20,62.5), (80,-1), wx.ALIGN_LEFT)
            self.identificador = wx.TextCtrl(self.panel, -1, 'Editar', (100,60),(150,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textRodovia = wx.StaticText(self.panel, -1, 'Rodovia',(20,92.5), (80,-1), wx.ALIGN_LEFT)
            self.rodovia = wx.TextCtrl(self.panel, -1, self.rodovia, (100,90),(150,-1), wx.TE_RIGHT)
            self.textTrecho = wx.StaticText(self.panel, -1, 'Trecho',(20,122.5), (80,-1), wx.ALIGN_LEFT)
            self.trecho = wx.TextCtrl(self.panel, -1, self.trecho, (100,120),(150,-1), wx.TE_RIGHT)
            self.textOperador = wx.StaticText(self.panel, -1, 'Operador',(20,152.5), (80,-1), wx.ALIGN_LEFT)
            self.operador = wx.TextCtrl(self.panel, -1, self.operador, (100,150),(150,-1), wx.TE_RIGHT)
            self.textCPn = wx.StaticText(self.panel, -1, 'C.P.n°',(300,62.5), (80,-1), wx.ALIGN_LEFT)
            self.CPn = wx.TextCtrl(self.panel, -1, self.cp, (380,60),(150,-1), wx.TE_RIGHT)
            self.textOrigem = wx.StaticText(self.panel, -1, 'Origem',(300,92.5), (80,-1), wx.ALIGN_LEFT)
            self.origem = wx.TextCtrl(self.panel, -1, self.origem, (380,90),(150,-1), wx.TE_RIGHT)
            self.textEstKm = wx.StaticText(self.panel, -1, 'Est/km',(300,122.5), (80,-1), wx.ALIGN_LEFT)
            self.estKm = wx.TextCtrl(self.panel, -1, self.est, (380,120),(150,-1), wx.TE_RIGHT)
            self.textInteresse = wx.StaticText(self.panel, -1, 'Interesse',(300,152.5), (80,-1), wx.ALIGN_LEFT)
            self.interesse = wx.TextCtrl(self.panel, -1, self.interesse, (380,150),(150,-1), wx.TE_RIGHT)
            self.textPesoSub = wx.StaticText(self.panel, -1, 'Peso sub.(kg)*',(20,202.5), (80,-1), wx.ALIGN_LEFT)
            self.pesoSub = wx.TextCtrl(self.panel, -1, '', (100,200),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textPesoAr = wx.StaticText(self.panel, -1, 'Peso ao ar(kg)*',(175,202.5), (80,-1), wx.ALIGN_LEFT)
            self.pesoAr = wx.TextCtrl(self.panel, -1, '', (260,200),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textTemp = wx.StaticText(self.panel, -1, 'Temp.(°C)*',(380,202.5), (80,-1), wx.ALIGN_LEFT)
            self.temp = wx.TextCtrl(self.panel, -1, '', (460,200),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textAsfalto = wx.StaticText(self.panel, -1, 'Asfalto (%)*',(20,232.5), (80,-1), wx.ALIGN_LEFT)
            self.asfalto = wx.TextCtrl(self.panel, -1, '', (100,230),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textDMT = wx.StaticText(self.panel, -1, 'DMT*',(175,232.5), (80,-1), wx.ALIGN_LEFT)
            self.DMT = wx.TextCtrl(self.panel, -1, '', (260,230),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textVv = wx.StaticText(self.panel, -1, 'Vv (%)*',(380,232.5), (80,-1), wx.ALIGN_LEFT)
            self.Vv= wx.TextCtrl(self.panel, -1, '', (460,230),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textCteAnel = wx.StaticText(self.panel, -1, 'Cte Anel*',(20,262.5), (80,-1), wx.ALIGN_LEFT)
            self.CteAnel = wx.TextCtrl(self.panel, -1, str(self.cteAnel), (100,260),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            # self.textTemp = wx.StaticText(self.panel, -1, 'Temp.(°C)*',(380,232.5), (80,-1), wx.ALIGN_LEFT)
            # self.temp = wx.TextCtrl(self.panel, -1, '', (460,230),(60,-1), wx.TE_RIGHT)
            self.textDiametro = wx.StaticText(self.panel, -1, 'Diâmetro C.P.(mm)*',(20,302.5), (120,-1), wx.ALIGN_LEFT)
            self.diametro1 = wx.TextCtrl(self.panel, -1, '', (140,300),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.diametro2 = wx.TextCtrl(self.panel, -1, '', (210,300),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.diametro3 = wx.TextCtrl(self.panel, -1, '', (280,300),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.diametro4 = wx.TextCtrl(self.panel, -1, '', (350,300),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.diametro5 = wx.TextCtrl(self.panel, -1, '', (420,300),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textAltura = wx.StaticText(self.panel, -1, 'Altura C.P.(mm)*',(20,332.5), (120,-1), wx.ALIGN_LEFT)
            self.altura1 = wx.TextCtrl(self.panel, -1, '', (140,330),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.altura2 = wx.TextCtrl(self.panel, -1, '', (210,330),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.altura3 = wx.TextCtrl(self.panel, -1, '', (280,330),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.altura4 = wx.TextCtrl(self.panel, -1, '', (350,330),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.altura5 = wx.TextCtrl(self.panel, -1, '', (420,330),(60,-1), wx.TE_READONLY | wx.TE_RIGHT)
            self.textObs = wx.StaticText(self.panel, -1, 'Observações',(20,362.5), (80,-1), wx.ALIGN_LEFT)
            self.obs = wx.TextCtrl(self.panel, -1, self.obs, (140,360),(340,-1), wx.TE_RIGHT)
            self.grafico = wx.Button(self.panel, -1, 'Gráfico', (20, 400), (250,-1), wx.ALIGN_LEFT)
            self.continuar = wx.Button(self.panel, -1, 'Atualizar', (20, 430), (510,-1), wx.ALIGN_LEFT)
            self.aviso = wx.StaticText(self.panel, -1, '*Campos de preenchimento obrigatório',(340,410), (200,-1), wx.ALIGN_LEFT)
            self.aviso.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))

            self.Bind(wx.EVT_BUTTON, self.Prosseguir, self.continuar)
            self.Bind(wx.EVT_BUTTON, self.coletas, self.grafico)
    #--------------------------------------------------
        def Prosseguir(self, event):
            a = self.rodovia.GetValue()
            b = self.trecho.GetValue()
            oper = self.operador.GetValue()
            d = self.CPn.GetValue()
            e = self.origem.GetValue()
            f = self.estKm.GetValue()
            g = self.interesse.GetValue()
            h = self.obs.GetValue()
            bancodedadosnovo.update_dadosEnsaio(id_ensaio,a,b,d,e,f,g,h)
            bancodedadosnovo.teste(id_ensaio, oper)
            self.Close(True)

        def coletas(self, event):
            dados_coleta = bancodedadosnovo.get_leituraEnsaio(id_ensaio)
            dados_ensaio = bancodedadosnovo.get_dadosEnsaio(id_ensaio)[0][1]
            deformacao = []
            estabilidade = []
            for i in range((len(dados_coleta))):
                deformacao.append(dados_coleta[i][1])
                estabilidade.append(dados_coleta[i][2]) #REMOVER O 0.9197 APÓS A DEFESA DO TCC - retirado 09/03/2023
            # estabilidade_mm = calculo.filtro_mm(estabilidade)
            # deformacao_mm = calculo.offset(deformacao, estabilidade_mm)
            # plt.clf()
            print(deformacao,estabilidade)
            plt.plot(deformacao, estabilidade)
            # plt.ylim(-0.05*min(estabilidade), 1.05*max(estabilidade))
            # plt.xlim(min(deformacao), max(deformacao))
            if(dados_ensaio[0:4] == 'DNER'):
                plt.title('Ensaio de Compressao')
            else:
                plt.title('Ensaio de Tracao')
            plt.ylabel('Forca (kgf)')
            plt.xlabel('Deformacao (mm)')
            plt.grid(True)
            plt.show()
