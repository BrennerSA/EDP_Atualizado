# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import time
import wx.adv
import matplotlib
import serial
import bancodedadosnovo
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
import logging
from front.dialogoDinamico import dialogoDinamico
from scipy.signal import savgol_filter

'''plt.style.use('ggplot')'''
vetorLeitura_lvdt1 = []
vetorLeitura_lvdt2 = []
leitura_velocidade = "aguardando"
leitura_lvdt1 = "aguardando"
leitura_lvdt2 = "aguardando"
estado_do_ensaio = 0

conexao = 0

'''Painel Superior'''

class TopPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent =  parent)
            FontTitle = wx.Font(-1, wx.SWISS, wx.NORMAL, wx.BOLD)

            self.sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer_grafico=wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)

            self.figure = plt.figure(figsize=(14, 2.3))
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvas(self, -1, self.figure)
            self.axes.set_xlabel("Deslocamento (mm)")
            self.axes.set_ylabel("Forca (kgf)")

            rect = self.figure.patch
            rect.set_facecolor('#D7D7D7')

            rect1 = self.axes.patch
            rect1.set_facecolor('#A0BA8C')

            self.figure1 = plt.figure(figsize=(14,2.3))
            self.axes1 = self.figure1.add_subplot(111)
            self.canvas1 = FigureCanvas(self, -1, self.figure1)
            self.axes1.set_xlabel("Tempo (S)")
            self.axes1.set_ylabel("Forca (kgf)")

            rect = self.figure1.patch
            rect.set_facecolor('#D7D7D7')

            rect1 = self.axes1.patch
            rect1.set_facecolor('#A0BA8C')


            self.figure2 = plt.figure(figsize=(14,2.3))
            self.axes2 = self.figure2.add_subplot(111)
            self.canvas2 = FigureCanvas(self, -1, self.figure2)
            self.axes2.set_xlabel("Tempo (S)")
            self.axes2.set_ylabel("Deslocamento (mm)")

            rect = self.figure2.patch
            rect.set_facecolor('#D7D7D7')

            rect1 = self.axes2.patch
            rect1.set_facecolor('#A0BA8C')

            

            self.offset = wx.Button(self, -1, 'OFFSET LVDTS')
            self.avanca = wx.Button(self, -1, 'INICIAR')
            self.fim = wx.Button(self, -1, 'FIM')
            self.continua = wx.Button(self, -1, 'CONTINUAR')
            self.fim.Enable(False)
            self.avanca.Enable(False)
            self.continua.Enable(False)

            self.offset.SetFont(FontTitle)
            self.avanca.SetFont(FontTitle)
            self.fim.SetFont(FontTitle)
            self.continua.SetFont(FontTitle)

            # self.avanca.SetForegroundColour((190,190,190))
            # self.pausa.SetForegroundColour((190,190,190))
            # self.continua.SetForegroundColour((190,190,190))
            # self.fim.SetForegroundColour((190,190,190))

            self.v_sizer.Add(self.offset, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.avanca, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.fim, 1, wx.EXPAND | wx.ALL, 5)
            self.v_sizer.Add(self.continua, 1, wx.EXPAND | wx.ALL, 5)

            texto1 = wx.StaticText(self, label = "Velocidade: ", style = wx.ALIGN_CENTER)
            texto2 = wx.StaticText(self, label = "Forca: ", style = wx.ALIGN_CENTER)
            texto3 = wx.StaticText(self, label = "Deslocamento: ", style = wx.ALIGN_CENTER)
            self.velocidade = wx.TextCtrl(self, -1, 'VELOCIDADE', size = (100, 20), style = wx.TE_READONLY | wx.TE_CENTER)
            self.lvdt1 = wx.TextCtrl(self, -1, 'LVDT 1', size = (100, 20), style = wx.TE_READONLY | wx.TE_CENTER)
            self.lvdt2 = wx.TextCtrl(self, -1, 'LVDT 2', size = (100, 20), style = wx.TE_READONLY | wx.TE_CENTER)
            self.h_sizer1.Add(texto1, 1, wx.CENTER)
            self.h_sizer1.Add(self.velocidade, 2, wx.CENTER)
            self.h_sizer1.Add(texto2, 1, wx.CENTER)
            self.h_sizer1.Add(self.lvdt1, 2, wx.CENTER)
            self.h_sizer1.Add(texto3, 1, wx.CENTER)
            self.h_sizer1.Add(self.lvdt2, 2, wx.CENTER)

            self.v_sizer_grafico.Add(self.canvas, 1, wx.CENTER | wx.ALL, 5)
            self.v_sizer_grafico.Add(self.canvas1, 1, wx.CENTER | wx.ALL, 5)
            self.v_sizer_grafico.Add(self.canvas2, 1, wx.CENTER | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer_grafico, 1, wx.CENTER | wx.ALL, 5)

            # self.h_sizer.Add(self.canvas, 1, wx.CENTER | wx.ALL, 5)
            # self.h_sizer.Add(self.canvas1, 1, wx.CENTER | wx.ALL, 5)
            self.h_sizer.Add(self.v_sizer, 1, wx.EXPAND | wx.ALL)

            self.sizer.Add(self.h_sizer, 14, wx.EXPAND | wx.ALL, 4)
            self.sizer.Add(self.h_sizer1, 1, wx.EXPAND | wx.ALL)
            self.SetSizer(self.sizer)
    #--------------------------------------------------
        def leituras(self):
            try:
                self.lvdt2.Clear()
                self.lvdt1.Clear()
                self.velocidade.Clear()
                self.lvdt2.AppendText(leitura_lvdt2)
                self.lvdt1.AppendText(leitura_lvdt1)
                self.velocidade.AppendText(leitura_velocidade)
            except:
                self.lvdt2.Clear()
                self.lvdt1.Clear()
                self.velocidade.Clear()

    #--------------------------------------------------
        def draw(self):
            global line1
            global line2
            global line3
            x = np.arange(0,10,0.01)
            y = np.cos(np.pi*x)
            line1, = self.axes.plot(x, y, 'xkcd:off white')
            line2, =self.axes1.plot(x,y,'xkcd:off white')
            line3, =self.axes2.plot(x,y,'xkcd:off white')

    #--------------------------------------------------
        def plot(self,lvdt1,lvdt2,velocidade):
            x = lvdt2
            y = lvdt1
            velocidade=velocidade
            

            if velocidade[-1]-int(velocidade[-1])==0:

                line1.set_xdata(x)
                line1.axes.set_xlim((0, x[-1]*1.01))
                line1.set_ydata(y)
                line1.axes.set_ylim((-0.05, 1.05*max(y)))
                self.figure.canvas.draw()

                line2.set_xdata(velocidade)
                line2.axes.set_xlim((0, velocidade[-1]*1.01))
                line2.set_ydata(x)
                line2.axes.set_ylim((-0.05*min(x), 1.05*max(x)))
                self.figure1.canvas.draw()

                line3.set_xdata(velocidade)
                line3.axes.set_xlim((0, velocidade[-1]*1.01))
                line3.set_ydata(y)
                line3.axes.set_ylim((-0.05*min(y), 1.05*max(y)))
                self.figure2.canvas.draw()
  
            self.figure.canvas.flush_events()
            # print("passou")

        def cleanplot(self):
            self.figure.clf()
            self.figure.close()

        def plot_save(self, identificador_norma,vetor1,vetor2):
            plt.figure(figsize=(7, 4))
            deformacao = vetor2 #*0.0061
            estabilidade = vetor1 #3.4672
            plt.plot(deformacao, estabilidade)
            plt.ylim(-0.05, 1.05*max(estabilidade))
            plt.xlim(0, max(deformacao))
            plt.title('Ensaio de Marshall')
            plt.ylabel('Forca, kgf')
            plt.xlabel('Deslocamento, mm')
            plt.grid(True)
            plt.savefig('graficos\E'+str(identificador_norma)+'.png', format='png')
            plt.clf()
            plt.close()


