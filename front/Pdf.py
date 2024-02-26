# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import banco.bancodedadosCAB as bancodedadosCAB
import banco.bancodedados as bancodedados
import banco.bdPreferences as bdPreferences
import banco.bdConfiguration as bdConfiguration
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import subprocess
from pyppeteer import launch
import asyncio

#--------------------------------------------------
def pm(mm):
    return mm/0.352777

'''Class Export PDF'''
class Pdf134(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.idt = idt
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_134_pdf(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)

    #--------------------------------------------------
     def createPDF(self, name):
            idt = self.idt
            lista = self.list

            # '''Obtendo os dados do cabeçario no bancoCAB'''
            listaCAB = bancodedadosCAB.ListaDadosCab(self.Id) #obtenção do cabeçariao do ensaio
            

            # '''Obter dados do banco'''
            list = bancodedados.dados_iniciais_(idt) #obtenção dos dados do ensaio
            lvdt = bdConfiguration.S1S2() #obtem dados do sensores S1 e S2

            if int(list[2]) == 0:
                valoramostra = 'Deformada'
            else:
                valoramostra = 'Indeformada'
            try:
                desvioUmidade = str(float(list[4])-float(list[6]))
            except:
                desvioUmidade = ''

            # '''Criando arquivo PDF'''
            with wx.FileDialog(self,defaultDir=idt,defaultFile=idt, name=idt, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                # if fileDialog.ShowModal() == wx.ID_CANCEL:
                #     return

                # pathname = fileDialog.GetPath()
                pathname= 'C:\\Users\\brenn\\OneDrive\\Documentos\\testesEDP\\'+idt
                pathname=bancodedados.get_dir_result(1)
                pathname=pathname+"\\"+idt
                # try:
                if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                    diretorio = pathname
                else:
                    diretorio = pathname+".pdf"

                cnv = canvas.Canvas(diretorio, pagesize=A4)
                cnv.setTitle(idt)

                #CABEÇALHO
                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])


                #CORPO
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Módulo de Resiliência')
                cnv.setFont("Helvetica", 11)
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Tipo de amostra:')
                cnv.drawRightString(pm(110), pm(200+x), 'Energia de compactação:')
                cnv.drawRightString(pm(110), pm(195+x), 'Tamanho do Corpo de Prova [mm]:')
                cnv.drawRightString(pm(110), pm(190+x), 'Teor de umidade do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(185+x), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                cnv.drawRightString(pm(110), pm(180+x), 'Grau de compactação do Corpo de Prova [%]:')
                cnv.drawRightString(pm(110), pm(175+x), 'Desvio de umidade [%]:')
                cnv.drawRightString(pm(110), pm(170+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(165+x), 'Curso do LVDT empregado [mm]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 134/2018-ME')
                cnv.drawString(pm(112), pm(225+x), list[9])
                cnv.drawString(pm(112), pm(220+x), list[10])
                cnv.drawString(pm(112), pm(215+x), list[11])
                cnv.drawString(pm(112), pm(210+x), list[3])
                cnv.drawString(pm(112), pm(205+x), valoramostra)
                cnv.drawString(pm(112), pm(200+x), list[7])
                cnv.drawString(pm(112), pm(195+x), str(format(list[13]).replace('.',','))+' x '+str(format(list[14]).replace('.',',')))
                cnv.drawString(pm(112), pm(190+x), list[4])
                cnv.drawString(pm(112), pm(185+x), list[5])
                cnv.drawString(pm(112), pm(180+x), list[8])
                cnv.drawString(pm(112), pm(175+x), desvioUmidade)
                cnv.drawString(pm(112), pm(170+x), str(list[16]))
                cnv.drawString(pm(112), pm(165+x), str(int(lvdt[3])))

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 720, 576)
                t.drawOn(cnv, pm(48), pm((19-len(lista))*6.35+25))
                
                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23]) 

                #pagina2
                cnv.showPage()

                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])
                
                tensaoConfinante=[]
                tensaoDesvio=[]
                tensaoMR=[]
                tensaoCombinada=[]
                i=1
                while i < len(lista):
                    tensaoConfinante.append(float(lista[i][1].replace(",",".")))
                    tensaoDesvio.append(float(lista[i][2].replace(",",".")))
                    tensaoMR.append(float(lista[i][5].replace(",",".")))
                    tensaoCombinada.append((float(lista[i][1].replace(",",".")))+(float(lista[i][2].replace(",","."))))
                    i+=1
                
                x=np.array(tensaoDesvio)
                y=np.array(tensaoMR)
                # trace = go.Scatter(x=x, y=y, mode='markers')
                # data = [trace]
                # fig = go.Figure(data=data)


            


                log_x_data = np.log(x)
                log_y_data = np.log(y)

                # modelo = LinearRegression()
                # modelo.fit(x.reshape(-1,1),y)

                coefficients = np.polyfit(np.log(x), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                # Calcule o R^2
                y_pred = np.exp(intercept)*x**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared)

                

                intercept_MR_x_sigmad=intercept
                slope_MR_sigmad=slope

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                x_trend = np.linspace(min(x), max(x), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                trace_scatter = go.Scatter(x=x, y=y, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Tensão de Desvio X MR',xaxis=dict(title='Tensao de Desvio'), yaxis=dict(title='MR'))
                fig = go.Figure(data=data, layout=layout)
                # fig.update_xaxes(type='log')
                # fig.update_yaxes(type='log')
                pio.write_image(fig, 'grafico.png')

                x=np.array(tensaoConfinante)
                # trace = go.Scatter(x=tensaoConfinante, y=tensaoMR, mode='markers')
                # data = [trace]
                # fig = go.Figure(data=data)
                # modelo = LinearRegression()
                # modelo.fit(x.reshape(-1,1),y)

                log_x_data = np.log(x)
                log_y_data = np.log(y)

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                coefficients = np.polyfit(np.log(x), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                # Calcule o R^2
                y_pred = np.exp(intercept)*x**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared1 = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared1)

                intercept_MR_x_sigma3=intercept
                slope_MR_sigma3=slope

                x_trend = np.linspace(min(x), max(x), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                trace_scatter = go.Scatter(x=tensaoConfinante, y=tensaoMR, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Tensão confinante X MR',xaxis=dict(title='Tensao Confinante'), yaxis=dict(title='MR'))
                fig = go.Figure(data=data, layout=layout)
                pio.write_image(fig, 'grafico1.png')
                
                

                

                # # Desenhar a imagem no canvas PDF
                cnv.drawInlineImage("grafico.png", 50, 400,width=300,height=300) 

                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(220), 'MR=K1σd^K2 ')
                cnv.drawString(pm(150), pm(215), 'K1= '+ str(np.exp(intercept_MR_x_sigmad)))
                cnv.drawString(pm(150), pm(210), 'K2= '+ str(slope_MR_sigmad))
                cnv.drawString(pm(150), pm(205), 'R^2= '+ str(r_squared))
                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(115), 'MR=K1σ3^K2 ')
                cnv.drawString(pm(150), pm(110), 'K1= '+ str(np.exp(intercept_MR_x_sigma3)))
                cnv.drawString(pm(150), pm(105), 'K2= '+ str(slope_MR_sigma3))
                cnv.drawString(pm(150), pm(100), 'R^2= '+ str(r_squared1))


                cnv.drawInlineImage("grafico1.png", 50, 100,width=300,height=300)

                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])

                #pagina3
                cnv.showPage()

                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                x1=np.array(tensaoCombinada)
                # trace = go.Scatter(x=tensaoCombinada, y=tensaoMR, mode='markers')
                # data = [trace]
                # fig = go.Figure(data=data)
                # modelo = LinearRegression()
                # modelo.fit(x1.reshape(-1,1),y)

                log_x_data = np.log(x1)
                log_y_data = np.log(y)

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                coefficients = np.polyfit(np.log(x1), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                y_pred = np.exp(intercept)*x1**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared2 = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared1)

                x_trend = np.linspace(min(x1), max(x1), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                intercept_MR_x_sigma1=intercept
                slope_MR_sigma1=slope



                trace_scatter = go.Scatter(x=tensaoCombinada, y=tensaoMR, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Somatorio das Tensões X MR',xaxis=dict(title='Somatorio das Tensões'), yaxis=dict(title='MR'))
                fig = go.Figure(data=data, layout=layout)
                pio.write_image(fig, 'grafico2.png')
                data=[]
                
                
                # # Desenhar a imagem no canvas PDF
                cnv.drawInlineImage("grafico2.png", 50, 400,width=300,height=300)

                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(220), 'MR=K1θ^K2 ')
                cnv.drawString(pm(150), pm(215), 'K1= '+ str(np.exp(intercept_MR_x_sigma1)))
                cnv.drawString(pm(150), pm(210), 'K2= '+ str(slope_MR_sigma1))
                cnv.drawString(pm(150), pm(205), 'R^2= '+ str(r_squared2)) 


                # Separar em 6 listas de 3 elementos cada
                listas_separadas = [tensaoDesvio[i:i+3] for i in range(0, len(tensaoDesvio), 3)]
                mr_separada=[tensaoMR[i:i+3] for i in range(0, len(tensaoMR), 3)]

                # Exibindo as listas separadas
                cont=1
                for lista,lista1 in zip(listas_separadas,mr_separada):
                    x1=np.array(lista)
                    log_x_data = np.log(x1)
                    log_y_data = np.log(lista1)
                    # modelo = LinearRegression()
                    # modelo.fit(x1.reshape(-1,1),lista1)

                    # a_coeff = modelo.coef_
                    # l_coeff = modelo.intercept_

                    coefficients = np.polyfit(np.log(x1), lista1, 1)
                    slope = coefficients[0]
                    intercept = coefficients[1]

                    x_trend = np.linspace(min(x1), max(x1), 100)
                    y_trend = slope * np.log(x_trend) + intercept


                    trace_scatter = go.Scatter(x=x1, y=lista1, mode='markers',name='Pontos '+str(cont))
                    trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva ajuste '+str(cont))
                    cont+=1
                    data.append(trace_scatter)
                    data.append(trace_fit)

                
                layout = go.Layout(title='Modelo Combinado',xaxis=dict(title='Tensao'), yaxis=dict(title='MR'))
                fig = go.Figure(data=data, layout=layout)
                pio.write_image(fig, 'grafico3.png')
                
                # # Desenhar a imagem no canvas PDF
                cnv.drawInlineImage("grafico3.png", 50, 100,width=300,height=300)
                


                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])

                leitorpdf='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
                leitorpdf=str(bancodedados.get_dir_result(2))

                cnv.save()
                self.Destroy()
                subprocess.Popen([leitorpdf, diretorio])

                # except Exception as e:
                #     print("Exceção:", type(e).__name__)
                #     wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                #     dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                #     result = dlg.ShowModal()
                #     self.Destroy()
                #     return

