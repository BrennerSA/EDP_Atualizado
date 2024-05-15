# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
import datetime
import banco.bancodedados as bancodedados
from front.TelaRealizacaoEnsaioDNIT135 import TelaRealizacaoEnsaioDNIT135

tipos = ['SIMPLES', 'COMPLETO']

class EditarDNIT135(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, idt,mainref, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - DNIT 135/2018ME - Editar', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.idt = idt
            self.mainref=mainref
            # self.Bind(wx.EVT_CLOSE, self.onExit)
            frame = self.basic_gui()
            

        
        #--------------------------------------------------
        def basic_gui(self):
            idt = self.idt

            self.list = bancodedados.dados_iniciais_(idt)

            self.DIAMETRO_MINIMO = 97.8
            self.DIAMETRO_MAXIMO =  105.4
            self.ALTURA_MINIMA = 35
            self.ALTURA_MAXIMA = 70
            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((600,500))
            window_sizer = wx.BoxSizer(wx.VERTICAL)
            principal_box = wx.BoxSizer(wx.VERTICAL)
            identificacao_box = wx.BoxSizer(wx.HORIZONTAL)
            natureza_amostra_box = wx.BoxSizer(wx.HORIZONTAL)
            resistencia_tracao_box = wx.BoxSizer(wx.HORIZONTAL)
            data_box = wx.BoxSizer(wx.HORIZONTAL)
            diametro_altura_box = wx.BoxSizer(wx.HORIZONTAL)
            nivel_tensao_box=wx.BoxSizer(wx.HORIZONTAL)
            observasoes_box = wx.BoxSizer(wx.HORIZONTAL)
            responsavel_formacao_box = wx.BoxSizer(wx.HORIZONTAL)
            extra_box=wx.BoxSizer(wx.HORIZONTAL)
            window = wx.Panel(self)

            #Titulo da tela
            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(window, label = "Editar Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            principal_box.Add(title, 1, wx.EXPAND | wx.ALL)


            
            # Adiciona Nome e Caixa de entrada da identificação
            identificacao_box.AddStretchSpacer(16)
            identificacao_text = wx.StaticText(window, label = "Identificação", style = wx.ALIGN_RIGHT)
            identificacao_box.Add(identificacao_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.identificador_text_input = wx.TextCtrl(window, -1, idt, style = wx.TE_RIGHT)
            self.identificador_text_input.SetMaxLength(15)
            self.identificador_text_input.Disable()
            identificacao_box.Add(self.identificador_text_input, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(identificacao_box, 1, wx.EXPAND | wx.ALL)



            # Adiciona Nome e Caixa de entrada da Responsavel Técnico
            responsavel_text = wx.StaticText(window, label = "Responsável Técnico", style = wx.ALIGN_RIGHT)
            responsavel_formacao_box.Add(responsavel_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.responsavel_tecnico_text_input = wx.TextCtrl(window, -1, self.list[22], style = wx.TE_RIGHT)
            self.responsavel_tecnico_text_input.SetMaxLength(30)
            self.responsavel_tecnico_text_input.Disable()
            responsavel_formacao_box.Add(self.responsavel_tecnico_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            # Adiciona Nome e Caixa de entrada da Formação/CREA
            formacao_text = wx.StaticText(window, label = "Formação/CREA", style = wx.ALIGN_RIGHT)
            responsavel_formacao_box.Add(formacao_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.formacao_text_input = wx.TextCtrl(window, -1, self.list[23], style = wx.TE_RIGHT)
            self.formacao_text_input.SetMaxLength(30)
            self.formacao_text_input.Disable()
            responsavel_formacao_box.Add(self.formacao_text_input, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(responsavel_formacao_box, 1, wx.EXPAND | wx.ALL)


            # Adiciona Nome e Caixa de entrada da Natureza da Amostra
            natureza_amostra_text = wx.StaticText(window, label = "Natureza da Amostra", style = wx.ALIGN_RIGHT)
            natureza_amostra_box.Add(natureza_amostra_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.natureza_amostra_text_input = wx.TextCtrl(window, -1, self.list[3], style = wx.TE_RIGHT)
            self.natureza_amostra_text_input.SetMaxLength(30)
            self.natureza_amostra_text_input.Disable()
            natureza_amostra_box.Add(self.natureza_amostra_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            principal_box.Add(natureza_amostra_box, 1, wx.EXPAND | wx.ALL)

            # Adiciona caixa do valor da resistencia à tração
            resistencia_tracao_box.AddStretchSpacer(16)
            resistencia_tracao_text = wx.StaticText(window, label = 'Resistencia à tração por compressão diametral média', style = wx.ALIGN_RIGHT)
            resistencia_tracao_box.Add(resistencia_tracao_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.resistencia_tracao_text_input = wx.TextCtrl(window, -1, self.list[24], style = wx.TE_RIGHT)
            self.resistencia_tracao_text_input.Disable()
            resistencia_tracao_box.Add(self.resistencia_tracao_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(resistencia_tracao_box, 1, wx.EXPAND | wx.ALL)


            # Adiciona Nome e Caixa de entrada da Data da coleta ou recebimento
            data_box.AddStretchSpacer(16)
            data_text = wx.StaticText(window, label = "Data da coleta ou recebimento", style = wx.ALIGN_RIGHT)
            dateC = datetime.datetime.strptime(self.list[9], '%d-%m-%Y')
            data_box.Add(data_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.data_text_input = wx.adv.DatePickerCtrl(window, id = wx.ID_ANY, dt = dateC, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            self.data_text_input.Disable()
            data_box.Add(self.data_text_input, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(data_box, 1, wx.EXPAND | wx.ALL)

            # Adiciona Nome e Caixa de entrada do DIametro
            diametro_text = wx.StaticText(window, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            diametro_altura_box.Add(diametro_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro_text_input = wx.TextCtrl(window, -1, str(self.list[13]), style = wx.TE_RIGHT)
            self.diametro_text_input.Disable()
            diametro_altura_box.Add(self.diametro_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            # Adiciona Nome e Caixa de entrada da Altura
            altura_text = wx.StaticText(window, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            diametro_altura_box.Add(altura_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura_text_input = wx.TextCtrl(window, -1, str(self.list[14]), style = wx.TE_RIGHT)
            self.altura_text_input.Disable()
            diametro_altura_box.Add(self.altura_text_input, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(diametro_altura_box, 1, wx.EXPAND | wx.ALL)


            # Adiciona nivel de tensão
            nivel_tensao_text = wx.StaticText(window, label = "Nivel de tensão %", style = wx.ALIGN_RIGHT)
            nivel_tensao_box.Add(nivel_tensao_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.tensao_input = wx.TextCtrl(window, -1, str(float(self.list[25])*100), style = wx.TE_RIGHT)
            self.tensao_input.Disable()
            nivel_tensao_box.Add(self.tensao_input, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(nivel_tensao_box, 1, wx.EXPAND | wx.ALL)



            
            # Adiciona Nome e Caixa de entrada da Observações
            observacoes_text = wx.StaticText(window, label = "Observações", style = wx.ALIGN_RIGHT)
            observasoes_box.Add(observacoes_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.observacoes_text_input = wx.TextCtrl(window, -1, self.list[15], style = wx.TE_RIGHT)
            self.observacoes_text_input.SetMaxLength(120)
            self.observacoes_text_input.Disable()
            observasoes_box.Add(self.observacoes_text_input, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            staticbox = wx.StaticBox(window, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)

            # LabelFadiga = wx.StaticText(window, label = "Fadiga", style = wx.ALIGN_RIGHT)
            # tipoAmostras = ['Modulo de Resiliencia', 'Fadiga']
            # self.amostra = wx.RadioBox(window, label = '', choices = tipoAmostras, majorDimension = 1, style = wx.RA_SPECIFY_COLS)
            # self.amostra.SetSelection(0)
            # self.amostra.Bind(wx.EVT_RADIOBOX, self.RadioBoxEvent)
            # principal_box.Add(LabelFadiga, 0, wx.ALL|wx.ALIGN_RIGHT)
            # principal_box.Add(self.amostra, 0, wx.ALL|wx.ALIGN_RIGHT)
            staticboxSizer.Add(principal_box, 0, wx.ALL|wx.CENTER)

            principal_box.Add(observasoes_box, 1, wx.EXPAND | wx.ALL)


           

            self.editar = wx.Button(window, -1, 'Editar')
            self.editar.Bind(wx.EVT_BUTTON, self.Editar)
            self.salvar = wx.Button(window, -1, 'Salvar')
            self.salvar.Bind(wx.EVT_BUTTON, self.Salvar)
            self.salvar.Disable()
            self.Ensaio = wx.Button(window, -1, 'Ensaio')
            self.Ensaio.Bind(wx.EVT_BUTTON, self.Prosseguir)
            
            if int(self.list[1]) != 0:
                self.Ensaio.Disable()

            extra_box.Add(self.editar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            extra_box.Add(self.salvar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            extra_box.Add(self.Ensaio, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            

            principal_box.Add(extra_box, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            window_sizer.Add(principal_box, 1,  wx.EXPAND | wx.ALL, 15)

            window.SetSizer(window_sizer)
            self.Centre()
            self.Show()

        def Prosseguir(self, event):
            identificador = self.identificador_text_input.GetValue()
            natureza_amostra = self.natureza_amostra_text_input.GetValue()
            tecnico = self.responsavel_tecnico_text_input.GetValue()
            formacao = self.formacao_text_input.GetValue()
            resistencia_tracao = self.resistencia_tracao_text_input.GetValue()
            resistencia_tracao=format(resistencia_tracao).replace(',','.')
            data = self.data_text_input.GetValue()
            diametro = self.diametro_text_input.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura_text_input.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.observacoes_text_input.GetValue()
            tensao=self.tensao_input.GetValue()
            tensao=format(tensao).replace(',','.')
            # fadiga = self.amostra.GetSelection()
            # self.Close()
            self.mainref.Hide()
            self.Hide()
            TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
            self.mainref.Show()
            self.Show()
            

        def Salvar(self, event):
            identificador = self.identificador_text_input.GetValue()
            natureza_amostra = self.natureza_amostra_text_input.GetValue()
            tecnico = self.responsavel_tecnico_text_input.GetValue()
            formacao = self.formacao_text_input.GetValue()
            resistencia_tracao = self.resistencia_tracao_text_input.GetValue()
            resistencia_tracao=format(resistencia_tracao).replace(',','.')
            data = self.data_text_input.GetValue()
            diametro = self.diametro_text_input.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura_text_input.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.observacoes_text_input.GetValue()
            tensao=self.tensao_input.GetValue()
            tensao=format(tensao).replace(',','.')
            # fadiga = self.amostra.GetSelection()
            

            try:
                diametro = float(diametro)
                altura = float(altura)
                tensao=float(tensao)/100
                resistencia_tracao=float(resistencia_tracao)

            except ValueError:
                # print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                return

            if identificador == '' or (tensao>0.25 or tensao<0.05):
                '''Diálogo para Forçar preenchimento da Identificacao'''
                dlg = wx.MessageDialog(None, 'É necessário que no mínimo a Indentificação seja preenchida.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                dlg.ShowModal()
            else:
                # Confere altura e diametro do corpo de prova pra ve se estão dentro do parametro da Norma
                if diametro>= self.DIAMETRO_MINIMO and diametro<=self.DIAMETRO_MAXIMO and altura>=self.ALTURA_MINIMA and altura<=self.ALTURA_MAXIMA:
                    '''Salva os dados iniciais de um ensaio'''
                    bancodedados.update_dados_135(identificador, natureza_amostra, tecnico,formacao, resistencia_tracao, data, diametro, altura, obs,tensao)
                    self.editar.Enable()
                    self.Ensaio.Enable()
                    self.salvar.Disable()
                    self.responsavel_tecnico_text_input.Disable()
                    self.formacao_text_input.Disable()
                    self.natureza_amostra_text_input.Disable()
                    self.resistencia_tracao_text_input.Disable()
                    self.data_text_input.Disable()
                    self.diametro_text_input.Disable()
                    self.altura_text_input.Disable()
                    self.tensao_input.Disable()
                    self.observacoes_text_input.Disable()
                else:
                    '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                    dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

        def Editar(self, event):
            self.editar.Disable()
            self.Ensaio.Disable()
            self.salvar.Enable()
            self.responsavel_tecnico_text_input.Enable()
            self.formacao_text_input.Enable()
            self.natureza_amostra_text_input.Enable()
            self.resistencia_tracao_text_input.Enable()
            self.data_text_input.Enable()
            self.diametro_text_input.Enable()
            self.altura_text_input.Enable()
            self.tensao_input.Enable()
            self.observacoes_text_input.Enable()

