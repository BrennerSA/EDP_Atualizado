# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
import banco.bancodedados as bancodedados
import banco.bdConfiguration as bdConfiguration
from front.TelaRealizacaoEnsaioDNIT135 import TelaRealizacaoEnsaioDNIT135
DIAMETRO_MINIMO = 97.8
DIAMETRO_MAXIMO =  105.4
ALTURA_MINIMA = 35
ALTURA_MAXIMA = 70
'''Tela Selecão de Ensaio'''
class TelaNovoEnsaioDNIT183(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, None, -1, 'EDP - DNIT 183/2018ME', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((600,520))
            window_sizer = wx.BoxSizer(wx.VERTICAL)
            principal_box = wx.BoxSizer(wx.VERTICAL)
            continuacao_box=wx.BoxSizer(wx.HORIZONTAL)
            extra_box=wx.BoxSizer(wx.HORIZONTAL)
            identificacao_box = wx.BoxSizer(wx.HORIZONTAL)
            natureza_amostra_box = wx.BoxSizer(wx.HORIZONTAL)
            resistencia_tracao_box = wx.BoxSizer(wx.HORIZONTAL)
            data_box = wx.BoxSizer(wx.HORIZONTAL)
            diametro_altura_box = wx.BoxSizer(wx.HORIZONTAL)
            observasoes_box = wx.BoxSizer(wx.HORIZONTAL)
            responsavel_formacao_box = wx.BoxSizer(wx.HORIZONTAL)
            mr_box=wx.BoxSizer(wx.HORIZONTAL)
            window = wx.Panel(self)

            #Titulo da tela
            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(window, label = "Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            principal_box.Add(title, 1, wx.EXPAND | wx.ALL)


            LabelContinuacao = wx.StaticText(window, label = "Continuação de ensaio anterior?", style = wx.ALIGN_RIGHT)
            tipoAmostras = ['Continuação', 'Nova Sequencia']
            self.escolha = wx.RadioBox(window, label = '', choices = tipoAmostras, majorDimension = 2, style = wx.RA_SPECIFY_COLS)
            self.escolha.Bind(wx.EVT_RADIOBOX, self.RadioBoxEvent)
            # self.continuacao = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            self.continuacao = wx.ComboBox(window, choices = bancodedados.dados_iniciais_183(str(183)), style = wx.ALL | wx.CB_READONLY)
            self.continuacao.Disable()
            continuacao_box.AddStretchSpacer(16)
            continuacao_box.Add(LabelContinuacao,12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            continuacao_box.Add(self.escolha, 0, wx.ALL|wx.CENTER)
            extra_box.Add(self.continuacao, wx.ALIGN_RIGHT | wx.ALL, 5)
            principal_box.Add(continuacao_box, 1, wx.ALIGN_RIGHT | wx.ALL)
            principal_box.Add(extra_box,1,wx.ALIGN_RIGHT)
            
            # Adiciona Nome e Caixa de entrada da identificação
            identificacao_box.AddStretchSpacer(16)
            identificacao_text = wx.StaticText(window, label = "Identificação", style = wx.ALIGN_RIGHT)
            identificacao_box.Add(identificacao_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.identificador_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            self.identificador_text_input.SetMaxLength(15)
            identificacao_box.Add(self.identificador_text_input, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(identificacao_box, 1, wx.EXPAND | wx.ALL)



            # Adiciona Nome e Caixa de entrada da Responsavel Técnico
            responsavel_text = wx.StaticText(window, label = "Responsável Técnico", style = wx.ALIGN_RIGHT)
            responsavel_formacao_box.Add(responsavel_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.responsavel_tecnico_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            self.responsavel_tecnico_text_input.SetMaxLength(30)
            responsavel_formacao_box.Add(self.responsavel_tecnico_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            # Adiciona Nome e Caixa de entrada da Formação/CREA
            formacao_text = wx.StaticText(window, label = "Formação/CREA", style = wx.ALIGN_RIGHT)
            responsavel_formacao_box.Add(formacao_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.formacao_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            self.formacao_text_input.SetMaxLength(30)
            responsavel_formacao_box.Add(self.formacao_text_input, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(responsavel_formacao_box, 1, wx.EXPAND | wx.ALL)


            # Adiciona Nome e Caixa de entrada da Natureza da Amostra
            natureza_amostra_text = wx.StaticText(window, label = "Natureza da Amostra", style = wx.ALIGN_RIGHT)
            natureza_amostra_box.Add(natureza_amostra_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.natureza_amostra_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            self.natureza_amostra_text_input.SetMaxLength(30)
            natureza_amostra_box.Add(self.natureza_amostra_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            principal_box.Add(natureza_amostra_box, 1, wx.EXPAND | wx.ALL)

            # Adiciona caixa do valor da resistencia à tração
            resistencia_tracao_box.AddStretchSpacer(16)
            resistencia_tracao_text = wx.StaticText(window, label = 'Resistencia à tração por compressão diametral média', style = wx.ALIGN_RIGHT)
            resistencia_tracao_box.Add(resistencia_tracao_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.resistencia_tracao_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            resistencia_tracao_box.Add(self.resistencia_tracao_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(resistencia_tracao_box, 1, wx.EXPAND | wx.ALL)


            # Adiciona Nome e Caixa de entrada da Data da coleta ou recebimento
            data_box.AddStretchSpacer(16)
            data_text = wx.StaticText(window, label = "Data da coleta ou recebimento", style = wx.ALIGN_RIGHT)
            data_box.Add(data_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.data_text_input = wx.adv.DatePickerCtrl(window, id = wx.ID_ANY, dt = wx.DefaultDateTime, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            data_box.Add(self.data_text_input, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(data_box, 1, wx.EXPAND | wx.ALL)

            # Adiciona Nome e Caixa de entrada do DIametro
            diametro_text = wx.StaticText(window, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            diametro_altura_box.Add(diametro_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            diametro_altura_box.Add(self.diametro_text_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            # Adiciona Nome e Caixa de entrada da Altura
            altura_text = wx.StaticText(window, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            diametro_altura_box.Add(altura_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            diametro_altura_box.Add(self.altura_text_input, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(diametro_altura_box, 1, wx.EXPAND | wx.ALL)

            # Adiciona Nome e Caixa de entrada da Observações
            observacoes_text = wx.StaticText(window, label = "Observações", style = wx.ALIGN_RIGHT)
            observasoes_box.Add(observacoes_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.observacoes_text_input = wx.TextCtrl(window, -1, '', style = wx.TE_RIGHT)
            self.observacoes_text_input.SetMaxLength(120)
            observasoes_box.Add(self.observacoes_text_input, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            staticbox = wx.StaticBox(window, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)

            LabelNivelTensao = wx.StaticText(window, label = "Nivel de Tensão (%)", style = wx.ALIGN_RIGHT)
            self.Pares = wx.ComboBox(window, choices = bdConfiguration.Tensao183(), style = wx.ALL | wx.CB_READONLY)
            self.Pares.SetSelection(0)
            
            self.escolha.SetSelection(1)
            self.continuacao.Disable()

            principal_box.Add(LabelNivelTensao, 0, wx.ALL|wx.ALIGN_RIGHT)
            principal_box.Add(self.Pares, 0, wx.ALL|wx.ALIGN_RIGHT)
            staticboxSizer.Add(principal_box, 0, wx.ALL|wx.CENTER)

            mr_text = wx.StaticText(window, label = "Modulo de Resiliencia (MPa)", style = wx.ALIGN_RIGHT)
            mr_box.Add(mr_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.mr_text_input = wx.TextCtrl(window, 10, '', style = wx.TE_RIGHT)
            mr_box.Add(self.mr_text_input, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(mr_box, 1, wx.EXPAND | wx.ALL)

            principal_box.Add(observasoes_box, 1, wx.EXPAND | wx.ALL)

            continuar = wx.Button(window, -1, 'Continuar')
            continuar.Bind(wx.EVT_BUTTON, self.Prosseguir)
            principal_box.Add(continuar, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            window_sizer.Add(principal_box, 1,  wx.EXPAND | wx.ALL, 15)

            self.identificador_text_input.AppendText("debug")
            self.resistencia_tracao_text_input.AppendText("1")
            self.diametro_text_input.AppendText("100")
            self.altura_text_input.AppendText("50")
            window.SetSizer(window_sizer)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def Prosseguir(self, event):
            identificador = self.identificador_text_input.GetValue()
            natureza_amostra = self.natureza_amostra_text_input.GetValue()
            tecnico = self.responsavel_tecnico_text_input.GetValue()
            formacao = self.formacao_text_input.GetValue()
            resistencia_tracao = self.resistencia_tracao_text_input.GetValue()
            data = self.data_text_input.GetValue()
            diametro = self.diametro_text_input.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura_text_input.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.observacoes_text_input.GetValue()
            tensao = self.Pares.GetValue()
            sequencia = self.continuacao.GetValue()
            amostra = self.escolha.GetSelection()
            mr =self.mr_text_input.GetValue()
            

            try:
                diametro = float(diametro)
                altura = float(altura)

            except ValueError:
                # print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                return

            if identificador == '':
                '''Diálogo para Forçar preenchimento da Identificacao'''
                dlg = wx.MessageDialog(None, 'É necessário que no mínimo a Indentificação seja preenchida.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                result = dlg.ShowModal()
            else:
                # Pega do banco de dados todos os identificadores já existentes
                # Confere se nome de identificador já foi utilizado
                if identificador in bancodedados.data_identificadores() or (amostra==0 and sequencia==''):
                    # Diálogo para informar que já existe um Ensaio com esse identificação
                    dlg = wx.MessageDialog(None, 'Já existe um Ensaio com essa Identificação.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    dlg.ShowModal()
                else:
                    # Confere altura e diametro do corpo de prova pra ve se estão dentro do parametro da Norma
                    if diametro>= DIAMETRO_MINIMO and diametro<=DIAMETRO_MAXIMO and altura>=ALTURA_MINIMA and altura<=ALTURA_MAXIMA:
                        '''Salva os dados iniciais de um ensaio'''
                        bancodedados.data_save_dados_183(identificador, natureza_amostra, tecnico,formacao, resistencia_tracao, data, diametro, altura, obs, tensao,sequencia,mr)
                        self.Close(True)
                        frame = TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
                    else:
                        '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                        dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                        result = dlg.ShowModal()

        def RadioBoxEvent(self, event):
            amostra = self.escolha.GetSelection()
            if amostra ==0:
                self.continuacao.Enable()
            else:
                self.continuacao.Disable()