class pdf183(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.idt = idt
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_183_pdf(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)
    
    #--------------------------------------------------
     def createPDF(self, name):
            idt = self.idt
            lista = self.list

            '''Obtendo os dados do cabeçario no bancoCAB'''
            listaCAB = bancodedadosCAB.ListaDadosCab(self.Id) #obtenção do cabeçariao do ensaio
            

            '''Obter dados do banco'''
            list = bancodedados.dados_iniciais_(idt) #obtenção dos dados do ensaio
            # lvdt = bdConfiguration.S1S2() #obtem dados do sensores S1 e S2

            if int(list[2]) == 0:
                valoramostra = 'Deformada'
            else:
                valoramostra = 'Indeformada'
            try:
                desvioUmidade = str(float(list[4])-float(list[6]))
            except:
                desvioUmidade = ''

            '''Criando arquivo PDF'''
            with wx.FileDialog(self,defaultDir=idt,defaultFile=idt, name=idt, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                # if fileDialog.ShowModal() == wx.ID_CANCEL:
                #     return

                # pathname = fileDialog.GetPath()
                pathname= 'C:\\Users\\brenn\\OneDrive\\Documentos\\testesEDP\\'+idt
                pathname=bancodedados.get_dir_result(1)
                pathname=pathname+"\\"+idt
                # try:
                if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                    diretorio = pathname
                else:
                    diretorio = pathname+".pdf"

                cnv = canvas.Canvas(diretorio, pagesize=A4)
                cnv.setTitle(idt)

                #CABEÇALHO
                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                #CORPO
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Fadiga')
                cnv.setFont("Helvetica", 11)
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Resistencia a tração:')
                cnv.drawRightString(pm(110), pm(200+x), 'Nivel de Tensão:')
                cnv.drawRightString(pm(110), pm(195+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(190+x), 'Modulo de resiliencia Medio [MPa]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 183/2018-ME')
                cnv.drawString(pm(112), pm(225+x), list[9])
                cnv.drawString(pm(112), pm(220+x), list[10])
                cnv.drawString(pm(112), pm(215+x), list[11])
                cnv.drawString(pm(112), pm(210+x), list[3])
                cnv.drawString(pm(112), pm(205+x), list[24])
                list[25]=float(list[25])*100
                cnv.drawString(pm(112), pm(200+x), str(list[25])+'%')
                cnv.drawString(pm(112), pm(195+x), str(list[16]))
                cnv.drawString(pm(112), pm(190+x), str(list[27]))

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 700, 576)
                t.drawOn(cnv, pm(12), pm((23-len(lista))*6.35+25))

                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])

                cnv.showPage()
                # pagina 2

                #CABEÇALHO
                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                
                defResiliente=[]
                difTensao=[]
                Ngolpes=[]
                i=1
                while i < len(lista):
                    defResiliente.append(float(lista[i][1]))
                    difTensao.append(float(lista[i][8]))
                    Ngolpes.append(float(lista[i][4]))
                    i+=1
                
                x=np.array(defResiliente)
                y=np.array(Ngolpes)

                log_x_data = np.log(x)
                log_y_data = np.log(y)

                coefficients = np.polyfit(np.log(x), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                # Calcule o R^2
                y_pred = np.exp(intercept)*x**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared)

                

                intercept_MR_x_sigmad=intercept
                slope_MR_sigmad=slope

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                x_trend = np.linspace(min(x), max(x), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                trace_scatter = go.Scatter(x=x, y=y, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Deformação especifica resiliente X Vida de Fadiga',xaxis=dict(title='Deformação especifica resiliente'), yaxis=dict(title='Numero de aplicações, N'))
                fig = go.Figure(data=data, layout=layout)
                fig.write_html('Img\\grafico.html')

                async def html_to_png(input_file, output_file):
                    browser = await launch()
                    page = await browser.newPage()
                    with open(input_file, 'r', encoding='utf-8') as file:
                        html_content = file.read()

                    await page.setContent(html_content)
                    await page.screenshot({'path': output_file, 'fullPage': True})
                    await browser.close()
                # options = {
                #     'format': 'png',
                #     'width': 1920,
                #     'height': 1280,
                # }
                # with open('grafico1.html') as f:
                #     imgkit.from_file(f, 'out.jpg')
                    
                html_input_file = 'Img\\grafico.html'
                output_file = 'Img\\grafico.png'

                asyncio.get_event_loop().run_until_complete(html_to_png(html_input_file, output_file))

                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(220), 'N='+ str(round(np.exp(intercept),4))+'*ε')
                cnv.setFont("Helvetica", 8)
                cnv.drawString(pm(172), pm(222), str(round(slope,4)))
                cnv.drawString(pm(170), pm(220), 'r')
                cnv.setFont("Helvetica", 11) 
                cnv.drawString(pm(150), pm(215), 'R^2= '+ str(round(r_squared,4)))
                cnv.drawString(pm(150), pm(210), 'K3= '+ str(round(np.exp(intercept),4)))
                cnv.drawString(pm(150), pm(205), 'n3= '+ str(round(slope,4)))
                
                
    


                x=np.array(difTensao)
                y=np.array(Ngolpes)

                log_x_data = np.log(x)
                log_y_data = np.log(y)

                coefficients = np.polyfit(np.log(x), np.log(y), 1)
                slope = coefficients[0]
                intercept = coefficients[1]

                # Calcule o R^2
                y_pred = np.exp(intercept)*x**slope
                residuals = y - y_pred
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y - np.mean(y))**2)
                r_squared = 1 - (ss_res / ss_tot)
                print("Coeficiente de Determinação (R^2):", r_squared)

                

                intercept_MR_x_sigmad=intercept
                slope_MR_sigmad=slope

                # a_coeff = modelo.coef_
                # l_coeff = modelo.intercept_

                x_trend = np.linspace(min(x), max(x), 100)
                y_trend = np.exp(intercept)*x_trend**slope

                trace_scatter = go.Scatter(x=x, y=y, mode='markers',name='Pontos')
                trace_fit = go.Scatter(x=x_trend, y=y_trend, mode='lines',name='Curva de ajuste')
                data = [trace_scatter, trace_fit]
                layout = go.Layout(title='Diferença de tensões X Vida de Fadiga',xaxis=dict(title='Diferença de tensões'), yaxis=dict(title='Numero de aplicações, N'))
                fig = go.Figure(data=data, layout=layout)
                # fig.update_xaxes(type='log')
                # fig.update_yaxes(type='log')
                fig.write_html('Img\\grafico1.html')

                async def html_to_png(input_file, output_file):
                    browser = await launch()
                    page = await browser.newPage()
                    with open(input_file, 'r', encoding='utf-8') as file:
                        html_content = file.read()

                    await page.setContent(html_content)
                    await page.screenshot({'path': output_file, 'fullPage': True})
                    await browser.close()
                # options = {
                #     'format': 'png',
                #     'width': 1920,
                #     'height': 1280,
                # }
                # with open('grafico1.html') as f:
                #     imgkit.from_file(f, 'out.jpg')
                    
                html_input_file = 'Img\\grafico1.html'
                output_file = 'Img\\grafico1.png'

                asyncio.get_event_loop().run_until_complete(html_to_png(html_input_file, output_file))
                
                cnv.setFont("Helvetica", 11)
                cnv.drawString(pm(150), pm(120), 'N='+ str(round(np.exp(intercept),4))+'*σ')
                cnv.setFont("Helvetica", 8)
                cnv.drawString(pm(175), pm(122), str(round(slope,4)))
                cnv.drawString(pm(173), pm(120), 'd')
                cnv.setFont("Helvetica", 11) 
                cnv.drawString(pm(150), pm(115), 'R^2= '+ str(round(r_squared,4))) 
                cnv.drawString(pm(150), pm(110), 'K3= '+ str(round(np.exp(intercept),4)))
                cnv.drawString(pm(150), pm(105), 'n3= '+ str(round(slope,4)))

                cnv.drawInlineImage("Img\\grafico.png", 50, 400,width=300,height=300)
                
                cnv.drawInlineImage("Img\\grafico1.png", 50, 100,width=300,height=300)

                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])


                leitorpdf='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
                leitorpdf=str(bancodedados.get_dir_result(2))

                cnv.save()
                self.Destroy()
                subprocess.Popen([leitorpdf, diretorio])