'''Tela Realização do Ensaio'''
class TelaRealizacaoEnsaioDNER04395(wx.Dialog):
    #--------------------------------------------------
        def __init__(self,rconexao,*args, **kwargs):
            wx.Dialog.__init__(self, parent = None, title = 'Software Marshall - DNER-ME 043/95', size = (1200,700), style = wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            self.leitura_lvdt1=[]
            self.leitura_lvdt2=[]
            self.vetorLeitura_lvdt1=[]
            self.vetorLeitura_lvdt2=[]
            self.velocidade=[]
            global conexao
            conexao = rconexao

            '''Iserção do IconeLogo'''
            ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(ico)

            '''Configurações do SPLITTER'''
            top = TopPanel(self)
            top.draw()

            id = bancodedadosnovo.get_id()
            dados_ensaio = bancodedadosnovo.get_dadosEnsaio(id)
            cte_anel = dados_ensaio[0][11]

            # self.Centre()
            self.Show()
            self.Maximize()
            info = "MARSHALL"
            titulo = "Preparação do ensaio."
            message1 = "Verifique se está tudo certo!"
            message2 = "Realize o ajuste de altura conforme o necessario para o inicio do ensaio."
            dlg = dialogoDinamico(5, info, titulo, message1, message2, "", None, conexao)
            if dlg.ShowModal() == wx.ID_OK:
                print("ok")
            '''self.Maximize(True)'''
            def leitura(event):
                global leitura_velocidade
                
                conexao.write('I')
                leitura=[0,0,0,0]
                valores = conexao.readline()
                leitura=valores.split(',')
                est_ens=float(leitura[0])
                estabilidade=float(leitura[1])
                velocidade=float(leitura[2])
                fluencia=float(leitura[3])
                while(leitura[0] == '0'):
                    if float(estabilidade)>0:
                        v1 = round((estabilidade - 1.0)*10000*cte_anel,4)#estabilidade --> força
                        v2 = velocidade#velocidade
                        v3 = round((fluencia - 1.0)*1000*0.00605532,3)#fluencia 0.00614944 antigo --> novo 0,00605532 deslocamento
                        self.leitura_lvdt1.append(v1)
                        self.velocidade.append(v2)
                        self.leitura_lvdt2.append(v3)
                        # print ("vet1:"+str(len(self.leitura_lvdt1))+" vet2:"+str(len(self.leitura_lvdt2)))
                        if len(self.leitura_lvdt1)>50:
                            self.vetorLeitura_lvdt1=savgol_filter(self.leitura_lvdt1,51,6)
                            self.vetorLeitura_lvdt2=savgol_filter(self.leitura_lvdt2,51,6)
                            
                            top.plot(self.vetorLeitura_lvdt1,self.vetorLeitura_lvdt2,self.velocidade)
                            leitura_velocidade = str(v2)
                            top.leituras()
                

                    leitura = conexao.readline()
                    leitura=leitura.split(',')
                    try:
                        est_ens=float(leitura[0])
                        estabilidade=float(leitura[1])
                        velocidade=float(leitura[2])
                        fluencia=float(leitura[3])
                        backup=leitura
                    except Exception as e:
                        print("dados incompletos")
                        est_ens=float(backup[0])
                        estabilidade=float(backup[1])
                        velocidade=float(backup[2])
                        fluencia=float(backup[3])
                    

                top.fim.Enable(True)
                print(len(self.vetorLeitura_lvdt1))
                if(len(self.vetorLeitura_lvdt1) > 45):
                    vetor1=[]
                    vetor2=[]
                    for i in range(0, len(self.vetorLeitura_lvdt1), 50):
                        vetor1.append(self.vetorLeitura_lvdt1[i])
                        vetor2.append(self.vetorLeitura_lvdt2[i])
                    print(vetor1)
                    print(vetor2)

                    # print ("vet1:"+str(len(vetor1))+" vet2:"+str(len(vetor2)))
                    bancodedadosnovo.write_table_Ensaio(id, vetor1, vetor2)
                else:
                    vetor1=[]
                    vetor2=[]
                    for i in range(0, len(self.vetorLeitura_lvdt1), 50):
                        vetor1.append(self.leitura_lvdt1[i])
                        vetor2.append(self.leitura_lvdt2[i])
                    bancodedadosnovo.write_table_Ensaio(id, str(vetor1), str(vetor2))
                    bancodedadosnovo.delete(id)
                    print("apagou")
                    logging.basicConfig(filename=str(id)+'example.log',level=logging.DEBUG)
                    logging.debug('Ensaio inacabado devido a: quantidade de dados coletados insuficiente')

            def estado():
                global estado_do_ensaio
                if(estado_do_ensaio == 1 or estado_do_ensaio == 2 or estado_do_ensaio == 3):
                    return True
                else:
                    return False
            def iniciar(event):
                top.avanca.Enable(False)
                global estado_do_ensaio
                estado_do_ensaio = 1
                contador = 0
                leitura(event)
            def offset(event):
                conexao.write('C')
                leitura = conexao.readline()
                v1 = round((float(leitura[6:12]) - 1.0)*10000*cte_anel,4)
                v2 = float(leitura[12:18])
                v3 = round((float(leitura[18:23]) - 1.0)*1000*0.00614944,3)
                print(leitura, " ", v1, " ", v2, " ", v3)
                global leitura_lvdt1
                global leitura_velocidade
                global leitura_lvdt2
                leitura_lvdt1 = str(v1)
                leitura_velocidade = str(v2)
                leitura_lvdt2 = str(v3)
                top.leituras()
                top.avanca.Enable(True)
                top.offset.Enable(False)
            def continuar(event):
                global estado_do_ensaio
                estado_do_ensaio = 1
                leitura(event)
            def fim(event):
                global estado_do_ensaio
                global identificador_norma
                estado_do_ensaio = 2
                conexao.write('F')
                top.fim.Enable(False)
                top.plot_save(id,self.vetorLeitura_lvdt1,self.vetorLeitura_lvdt2)
                self.vetorLeitura_lvdt1 = []
                self.vetorLeitura_lvdt2 = []
                conexao.close()
                self.Close(True) #fechar a tela depois que aperta o botão fim
                # tela.Tela(self).basic_gui()


            top.avanca.Bind(wx.EVT_BUTTON, iniciar)
            top.offset.Bind(wx.EVT_BUTTON, offset)
            top.continua.Bind(wx.EVT_BUTTON, continuar)
            top.fim.Bind(wx.EVT_BUTTON, fim)
