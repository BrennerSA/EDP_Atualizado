# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import bancodedadosnovo
import bancodedadosCAB
import calculo
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import bdPreferences

'''Class Export PDF'''
class Pdf(wx.Dialog):
    #--------------------------------------------------
     def __init__(self, id, *args, **kwargs):
        wx.Dialog.__init__(self, None, -1, 'Software Marshall - PDF')
        self.id = id - 9000
        self.a = bancodedadosCAB.idEscolha()
        self.createPDF("Software Marshall - PDF")

    #--------------------------------------------------
     def createPDF(self, name):

        id = self.id

     	# '''Obtendo os dados do banco'''
        dados_ensaio = bancodedadosnovo.get_dadosEnsaio(self.id)
        self.norma = dados_ensaio[0][1].encode('utf-8','ignore')
        self.rodovia = dados_ensaio[0][2].encode('utf-8','ignore')
        self.trecho = dados_ensaio[0][3].encode('utf-8','ignore')
        self.operador = dados_ensaio[0][4].encode('utf-8','ignore')
        self.cp = dados_ensaio[0][5].encode('utf-8','ignore')
        self.origem = dados_ensaio[0][6].encode('utf-8','ignore')
        self.est = dados_ensaio[0][7].encode('utf-8','ignore')
        self.interesse = dados_ensaio[0][8].encode('utf-8','ignore')
        self.obs = dados_ensaio[0][9].encode('utf-8','ignore')
        self.cteAnel = bdPreferences.getCteAnel()
        # '''Calculando parâmetros'''
        if(self.norma[8:-1] == '043/95' or self.norma[8:-1] == '107/94'):
            ensaio = 1
            dados_amostra = bancodedadosnovo.get_dadosAmostra(self.id)
            self.pesosub = dados_amostra[0][1]
            self.pesoar = dados_amostra[0][2]
            self.temp = dados_amostra[0][3]
            self.diametro = dados_amostra[0][4]
            self.altura = dados_amostra[0][5]
            self.asfalto = dados_amostra[0][6]
            self.densidade_teorica = dados_amostra[0][7]
            self.volume_vazios = dados_amostra[0][8]
            if(self.norma[8:-1] == '043/95'):
                valores_calculados = calculo.calcular_04395(self.pesosub, self.pesoar, self.temp, self.diametro, self.altura, self.asfalto, self.id)
            else:
                valores_calculados = calculo.calcular_10794(self.pesosub, self.pesoar, self.temp, self.diametro, self.altura, self.asfalto, self.id)
            self.volume = valores_calculados[0]
            self.densidade_aparente = valores_calculados[1]
            self.defAnel = 0
            self.carga = 0
            self.corr = 0
            self.estabilidade = valores_calculados[2]
            self.fluencia = valores_calculados[3]
            self.vv = 0
            self.vb = 0
            self.vam = 0
            self.vrbv = 0
        else:
            ensaio = 2
            dados_amostra = bancodedadosnovo.get_dadosAmostra(self.id)
            self.pesosub = dados_amostra[0][1]
            self.pesoar = dados_amostra[0][2]
            self.temp = dados_amostra[0][3]
            self.diametro = dados_amostra[0][4]
            self.altura = dados_amostra[0][5]
            self.asfalto = dados_amostra[0][6]
            valores_calculados = calculo.calcular_1362018(self.id, self.diametro, self.altura)
            forca = valores_calculados[0]
            resistecia_tracao_indireta = valores_calculados[1]
        
     	 
        ''' Data de emissão'''
        now = datetime.now()
        data = now.strftime("%d/%m/%Y")

        listaCAB = bancodedadosCAB.ListaDadosCab(self.a)
        instituicao = listaCAB[1].encode('utf-8','ignore')
        fantasia = listaCAB[2].encode('utf-8','ignore')
        cpfcnpj = listaCAB[3].encode('utf-8','ignore')
        email = listaCAB[4].encode('utf-8','ignore')
        fone = listaCAB[5].encode('utf-8','ignore')
        uf = listaCAB[6].encode('utf-8','ignore')
        cidade = listaCAB[7].encode('utf-8','ignore')
        bairro = listaCAB[8].encode('utf-8','ignore')
        rua = listaCAB[9].encode('utf-8','ignore')
        numero = listaCAB[10].encode('utf-8','ignore')
        complemento = listaCAB[11].encode('utf-8','ignore')
        cep = listaCAB[12].encode('utf-8','ignore')
        logo = listaCAB[13].encode('utf-8','ignore')

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
                try:
                    cnv.drawImage("logo\UFRB.jpg", 13/0.352777, 257/0.352777, width = 95, height = 95)
                    cnv.drawImage("logo\LogoLabPav.jpeg", 155/0.352777, 265/0.352777, width = 95, height = 40)
                except:
                    pass

                def createTable(posx, posy, linhas, colunas, alturalinha, larguracoluna):
                    vetorLinhas = []
                    for i in range(0,linhas+1):
                        vetorLinhas.append(posy-(alturalinha*i))
                    vetorColunas = []
                    for i in range(0,colunas+1):
                        vetorColunas.append(posx+(larguracoluna*i))
                    cnv.grid(vetorColunas,vetorLinhas)

                def leituras():
                    k = 0.352777
                    dados_coleta = bancodedadosnovo.get_leituraEnsaio(self.id)
                    dados_tratados = calculo.pos_curva(self.id, ensaio)
                    deformacao = []
                    estabilidade = []
                    for i in range((len(dados_tratados))):
                        if(dados_tratados[i][0] > 0):
                            deformacao.append(dados_tratados[i][0])
                            estabilidade.append(dados_tratados[i][1])
                    passo = int(round((len(deformacao)/90))+1)
                    contador = -1
                    j = 0
                    for i in range(0,len(deformacao),passo):
                        contador+=1
                        if(contador <= 17):
                            cnv.drawString(15.5/k + j*36.5/k, 124/k - contador*4.31/k, str(format(round(deformacao[i],3)).replace('.',',')))
                            cnv.drawString(30.5/k + j*36.5/k, 124/k - contador*4.31/k, str(format(round(estabilidade[i],3)).replace('.',',')))
                        else:
                            j+=1
                            contador = -1
                k = 0.352777
                cnv.setLineWidth(0.4)
                cnv.setFont("Helvetica-Bold", 11)
                cnv.drawCentredString(100/0.352777, 280.5/0.352777, fantasia)
                cnv.drawCentredString(100/0.352777, 270.5/0.352777, instituicao)
                cnv.setFont("Helvetica", 11)
                cnv.drawCentredString(100/0.352777, 260.5/0.352777, "Ensaio Marshall - " + self.norma)
                cnv.rect(15.5/k,244.2/k,176/k,5/k)
                cnv.setFillColor(colors.black)
                cnv.setFont("Helvetica-Bold", 11)
                cnv.drawCentredString(100/k,245/k, "Ensaio Marshall - " + self.norma)
                cnv.setFont("Helvetica", 11)
                createTable(15.5/k,244.2/k,3,1,7/k,22/k)
                createTable(37.5/k,244.2/k,3,1,7/k,66/k)
                createTable(103.5/k,244.2/k,3,1,7/k,22/k)
                createTable(125.5/k,244.2/k,3,1,7/k,66/k)
                createTable(15.5/k,223.2/k,1,1,7/k,176/k)
                cnv.drawString(16/k,239/k, "Operador:")
                cnv.drawString(38/k,239/k, self.operador)
                cnv.drawString(104/k,239/k, "Emissão:")
                cnv.drawString(126/k,239/k, data)
                cnv.drawString(16/k,232/k, "Rodovia:")
                cnv.drawString(38/k,232/k, self.rodovia)
                cnv.drawString(104/k,232/k, "Trecho:")
                cnv.drawString(126/k,232/k, self.trecho)
                cnv.drawString(16/k,225/k, "Origem:")
                cnv.drawString(38/k,225/k, self.origem)
                cnv.drawString(104/k,225/k, "Est/km:")
                cnv.drawString(126/k,225/k, self.est)
                cnv.drawString(16/k,218/k, "Interesse:")
                cnv.drawString(40/k,218/k, self.interesse)

                if(self.norma[8:-1] == '043/95' or self.norma[8:-1] == '107/94'):

                    createTable(15.5/k,208/k,11,1,6/k,38/k)
                    createTable(53.5/k,208/k,11,1,6/k,22/k)
                    a = 6
                    b = 204
                    c = 55
                    cnv.drawString(16/k,(b - 0*a)/k, "Teor de Asfalto(%)")
                    cnv.drawString(c/k,(b - 0*a)/k, str(format(round(self.asfalto,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 1*a)/k, "Número do CP")
                    cnv.drawString(c/k,(b - 1*a)/k, str(self.cp))
                    cnv.drawString(16/k,(b - 2*a)/k, "Peso ao ar(g)")
                    cnv.drawString(c/k,(b - 2*a)/k, str(format(round(self.pesoar,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 3*a)/k, "Peso Imerso(mm)")
                    cnv.drawString(c/k,(b - 3*a)/k, str(format(round(self.pesosub,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 4*a)/k, "Altura média(mm)")
                    cnv.drawString(c/k,(b - 4*a)/k, str(format(round(self.altura,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 5*a)/k, "Diâmetro médio(mm)")
                    cnv.drawString(c/k,(b - 5*a)/k, str(format(round(self.diametro,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 6*a)/k, "DMT(g/cm³)")
                    cnv.drawString(c/k,(b - 6*a)/k, str(format(round(self.densidade_teorica,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 7*a)/k, "Vv(%)")
                    cnv.drawString(c/k,(b - 7*a)/k, str(format(round(self.volume_vazios,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 8*a)/k, "Cte. do anel(kgf/mm)")
                    cnv.drawString(c/k,(b - 8*a)/k, str(format(round(self.cteAnel[0],3)).replace('.',',')))
                    cnv.setFont("Helvetica-Bold", 10)
                    cnv.drawString(16/k,(b - 9*a)/k, "Fluência(mm)")
                    cnv.drawString(c/k,(b - 9*a)/k, str(format(round(self.fluencia,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 10*a)/k, "Estab. (kgf)")
                    cnv.drawString(c/k,(b - 10*a)/k, str(format(round(self.estabilidade,3)).replace('.',',')))
                    cnv.setFont("Helvetica", 10)
                    for i in range(0,5):
                        cnv.setFillGray(0.5)
                        cnv.rect(15.5/k + i*36.5/k, 128/k, 15/k, 4.31/k, fill=1)
                        cnv.rect(30.5/k + i*36.5/k, 128/k, 15/k, 4.31/k, fill=1)
                        cnv.setFillColor(colors.black)
                        createTable(15.5/k + i*36.5/k,128/k,18,2,4.31/k,15/k)
                        cnv.drawString(18/k + i*36.5/k,129.5/k, "Desl.")
                        cnv.drawString(33/k + i*36.5/k,129.5/k, "Força")
                    leituras()
                    cnv.drawString(16/k,41/k, "_________________________________________________________________________________________")
                    cnv.setFont("Helvetica-Bold", 10)
                    cnv.drawString(16/k,36/k, "Observações:")
                    cnv.setFont("Helvetica", 10)
                    cnv.drawString(18/k,31/k, self.obs)
                    cnv.drawString(16/k,21/k, "_________________________________________________________________________________________")
                    cnv.drawString(70/k,6/k, "__________________________________________")
                    cnv.drawString(85/k,1/k, "                Responsável               ")
                    cnv.drawImage('graficos\E'+str(id)+'.png', 84/0.352777, 135/0.352777, width = 335, height = 220)
                else:
                    createTable(15.5/k,194/k,8,1,6/k,38/k)
                    createTable(53.5/k,194/k,8,1,6/k,22/k)
                    a = 6
                    b = 190
                    c = 55
                    cnv.drawString(16/k,(b - 0*a)/k, "Teor de Asfalto(%)")
                    cnv.drawString(c/k,(b - 0*a)/k, str(format(round(self.asfalto,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 1*a)/k, "Número do CP")
                    cnv.drawString(c/k,(b - 1*a)/k, str(self.cp))
                    cnv.drawString(16/k,(b - 2*a)/k, "Peso ao ar(g)")
                    cnv.drawString(c/k,(b - 2*a)/k, str(format(round(self.pesoar,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 3*a)/k, "Altura média(mm)")
                    cnv.drawString(c/k,(b - 3*a)/k, str(format(round(self.altura,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 4*a)/k, "Diâmetro médio(mm)")
                    cnv.drawString(c/k,(b - 4*a)/k, str(format(round(self.diametro,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 5*a)/k, "Cte. do anel(kgf/mm)")
                    cnv.drawString(c/k,(b - 5*a)/k, str(format(round(self.cteAnel[0],3)).replace('.',',')))
                    cnv.setFont("Helvetica-Bold", 10)
                    cnv.drawString(16/k,(b - 6*a)/k, "Rompimento(kgf)")
                    cnv.drawString(c/k,(b - 6*a)/k, str(format(round(forca,3)).replace('.',',')))
                    cnv.drawString(16/k,(b - 7*a)/k, "Res. Trac. Ind. (MPa)")
                    cnv.drawString(c/k,(b - 7*a)/k, str(format(round(resistecia_tracao_indireta,3)).replace('.',',')))
                    cnv.setFont("Helvetica", 10)
                    for i in range(0,5):
                        cnv.setFillGray(0.5)
                        cnv.rect(15.5/k + i*36.5/k, 128/k, 15/k, 4.31/k, fill=1)
                        cnv.rect(30.5/k + i*36.5/k, 128/k, 15/k, 4.31/k, fill=1)
                        cnv.setFillColor(colors.black)
                        createTable(15.5/k + i*36.5/k,128/k,18,2,4.31/k,15/k)
                        cnv.drawString(18/k + i*36.5/k,129.5/k, "Desl.")
                        cnv.drawString(33/k + i*36.5/k,129.5/k, "Força")
                    leituras()
                    cnv.drawString(16/k,41/k, "_________________________________________________________________________________________")
                    cnv.setFont("Helvetica-Bold", 10)
                    cnv.drawString(16/k,36/k, "Observações:")
                    cnv.setFont("Helvetica", 10)
                    cnv.drawString(18/k,31/k, self.obs)
                    cnv.drawString(16/k,21/k, "_________________________________________________________________________________________")
                    cnv.drawString(70/k,6/k, "__________________________________________")
                    cnv.drawString(85/k,1/k, "                Responsável               ")
                    cnv.drawImage('graficos\E'+str(id)+'.png', 84/0.352777, 135/0.352777, width = 335, height = 220)
                cnv.save()
                self.Destroy()

            except (RuntimeError, TypeError, NameError):
                wx.LogError("O arquivo nao pode ser salvo em '%s'." % pathname)
                dlg = wx.MessageDialog(None, 'Erro ao criar PDF', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
                print(RuntimeError)
                self.Destroy()
                return