class pdf135(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.idt = idt
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_135_pdf(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)
    
    #--------------------------------------------------
     def createPDF(self, name):
            idt = self.idt
            lista = self.list

            '''Obtendo os dados do cabeçario no bancoCAB'''
            listaCAB = bancodedadosCAB.ListaDadosCab(self.Id) #obtenção do cabeçariao do ensaio

            '''Obter dados do banco'''
            list = bancodedados.dados_iniciais_(idt) #obtenção dos dados do ensaio
            # lvdt = bdConfiguration.S1S2() #obtem dados do sensores S1 e S2

            if int(list[2]) == 0:
                valoramostra = 'Deformada'
            else:
                valoramostra = 'Indeformada'
            try:
                desvioUmidade = str(float(list[4])-float(list[6]))
            except:
                desvioUmidade = ''

            '''Criando arquivo PDF'''
            with wx.FileDialog(self,defaultDir=idt,defaultFile=idt, name=idt, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                # if fileDialog.ShowModal() == wx.ID_CANCEL:
                #     return

                # pathname = fileDialog.GetPath()
                pathname= 'C:\\Users\\brenn\\OneDrive\\Documentos\\testesEDP\\'+idt
                pathname=bancodedados.get_dir_result(1)
                pathname=pathname+"\\"+idt
                # try:
                if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                    diretorio = pathname
                else:
                    diretorio = pathname+".pdf"

                cnv = canvas.Canvas(diretorio, pagesize=A4)
                cnv.setTitle(idt)

                #CABEÇALHO
                try:
                    cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                except:
                    pass
                cnv.setFont("Helvetica-Bold", 16)
                cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                #CORPO
                cnv.setFont("Helvetica-Bold", 14)
                cnv.drawCentredString(pm(110), pm(242), 'Relatório de Modulo de Resiliencia para misturas asfalticas')
                cnv.setFont("Helvetica", 11)
                x = -2
                cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                cnv.drawRightString(pm(110), pm(205+x), 'Resistencia a tração [MPa]:')
                cnv.drawRightString(pm(110), pm(200+x), 'Frequência do ensaio [Hz]:')
                cnv.drawRightString(pm(110), pm(195+x), 'Temperatura do ensaio:')
                cnv.drawRightString(pm(110), pm(190+x), 'Coeficiente de Poisson adotado [μ]:')
                cnv.drawRightString(pm(110), pm(185+x), 'Nivel de Tensão Inicial:')


                # cnv.drawRightString(pm(110), pm(190+x), 'Modulo de resiliencia Medio [MPa]:')

                cnv.drawString(pm(112), pm(235+x), idt)
                cnv.drawString(pm(112), pm(230+x), 'DNIT 135/2018-ME')
                cnv.drawString(pm(112), pm(225+x), list[9])
                cnv.drawString(pm(112), pm(220+x), list[10])
                cnv.drawString(pm(112), pm(215+x), list[11])
                cnv.drawString(pm(112), pm(210+x), list[3])
                cnv.drawString(pm(112), pm(205+x), list[24])
                # list[25]=float(list[25])*100
                # cnv.drawString(pm(112), pm(200+x), str(list[25])+'%')
                cnv.drawString(pm(112), pm(200+x), str(list[16]))
                cnv.drawString(pm(112), pm(195+x), '25°C')
                # cnv.drawString(pm(112), pm(190+x), str(list[27]))
                cnv.drawString(pm(112), pm(190+x), '0,3')
                nivel_tensao=float(list[25])*100
                cnv.drawString(pm(112), pm(185+x), str(nivel_tensao)+"%")

                #TABLE
                t=Table(lista)
                t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                t.wrapOn(cnv, 700, 576)
                t.drawOn(cnv, pm(30), pm((21-len(lista))*6.35+25))

                fase1=[]
                fase2=[]
                fase3=[]
                x3=[]
                y3=[]
                pontos=bancodedados.getpulso135(idt)
                for item in pontos:
                    if item[0]==1:
                        fase1.append(item)
                    elif item[0]==2:
                        fase2.append(item)
                    else:
                        x3.append(item[1])
                        y3.append(item[2])

                trace_scatter = go.Scatter(x=x3, y=y3, mode='markers',name='Pontos',marker=dict(color='black'))
                data = [trace_scatter]
                layout = go.Layout(title='Pulso dos ultimos 5 golpes',xaxis=dict(title='Numero de Golpes, N',showline=True, linecolor='black'), yaxis=dict(title='Deslocamento, (mm)',showline=True,linecolor='black'),plot_bgcolor='white',xaxis_gridcolor='lightgray',yaxis_gridcolor='lightgray')
                fig = go.Figure(data=data, layout=layout)
                fig.write_html('Img\\grafico1.html')

                async def html_to_png(input_file, output_file):
                    browser = await launch()
                    page = await browser.newPage()
                    with open(input_file, 'r', encoding='utf-8') as file:
                        html_content = file.read()

                    await page.setContent(html_content)
                    await page.screenshot({'path': output_file, 'fullPage': True})
                    await browser.close()
                # options = {
                #     'format': 'png',
                #     'width': 1920,
                #     'height': 1280,
                # }
                # with open('grafico1.html') as f:
                #     imgkit.from_file(f, 'out.jpg')
                    
                html_input_file = 'Img\\grafico1.html'
                output_file = 'Img\\grafico1.png'

                asyncio.get_event_loop().run_until_complete(html_to_png(html_input_file, output_file))

                # imgkit.from_file(html_file_path, output_image_path,options=options)
                # image_bytes = to_image(fig, format='png')
                # fig.write_image('D:\\Games\\Nova pasta\\grafico1.jpeg')
                # pio.write_image(fig, 'grafico1.png')
                cnv.drawInlineImage("Img\\grafico1.png", 55, 75,width=500,height=300)
                

                #RODAPÉ
                o = Paragraph('OBS.: '+list[15])
                o.wrapOn(cnv, 250, 50)
                o.drawOn(cnv, pm(32), pm(10))
                cnv.line(pm(130),pm(18),pm(195),pm(18))
                cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                cnv.drawString(pm(130), pm(10), list[23])

                leitorpdf='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
                leitorpdf=str(bancodedados.get_dir_result(2))

                cnv.save()
                self.Destroy()
                subprocess.Popen([leitorpdf, diretorio])

















# '''Class Export PDF'''
class Pdf179(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.Bind(wx.EVT_CLOSE, self.onExit)
        
        self.idt = idt
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()

    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_179_pdf(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)

    #--------------------------------------------------
     def createPDF(self, name):
            idt = self.idt
            lista = self.list

            '''Obtendo os dados do banco'''
            listaCAB = bancodedadosCAB.ListaDadosCab(self.Id) # obtenção dos dados do cabeçario
            

            '''Obter dados do banco'''
            list = bancodedados.dados_iniciais_(idt) #obtenção dos dados do ensaio
            lvdt = bdConfiguration.S1S2() # obtenção dos dados dos sensores S1 e S2
            

            if int(list[12]) == 0:
                valoramostra = 'Deformada'
            else:
                valoramostra = 'Indeformada'
            try:
                desvioUmidade = str(float(list[4])-float(list[6]))
            except:
                desvioUmidade = ''
            try:
                pressaoConf = str(float(list[17])*1000)
            except:
                pressaoConf = ''
            try:
                pressaoDesvio = str(float(list[18])*1000)
            except:
                pressaoDesvio = ''

            '''Criando arquivo PDF'''
            with wx.FileDialog(self, name, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

                pathname = fileDialog.GetPath()

                try:
                    if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                        diretorio = pathname
                    else:
                        diretorio = pathname+".pdf"

                    cnv = canvas.Canvas(diretorio, pagesize=A4)
                    cnv.setTitle(idt)

                    #CABEÇALHO
                    try:
                        cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                    except:
                        pass
                    cnv.setFont("Helvetica-Bold", 16)
                    cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                    cnv.setFont("Helvetica-Bold", 14)
                    cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                    cnv.setFont("Helvetica", 11)
                    cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                    cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                    cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                    cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])


                    #CORPO
                    cnv.setFont("Helvetica-Bold", 14)
                    cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Deformação Permanente')
                    cnv.setFont("Helvetica", 11)
                    x = -2
                    cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                    cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                    cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                    cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                    cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                    cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                    cnv.drawRightString(pm(110), pm(205+x), 'Tipo de amostra:')
                    cnv.drawRightString(pm(110), pm(200+x), 'Energia de compactação:')
                    cnv.drawRightString(pm(110), pm(195+x), 'Tamanho do Corpo de Prova [mm]:')
                    cnv.drawRightString(pm(110), pm(190+x), 'Teor de umidade do Corpo de Prova [%]:')
                    cnv.drawRightString(pm(110), pm(185+x), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                    cnv.drawRightString(pm(110), pm(180+x), 'Grau de compactação do Corpo de Prova [%]:')
                    cnv.drawRightString(pm(110), pm(175+x), 'Desvio de umidade [%]:')
                    cnv.drawRightString(pm(110), pm(170+x), 'Frequência do ensaio [Hz]:')
                    cnv.drawRightString(pm(110), pm(165+x), 'Curso do LVDT empregado [mm]:')
                    cnv.drawRightString(pm(110), pm(160+x), 'σ3 [kPa]:')
                    cnv.drawRightString(pm(110), pm(155+x), 'σd [kPa]:')
                    cnv.drawRightString(pm(90), pm(158+x), 'Estado de tensões do ensaio:')

                    cnv.drawString(pm(112), pm(235+x), idt)
                    cnv.drawString(pm(112), pm(230+x), 'DNIT 179/2018-IE')
                    cnv.drawString(pm(112), pm(225+x), list[9])
                    cnv.drawString(pm(112), pm(220+x), list[10])
                    cnv.drawString(pm(112), pm(215+x), list[11])
                    cnv.drawString(pm(112), pm(210+x), list[3])
                    cnv.drawString(pm(112), pm(205+x), valoramostra)
                    cnv.drawString(pm(112), pm(200+x), list[7])
                    cnv.drawString(pm(112), pm(195+x), str(format(list[13]).replace('.',','))+' x '+str(format(list[14]).replace('.',',')))
                    cnv.drawString(pm(112), pm(190+x), list[4])
                    cnv.drawString(pm(112), pm(185+x), list[5])
                    cnv.drawString(pm(112), pm(180+x), list[8])
                    cnv.drawString(pm(112), pm(175+x), desvioUmidade)
                    cnv.drawString(pm(112), pm(170+x), str(list[16]))
                    cnv.drawString(pm(112), pm(165+x), str(int(lvdt[3])))
                    cnv.drawString(pm(112), pm(160+x), format(pressaoConf).replace('.',','))
                    cnv.drawString(pm(112), pm(155+x), format(pressaoDesvio).replace('.',','))

                    if len(lista) <=17:
                        #TABLE1
                        t=Table(lista[0:17])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                    
                    elif len(lista) >17 and len(lista) <=54:
                        #TABLE1
                        t=Table(lista[0:17])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE2
                        t=Table([lista[0]]+lista[17:54])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                    
                    elif len(lista) >54 and len(lista) <=91:
                        #TABLE1
                        t=Table(lista[0:17])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE2
                        t=Table([lista[0]]+lista[17:54])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE3
                        t=Table([lista[0]]+lista[54:91])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[54:91]))*6.35+25))

                    elif len(lista) >91 and len(lista) <=128:
                        #TABLE1
                        t=Table(lista[0:17])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE2
                        t=Table([lista[0]]+lista[17:54])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE3
                        t=Table([lista[0]]+lista[54:91])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[54:91]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE4
                        t=Table([lista[0]]+lista[91:128])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[91:128]))*6.35+25))

                    elif len(lista) >128 and len(lista) <=165:
                        #TABLE1
                        t=Table(lista[0:17])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((17-len(lista[0:17]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE2
                        t=Table([lista[0]]+lista[17:54])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[17:54]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE3
                        t=Table([lista[0]]+lista[54:91])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[54:91]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE4
                        t=Table([lista[0]]+lista[91:128])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[91:128]))*6.35+25))
                        cnv.showPage()

                        #TABLEPAGE5
                        t=Table([lista[0]]+lista[128:165])
                        t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
                        
                        t.wrapOn(cnv, 720, 576)
                        t.drawOn(cnv, pm(45), pm((38-len([lista[0]]+lista[128:165]))*6.35+25))

                    #RODAPÉ
                    o = Paragraph('OBS.: '+list[15])
                    o.wrapOn(cnv, 250, 50)
                    o.drawOn(cnv, pm(32), pm(10))
                    cnv.line(pm(130),pm(18),pm(195),pm(18))
                    cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                    cnv.drawString(pm(130), pm(10), list[23]) 

                    cnv.save()
                    self.Destroy()
                    dlg = wx.MessageDialog(None, 'PDF gerado com sucesso', 'EDP', wx.OK|wx.CENTRE)#codigo para mostrar uma mensagem de confirmação quando o pdf for gerado
                    dlg.ShowModal()

                except:
                    wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                    dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()
                    self.Destroy()
                    return

'''Class Export PDF'''
class Pdf181(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, idt, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'EDP - PDF')
        self.Bind(wx.EVT_CLOSE, self.onExit)

        self.idt = idt
        self.Id = bancodedadosCAB.idEscolha()
        frame = self.basic_gui()

    #--------------------------------------------------
     def onExit(self, event):
        '''Opcao Sair'''
        self.Destroy()
        
    #--------------------------------------------------
     def basic_gui(self):
        idt = self.idt

        self.list = bancodedados.dados_da_coleta_181_pdf(idt)

        if len(self.list) == 1:
            menssagError = wx.MessageDialog(self, 'NADA AINDA!\n\n Seu arquivo PDF ainda não pode ser exportado!\n Alguns dados precisam ser coletados.', 'EDP', wx.OK|wx.ICON_INFORMATION)
            aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
            menssagError.ShowModal()
            menssagError.Destroy()
            self.Destroy()

        else:
            self.createPDF("EDP PDF - "+idt)

    #--------------------------------------------------
     def createPDF(self, name):
            idt = self.idt
            lista = self.list

            '''Obtendo os dados do banco'''
            listaCAB = bancodedadosCAB.ListaDadosCab(self.Id) #obtem o cabeçalho do pdf
            

            '''Obter dados do banco'''
            list = bancodedados.dados_iniciais_(idt) # obtem os dados do ensaio
            lvdt = bdConfiguration.S1S2()  #obtem dados dos sensores S1 e S2


            if int(list[12]) == 0:
                valoramostra = 'Deformada'
            else:
                valoramostra = 'Indeformada'
            try:
                desvioUmidade = str(float(list[4])-float(list[6]))
            except:
                desvioUmidade = ''

            '''Criando arquivo PDF'''
            with wx.FileDialog(self, name, wildcard="PDF files(*.pdf)|*.pdf*", style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return

                pathname = fileDialog.GetPath()

                try:
                    if re.search('\\.pdf\\b', pathname, re.IGNORECASE):
                        diretorio = pathname
                    else:
                        diretorio = pathname+".pdf"

                    cnv = canvas.Canvas(diretorio, pagesize=A4)
                    cnv.setTitle(idt)

                    #CABEÇALHO
                    try:
                        cnv.drawImage(listaCAB[12], pm(15), pm(252), width = 95, height = 95)
                    except:
                        pass
                    cnv.setFont("Helvetica-Bold", 16)
                    cnv.drawCentredString(pm(125), pm(280.5), listaCAB[1])
                    cnv.setFont("Helvetica-Bold", 14)
                    cnv.drawCentredString(pm(125), pm(274), listaCAB[0])
                    cnv.setFont("Helvetica", 11)
                    cnv.drawCentredString(pm(125), pm(269), listaCAB[8]+', '+listaCAB[9]+', '+listaCAB[7])
                    cnv.drawCentredString(pm(125), pm(264), listaCAB[11]+', '+listaCAB[6]+', '+listaCAB[5])
                    cnv.drawCentredString(pm(125), pm(259), listaCAB[10])
                    cnv.drawCentredString(pm(125), pm(254), listaCAB[2]+', '+listaCAB[4]+', '+listaCAB[3])

                    #CORPO
                    cnv.setFont("Helvetica-Bold", 14)
                    cnv.drawCentredString(pm(110), pm(242), 'Relatório de Ensaio de Módulo de Resiliência')
                    cnv.setFont("Helvetica", 11)
                    x = -2
                    cnv.drawRightString(pm(110), pm(235+x), 'Identificação:')
                    cnv.drawRightString(pm(110), pm(230+x), 'Norma de referência:')
                    cnv.drawRightString(pm(110), pm(225+x), 'Coleta da amostra:')
                    cnv.drawRightString(pm(110), pm(220+x), 'Início do ensaio:')
                    cnv.drawRightString(pm(110), pm(215+x), 'Fim do ensaio:')
                    cnv.drawRightString(pm(110), pm(210+x), 'Identificação e natureza da amostra:')
                    cnv.drawRightString(pm(110), pm(205+x), 'Tipo de estabilizante químico:')
                    cnv.drawRightString(pm(110), pm(200+x), 'Tempo de cura [dias]:')
                    cnv.drawRightString(pm(110), pm(195+x), 'Peso do estabilizante químico [%]:')
                    cnv.drawRightString(pm(110), pm(190+x), 'Energia de compactação:')
                    cnv.drawRightString(pm(110), pm(185+x), 'Tamanho do Corpo de Prova [mm]:')
                    cnv.drawRightString(pm(110), pm(180+x), 'Teor de umidade do Corpo de Prova [%]:')
                    cnv.drawRightString(pm(110), pm(175+x), 'Peso específico seco do Corpo de Prova [kN/m³]:')
                    cnv.drawRightString(pm(110), pm(170+x), 'Grau de compactação do Corpo de Prova [%]:')
                    cnv.drawRightString(pm(110), pm(165+x), 'Desvio de umidade [%]:')
                    cnv.drawRightString(pm(110), pm(160+x), 'Frequência do ensaio [Hz]:')
                    cnv.drawRightString(pm(110), pm(155+x), 'Curso do LVDT empregado [mm]:')

                    cnv.drawString(pm(112), pm(235+x), idt)
                    cnv.drawString(pm(112), pm(230+x), 'DNIT 181/2018-ME')
                    cnv.drawString(pm(112), pm(225+x), list[9])
                    cnv.drawString(pm(112), pm(220+x), list[10])
                    cnv.drawString(pm(112), pm(215+x), list[11])
                    cnv.drawString(pm(112), pm(210+x), list[3])
                    cnv.drawString(pm(112), pm(205+x), list[19])
                    cnv.drawString(pm(112), pm(200+x), list[21])
                    cnv.drawString(pm(112), pm(195+x), list[20])
                    cnv.drawString(pm(112), pm(190+x), list[7])
                    cnv.drawString(pm(112), pm(185+x), str(format(list[13]).replace('.',','))+' x '+str(format(list[14]).replace('.',',')))
                    cnv.drawString(pm(112), pm(180+x), list[4])
                    cnv.drawString(pm(112), pm(175+x), list[5])
                    cnv.drawString(pm(112), pm(170+x), list[8])
                    cnv.drawString(pm(112), pm(165+x), desvioUmidade)
                    cnv.drawString(pm(112), pm(160+x), str(list[16]))
                    cnv.drawString(pm(112), pm(155+x), str(int(lvdt[3])))

                    #RODAPÉ
                    o = Paragraph('OBS.: '+list[15])
                    o.wrapOn(cnv, 250, 50)
                    o.drawOn(cnv, pm(32), pm(10))
                    cnv.line(pm(130),pm(18),pm(195),pm(18))
                    cnv.drawString(pm(130), pm(14), 'R. T.: '+list[22])
                    cnv.drawString(pm(130), pm(10), list[23]) 

                    #TABLE
                    t=Table(lista)
                    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('ALIGN',(0,0),(-1,-1),'CENTER'), ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

                    t.wrapOn(cnv, 720, 576)
                    t.drawOn(cnv, pm(60), pm((17-len(lista))*6.35+25))

                    cnv.save()
                    self.Destroy()
                    dlg = wx.MessageDialog(None, 'PDF gerado com sucesso', 'EDP', wx.OK|wx.CENTRE)#codigo para mostrar uma mensagem de confirmação quando o pdf for gerado
                    dlg.ShowModal()

                except:
                    wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                    dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()
                    self.Destroy()
                    return