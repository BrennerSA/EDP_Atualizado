# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
import wx.adv
import datetime
import banco.bancodedados as bancodedados
import banco.bdPreferences as bdPreferences
import banco.bdConfiguration as bdConfiguration
import back.HexForRGB as HexRGB
# from front.TelaRealizacaoEnsaioDNIT134 import TelaRealizacaoEnsaioDNIT134
# from front.TelaRealizacaoEnsaioDNIT179 import TelaRealizacaoEnsaioDNIT179
# from front.TelaRealizacaoEnsaioDNIT181 import TelaRealizacaoEnsaioDNIT181
from front.TelaRealizacaoEnsaioDNIT135 import TelaRealizacaoEnsaioDNIT135

tipos = ['SIMPLES', 'COMPLETO']

'''Tela Editar Ensaio DNIT134'''
class EditarDNIT134(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, idt, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - DNIT 134/2018ME - Editar', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.idt = idt
            self.Bind(wx.EVT_CLOSE, self.onExit)
            frame = self.basic_gui()

        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()

        #--------------------------------------------------
        def basic_gui(self):
            idt = self.idt

            self.list = bancodedados.dados_iniciais_(idt)

            colors = bdPreferences.ListColors()
            colorBackground = colors[2]

            self.SetBackgroundColour(colorBackground)

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((600,410))
            sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v2_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "Editar Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL)

            LabelIdt = wx.StaticText(panel, label = "Identificação", style = wx.ALIGN_RIGHT)
            h_sizer.Add(LabelIdt, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(panel, -1, idt, style = wx.TE_RIGHT)
            self.Identificador.SetMaxLength(15)
            self.Identificador.Disable()
            h_sizer.Add(self.Identificador, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            LablelTipoEnsaio = wx.StaticText(panel, label = "Tipo de Ensaio", style = wx.ALIGN_RIGHT)
            h_sizer.Add(LablelTipoEnsaio, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Tipo = wx.ComboBox(panel, choices = tipos, style = wx.ALL | wx.CB_READONLY)
            self.Tipo.SetSelection(0)
            self.Tipo.Disable()
            h_sizer.Add(self.Tipo, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL)

            LabelResponsavelTecnico = wx.StaticText(panel, label = "Responsável Técnico", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(LabelResponsavelTecnico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.responsavel = wx.TextCtrl(panel, -1, self.list[22], style = wx.TE_RIGHT)
            self.responsavel.SetMaxLength(30)
            self.responsavel.Disable()
            h10_sizer.Add(self.responsavel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            LabelFormCrea = wx.StaticText(panel, label = "Formação/CREA", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(LabelFormCrea, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.formacao = wx.TextCtrl(panel, -1, self.list[23], style = wx.TE_RIGHT)
            self.formacao.SetMaxLength(30)
            self.formacao.Disable()
            h10_sizer.Add(self.formacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h10_sizer, 1, wx.EXPAND | wx.ALL)

            LabelNatAmostra = wx.StaticText(panel, label = "Natureza da Amostra", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(LabelNatAmostra, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cp = wx.TextCtrl(panel, -1, self.list[3], style = wx.TE_RIGHT)
            self.cp.SetMaxLength(30)
            self.cp.Disable()
            h1_sizer.Add(self.cp, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            LabelTeorUmi = wx.StaticText(panel, label = "Teor de Umidade (%)", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(LabelTeorUmi, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.teordeumidade = wx.TextCtrl(panel, -1, self.list[4], style = wx.TE_RIGHT)
            self.teordeumidade.SetMaxLength(5)
            self.teordeumidade.Disable()
            h1_sizer.Add(self.teordeumidade, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h1_sizer, 1, wx.EXPAND | wx.ALL)

            LabelPesoEspecifico = wx.StaticText(panel, label = "Peso específico seco (kN/m³)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(LabelPesoEspecifico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.pesoespecifico = wx.TextCtrl(panel, -1, self.list[5], style = wx.TE_RIGHT)
            self.pesoespecifico.SetMaxLength(5)
            self.pesoespecifico.Disable()
            h2_sizer.Add(self.pesoespecifico, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            LabelUmidadeOtima = wx.StaticText(panel, label = "Umidade Ótima (%)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(LabelUmidadeOtima, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.umidadeotima = wx.TextCtrl(panel, -1, self.list[6], style = wx.TE_RIGHT)
            self.umidadeotima.SetMaxLength(5)
            self.umidadeotima.Disable()
            h2_sizer.Add(self.umidadeotima, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h2_sizer, 1, wx.EXPAND | wx.ALL)

            LabelEnergCompact = wx.StaticText(panel, label = "Energia de compactação", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(LabelEnergCompact, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.energiacompactacao = wx.TextCtrl(panel, -1, self.list[7], style = wx.TE_RIGHT)
            self.energiacompactacao.SetMaxLength(30)
            self.energiacompactacao.Disable()
            h3_sizer.Add(self.energiacompactacao, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            
            LabelGrauCompact = wx.StaticText(panel, label = "Grau de compactação (%)", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(LabelGrauCompact, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.graucompactacao = wx.TextCtrl(panel, -1, self.list[8], style = wx.TE_RIGHT)
            self.graucompactacao.SetMaxLength(5)
            self.graucompactacao.Disable()
            h3_sizer.Add(self.graucompactacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h3_sizer, 1, wx.EXPAND | wx.ALL)

            LabelDataColeta = wx.StaticText(panel, label = "Data da coleta ou recebimento", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(LabelDataColeta, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            dateC = datetime.datetime.strptime(self.list[9], '%d-%m-%Y')
            self.date = wx.adv.DatePickerCtrl(panel, id = wx.ID_ANY, dt = dateC, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            self.date.Disable()
            h4_sizer.Add(self.date, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h4_sizer, 1, wx.EXPAND | wx.ALL)
            
            LabelDiametroCP = wx.StaticText(panel, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(LabelDiametroCP, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro = wx.TextCtrl(panel, -1, str(self.list[13]), style = wx.TE_RIGHT | wx.TE_READONLY)
            self.diametro.Disable()
            h5_sizer.Add(self.diametro, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h5_sizer, 1, wx.EXPAND | wx.ALL)
            
            LabelAlturaCP = wx.StaticText(panel, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(LabelAlturaCP, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura = wx.TextCtrl(panel, -1, str(self.list[14]), style = wx.TE_RIGHT | wx.TE_READONLY)
            self.altura.Disable()
            h6_sizer.Add(self.altura, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h6_sizer, 1, wx.EXPAND | wx.ALL)

            staticbox = wx.StaticBox(panel, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
            
            LabelTipoAmostra = wx.StaticText(panel, label = "Tipo da Amostra", style = wx.ALIGN_RIGHT)
            tipoAmostras = ['Deformada', 'Indeformada']
            self.amostra = wx.RadioBox(panel, label = '', choices = tipoAmostras, majorDimension = 1, style = wx.RA_SPECIFY_COLS)
            self.amostra.SetSelection(int(self.list[12]))
            self.amostra.Disable()
            self.amostra.Bind(wx.EVT_RADIOBOX, self.RadioBoxEvent)
            v2_sizer.Add(LabelTipoAmostra, 0, wx.ALL|wx.CENTER)
            v2_sizer.Add(self.amostra, 0, wx.ALL|wx.CENTER)
            staticboxSizer.Add(v2_sizer, 0, wx.ALL|wx.CENTER)

            h7_sizer.AddStretchSpacer(2)
            h7_sizer.Add(staticboxSizer, 1, wx.EXPAND | wx.ALL, 1)
            h7_sizer.AddStretchSpacer(1)
            h7_sizer.Add(v1_sizer, 5, wx.EXPAND | wx.ALL)

            v_sizer.Add(h7_sizer, 3, wx.EXPAND | wx.ALL)

            LabelObserv = wx.StaticText(panel, label = "Observações", style = wx.ALIGN_RIGHT)
            h9_sizer.Add(LabelObserv, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.obs = wx.TextCtrl(panel, -1, self.list[15], style = wx.TE_RIGHT)
            self.obs.Disable()
            self.obs.SetMaxLength(120)
            h9_sizer.Add(self.obs, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h9_sizer, 1, wx.EXPAND | wx.ALL)

            self.editar = wx.Button(panel, -1, 'Editar')
            self.editar.Bind(wx.EVT_BUTTON, self.Editar)
            self.salvar = wx.Button(panel, -1, 'Salvar')
            self.salvar.Bind(wx.EVT_BUTTON, self.Salvar)
            self.salvar.Disable()
            self.Ensaio = wx.Button(panel, -1, 'Ensaio')
            self.Ensaio.Bind(wx.EVT_BUTTON, self.Prosseguir)
            
            if int(self.list[1]) != 0:
                self.Ensaio.Disable()

            h11_sizer.Add(self.editar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            h11_sizer.Add(self.salvar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            h11_sizer.Add(self.Ensaio, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            v_sizer.Add(h11_sizer, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            sizer.Add(v_sizer, 1,  wx.EXPAND | wx.ALL, 15)

            panel.SetSizer(sizer)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def RadioBoxEvent(self, event):
            amostra = self.amostra.GetSelection()
            if amostra == 1:
                self.diametro.Clear()
                self.altura.Clear()
                self.diametro.SetEditable(True)
                self.altura.SetEditable(True)
            elif amostra == 0:
                self.diametro.Clear()
                self.altura.Clear()
                self.diametro.AppendText("100")
                self.altura.AppendText("200")
                self.diametro.SetEditable(False)
                self.altura.SetEditable(False)
    #--------------------------------------------------
        def Editar(self, event):
            self.editar.Disable()
            self.Ensaio.Disable()
            self.salvar.Enable()
            if int(self.list[1]) == 0:
                self.Tipo.Enable()
                self.amostra.Enable()
                self.diametro.Enable()
                self.altura.Enable()
            self.cp.Enable()
            self.responsavel.Enable()
            self.formacao.Enable()
            self.teordeumidade.Enable()
            self.pesoespecifico.Enable()
            self.umidadeotima.Enable()
            self.energiacompactacao.Enable()
            self.graucompactacao.Enable()
            self.date.Enable()
            self.obs.Enable()

    #--------------------------------------------------
        def Prosseguir(self, event):
            identificador = self.Identificador.GetValue()
            tipo = self.Tipo.GetSelection()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            diametro = float(diametro)
            altura = float(altura)
            self.Close(True)
            if tipo == 0:
                tipoE = True
            elif tipo == 1:
                tipoE = False
            TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
            # frame = TelaRealizacaoEnsaioDNIT134(identificador, tipoE, diametro, altura).ShowModal()

    #--------------------------------------------------
        def Salvar(self, event):
            identificador = self.Identificador.GetValue()
            tipo = self.Tipo.GetSelection()
            cp = self.cp.GetValue()
            tecnico = self.responsavel.GetValue()
            formacao = self.formacao.GetValue()
            teordeumidade = self.teordeumidade.GetValue()
            pesoespecifico = self.pesoespecifico.GetValue()
            umidadeotima = self.umidadeotima.GetValue()
            energiacompactacao = self.energiacompactacao.GetValue()
            graucompactacao = self.graucompactacao.GetValue()
            data = self.date.GetValue()
            amostra = self.amostra.GetSelection()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.obs.GetValue()
            condicional = 1

            try:
                diametro = float(diametro)
                altura = float(altura)

            except ValueError:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                diametro = -1
                condicional = -1

            if diametro!='' and altura!='' and diametro>=95 and diametro<=155 and altura>=190 and altura<=310:
                '''Atualiza os dados iniciais de um ensaio'''
                bancodedados.update_dados_134(identificador, tipo, cp, teordeumidade, pesoespecifico, umidadeotima, energiacompactacao, graucompactacao, data, amostra, diametro, altura, obs, tecnico, formacao)
                if int(self.list[1]) == 0:
                    self.Ensaio.Enable()
                self.editar.Enable()
                self.salvar.Disable()
                self.Tipo.Disable()
                self.amostra.Disable()
                self.diametro.Disable()
                self.altura.Disable()
                self.cp.Disable()
                self.responsavel.Disable()
                self.formacao.Disable()
                self.teordeumidade.Disable()
                self.pesoespecifico.Disable()
                self.umidadeotima.Disable()
                self.energiacompactacao.Disable()
                self.graucompactacao.Disable()
                self.date.Disable()
                self.obs.Disable()
            else:
                '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                if condicional>0:
                    dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()


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


class EditarDNIT183(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, idt, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - DNIT 135/2018ME - Editar', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.idt = idt
            self.Bind(wx.EVT_CLOSE, self.onExit)
            frame = self.basic_gui()
            

        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()

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
            botoes_box=wx.BoxSizer(wx.HORIZONTAL)
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
            self.escolha.Disable()
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
            data_box.Add(data_text, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            dateC = datetime.datetime.strptime(self.list[9], '%d-%m-%Y')
            self.data_text_input = wx.adv.DatePickerCtrl(window, id = wx.ID_ANY, dt = dateC, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
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

            # Adiciona Nome e Caixa de entrada da Observações
            observacoes_text = wx.StaticText(window, label = "Observações", style = wx.ALIGN_RIGHT)
            observasoes_box.Add(observacoes_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.observacoes_text_input = wx.TextCtrl(window, -1, self.list[15], style = wx.TE_RIGHT)
            self.observacoes_text_input.SetMaxLength(120)
            self.observacoes_text_input.Disable()
            observasoes_box.Add(self.observacoes_text_input, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            staticbox = wx.StaticBox(window, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)

            LabelNivelTensao = wx.StaticText(window, label = "Nivel de Tensão", style = wx.ALIGN_RIGHT)
            self.Pares = wx.ComboBox(window, choices = bdConfiguration.Tensao183(), style = wx.ALL | wx.CB_READONLY)
            self.Pares.SetSelection(0)
            self.Pares.Disable()
            
            self.escolha.SetSelection(1)
            self.continuacao.Disable()

            principal_box.Add(LabelNivelTensao, 0, wx.ALL|wx.ALIGN_RIGHT)
            principal_box.Add(self.Pares, 0, wx.ALL|wx.ALIGN_RIGHT)
            staticboxSizer.Add(principal_box, 0, wx.ALL|wx.CENTER)

            mr_text = wx.StaticText(window, label = "Modulo de Resiliencia (MPa)", style = wx.ALIGN_RIGHT)
            mr_box.Add(mr_text, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.mr_text_input = wx.TextCtrl(window, 10, self.list[27], style = wx.TE_RIGHT)
            self.mr_text_input.Disable()
            mr_box.Add(self.mr_text_input, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            principal_box.Add(mr_box, 1, wx.EXPAND | wx.ALL)

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

            botoes_box.Add(self.editar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            botoes_box.Add(self.salvar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            botoes_box.Add(self.Ensaio, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            principal_box.Add(botoes_box, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            window_sizer.Add(principal_box, 1,  wx.EXPAND | wx.ALL, 15)

            window.SetSizer(window_sizer)
            self.Centre()
            self.Show()
        
        def RadioBoxEvent(self, event):
            amostra = self.escolha.GetSelection()
            if amostra ==0:
                self.continuacao.Enable()
            else:
                self.continuacao.Disable()

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
            self.Pares.Enable()
            self.observacoes_text_input.Enable()
            self.escolha.Enable()
            self.mr_text_input.Enable()

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
            TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()

        def Salvar(self, event):
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
                # Confere altura e diametro do corpo de prova pra ve se estão dentro do parametro da Norma
                if diametro>= self.DIAMETRO_MINIMO and diametro<=self.DIAMETRO_MAXIMO and altura>=self.ALTURA_MINIMA and altura<=self.ALTURA_MAXIMA:
                    '''Salva os dados iniciais de um ensaio'''
                    bancodedados.update_dados_183(identificador, natureza_amostra, tecnico,formacao, resistencia_tracao, data, diametro, altura, obs, tensao,sequencia,mr)
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
                    self.Pares.Disable()
                    self.observacoes_text_input.Disable()
                    self.escolha.Disable()
                    self.mr_text_input.Disable()
                else:
                    '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                    dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()







'''Tela Editar Ensaio DNIT179'''
class EditarDNIT179(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, idt, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - DNIT 179/2018IE - Editar', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.idt = idt
            self.Bind(wx.EVT_CLOSE, self.onExit)
            frame = self.basic_gui()

        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()

        #--------------------------------------------------
        def basic_gui(self):
            idt = self.idt

            self.list = bancodedados.dados_iniciais_(idt)
            #print self.list

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((600,410))
            sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v2_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "Editar Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL)

            LabelIdt = wx.StaticText(panel, label = "Identificação", style = wx.ALIGN_RIGHT)
            h_sizer.Add(LabelIdt, 96, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(panel, -1, idt, style = wx.TE_RIGHT)
            self.Identificador.SetMaxLength(15)
            self.Identificador.Disable()
            h_sizer.Add(self.Identificador, 32, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LablelParesTensao = wx.StaticText(panel, label = "Pares de Tensão (MPa)", style = wx.ALIGN_RIGHT)
            h_sizer.Add(LablelParesTensao, 83, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Pares = wx.ComboBox(panel, choices = bdConfiguration.Pares_Tensoes(), style = wx.ALL | wx.CB_READONLY)
            self.Pares.SetSelection(int(self.list[2]))
            self.Pares.Disable()
            h_sizer.Add(self.Pares, 60, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL)

            LabelResponsavelTecnico = wx.StaticText(panel, label = "Responsável Técnico", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(LabelResponsavelTecnico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.responsavel = wx.TextCtrl(panel, -1, self.list[22], style = wx.TE_RIGHT)
            self.responsavel.SetMaxLength(30)
            self.responsavel.Disable()
            h10_sizer.Add(self.responsavel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelFormCrea = wx.StaticText(panel, label = "Formação/CREA", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(LabelFormCrea, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.formacao = wx.TextCtrl(panel, -1, self.list[23], style = wx.TE_RIGHT)
            self.formacao.SetMaxLength(30)
            self.formacao.Disable()
            h10_sizer.Add(self.formacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h10_sizer, 1, wx.EXPAND | wx.ALL)

            LabelNatAmostra = wx.StaticText(panel, label = "Natureza da Amostra", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(LabelNatAmostra, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cp = wx.TextCtrl(panel, -1, self.list[3], style = wx.TE_RIGHT)
            self.cp.SetMaxLength(30)
            self.cp.Disable()
            h1_sizer.Add(self.cp, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelTeorUmi = wx.StaticText(panel, label = "Teor de Umidade (%)", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(LabelTeorUmi, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.teordeumidade = wx.TextCtrl(panel, -1, self.list[4], style = wx.TE_RIGHT)
            self.teordeumidade.SetMaxLength(5)
            self.teordeumidade.Disable()
            h1_sizer.Add(self.teordeumidade, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h1_sizer, 1, wx.EXPAND | wx.ALL)

            LabelPesoEspecifico = wx.StaticText(panel, label = "Peso específico seco (kN/m³)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(LabelPesoEspecifico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.pesoespecifico = wx.TextCtrl(panel, -1, self.list[5], style = wx.TE_RIGHT)
            self.pesoespecifico.SetMaxLength(5)
            self.pesoespecifico.Disable()
            h2_sizer.Add(self.pesoespecifico, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelUmidadeOtima = wx.StaticText(panel, label = "Umidade Ótima (%)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(LabelUmidadeOtima, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.umidadeotima = wx.TextCtrl(panel, -1, self.list[6], style = wx.TE_RIGHT)
            self.umidadeotima.SetMaxLength(5)
            self.umidadeotima.Disable()
            h2_sizer.Add(self.umidadeotima, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h2_sizer, 1, wx.EXPAND | wx.ALL)

            LabelEnergCompact = wx.StaticText(panel, label = "Energia de compactação", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(LabelEnergCompact, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.energiacompactacao = wx.TextCtrl(panel, -1, self.list[7], style = wx.TE_RIGHT)
            self.energiacompactacao.SetMaxLength(30)
            self.energiacompactacao.Disable()
            h3_sizer.Add(self.energiacompactacao, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelGrauCompact = wx.StaticText(panel, label = "Grau de compactação (%)", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(LabelGrauCompact, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.graucompactacao = wx.TextCtrl(panel, -1, self.list[8], style = wx.TE_RIGHT)
            self.graucompactacao.SetMaxLength(5)
            self.graucompactacao.Disable()
            h3_sizer.Add(self.graucompactacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h3_sizer, 1, wx.EXPAND | wx.ALL)

            LabelDataColeta = wx.StaticText(panel, label = "Data da coleta ou recebimento", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(LabelDataColeta, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            dateC = datetime.datetime.strptime(self.list[9], '%d-%m-%Y')
            self.date = wx.adv.DatePickerCtrl(panel, id = wx.ID_ANY, dt = dateC, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            self.date.Disable()
            h4_sizer.Add(self.date, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h4_sizer, 1, wx.EXPAND | wx.ALL)
            LabelDiametroCP = wx.StaticText(panel, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(LabelDiametroCP, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro = wx.TextCtrl(panel, -1, str(self.list[13]), style = wx.TE_RIGHT | wx.TE_READONLY)
            self.diametro.Disable()
            h5_sizer.Add(self.diametro, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h5_sizer, 1, wx.EXPAND | wx.ALL)
            LabelAlturaCP = wx.StaticText(panel, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            h6_sizer.Add(LabelAlturaCP, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura = wx.TextCtrl(panel, -1, str(self.list[14]), style = wx.TE_RIGHT | wx.TE_READONLY)
            self.altura.Disable()
            h6_sizer.Add(self.altura, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            v1_sizer.Add(h6_sizer, 1, wx.EXPAND | wx.ALL)

            staticbox = wx.StaticBox(panel, -1, '')
            staticboxSizer = wx.StaticBoxSizer(staticbox, wx.VERTICAL)
            LabelTipoAmostra = wx.StaticText(panel, label = "Tipo da Amostra", style = wx.ALIGN_RIGHT)
            tipoAmostras = ['Deformada', 'Indeformada']
            self.amostra = wx.RadioBox(panel, label = '', choices = tipoAmostras, majorDimension = 1, style = wx.RA_SPECIFY_COLS)
            self.amostra.SetSelection(int(self.list[12]))
            self.amostra.Disable()
            self.amostra.Bind(wx.EVT_RADIOBOX, self.RadioBoxEvent)
            v2_sizer.Add(LabelTipoAmostra, 0, wx.ALL|wx.CENTER)
            v2_sizer.Add(self.amostra, 0, wx.ALL|wx.CENTER)
            staticboxSizer.Add(v2_sizer, 0, wx.ALL|wx.CENTER)

            h7_sizer.AddStretchSpacer(2)
            h7_sizer.Add(staticboxSizer, 1, wx.EXPAND | wx.ALL, 1)
            h7_sizer.AddStretchSpacer(1)
            h7_sizer.Add(v1_sizer, 5, wx.EXPAND | wx.ALL)

            v_sizer.Add(h7_sizer, 3, wx.EXPAND | wx.ALL)

            LabelObserv = wx.StaticText(panel, label = "Observações", style = wx.ALIGN_RIGHT)
            h9_sizer.Add(LabelObserv, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.obs = wx.TextCtrl(panel, -1, self.list[15], style = wx.TE_RIGHT)
            self.obs.SetMaxLength(120)
            self.obs.Disable()
            h9_sizer.Add(self.obs, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h9_sizer, 1, wx.EXPAND | wx.ALL)

            self.editar = wx.Button(panel, -1, 'Editar')
            self.editar.Bind(wx.EVT_BUTTON, self.Editar)
            self.salvar = wx.Button(panel, -1, 'Salvar')
            self.salvar.Bind(wx.EVT_BUTTON, self.Salvar)
            self.salvar.Disable()
            self.Ensaio = wx.Button(panel, -1, 'Ensaio')
            self.Ensaio.Bind(wx.EVT_BUTTON, self.Prosseguir)
            
            if int(self.list[1]) != 0:
                self.Ensaio.Disable()

            h11_sizer.Add(self.editar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            h11_sizer.Add(self.salvar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            h11_sizer.Add(self.Ensaio, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            v_sizer.Add(h11_sizer, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            sizer.Add(v_sizer, 1,  wx.EXPAND | wx.ALL, 15)

            panel.SetSizer(sizer)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def RadioBoxEvent(self, event):
            amostra = self.amostra.GetSelection()
            if amostra == 1:
                self.diametro.Clear()
                self.altura.Clear()
                self.diametro.SetEditable(True)
                self.altura.SetEditable(True)
            if amostra == 0:
                self.diametro.Clear()
                self.altura.Clear()
                self.diametro.AppendText("100")
                self.altura.AppendText("200")
                self.diametro.SetEditable(False)
                self.altura.SetEditable(False)
    
    #--------------------------------------------------
        def Editar(self, event):
            self.editar.Disable()
            self.Ensaio.Disable()
            self.salvar.Enable()
            if int(self.list[1]) == 0:
                self.Pares.Enable()
                self.amostra.Enable()
                self.diametro.Enable()
                self.altura.Enable()
            self.cp.Enable()
            self.responsavel.Enable()
            self.formacao.Enable()
            self.teordeumidade.Enable()
            self.pesoespecifico.Enable()
            self.umidadeotima.Enable()
            self.energiacompactacao.Enable()
            self.graucompactacao.Enable()
            self.date.Enable()
            self.obs.Enable()

    #--------------------------------------------------
        def Prosseguir(self, event):
            identificador = self.Identificador.GetValue()
            tipo = self.Pares.GetSelection()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            diametro = float(diametro)
            altura = float(altura)
            self.Close(True)
            TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
            # frame = TelaRealizacaoEnsaioDNIT179(identificador, tipo, diametro, altura).ShowModal()

    #--------------------------------------------------
        def Salvar(self, event):
            identificador = self.Identificador.GetValue()
            tipo = self.Pares.GetSelection()
            cp = self.cp.GetValue()
            tecnico = self.responsavel.GetValue()
            formacao = self.formacao.GetValue()
            teordeumidade = self.teordeumidade.GetValue()
            pesoespecifico = self.pesoespecifico.GetValue()
            umidadeotima = self.umidadeotima.GetValue()
            energiacompactacao = self.energiacompactacao.GetValue()
            graucompactacao = self.graucompactacao.GetValue()
            data = self.date.GetValue()
            amostra = self.amostra.GetSelection()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.obs.GetValue()
            condicional = 1

            try:
                diametro = float(diametro)
                altura = float(altura)

            except ValueError:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                diametro = -1
                condicional = -1

            if diametro!='' and altura!='' and diametro>=95 and diametro<=155 and altura>=190 and altura<=310:
                '''Atualiza os dados iniciais de um ensaio'''
                bancodedados.update_dados_179(identificador, tipo, cp, teordeumidade, pesoespecifico, umidadeotima, energiacompactacao, graucompactacao, data, amostra, diametro, altura, obs, tecnico, formacao)
                if int(self.list[1]) == 0:
                    self.Ensaio.Enable()
                self.editar.Enable()
                self.salvar.Disable()
                self.Pares.Disable()
                self.amostra.Disable()
                self.diametro.Disable()
                self.altura.Disable()
                self.cp.Disable()
                self.responsavel.Disable()
                self.formacao.Disable()
                self.teordeumidade.Disable()
                self.pesoespecifico.Disable()
                self.umidadeotima.Disable()
                self.energiacompactacao.Disable()
                self.graucompactacao.Disable()
                self.date.Disable()
                self.obs.Disable()
            else:
                '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                if condicional>0:
                    dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()

'''Tela Editar Ensaio DNIT181'''
class EditarDNIT181(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, idt, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - DNIT 181/2018ME - Editar', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.idt = idt
            self.Bind(wx.EVT_CLOSE, self.onExit)
            frame = self.basic_gui()
        
        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
            
        #--------------------------------------------------
        def basic_gui(self):
            idt = self.idt

            self.list = bancodedados.dados_iniciais_(idt)
            #print self.list

            '''Iserção do IconeLogo'''
            try:
                ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
                self.SetIcon(ico)
            except:
                pass

            '''Configurações do Size'''
            self.SetSize((600,410))
            sizer = wx.BoxSizer(wx.VERTICAL)
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            v1_sizer = wx.BoxSizer(wx.VERTICAL)
            v2_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h2_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h3_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h03_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h4_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h04_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h5_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h6_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h7_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h8_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h9_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h10_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h11_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "Editar Dados do Ensaio", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL)

            h_sizer.AddStretchSpacer(16)
            LabelIdt = wx.StaticText(panel, label = "Identificação", style = wx.ALIGN_RIGHT)
            h_sizer.Add(LabelIdt, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.Identificador = wx.TextCtrl(panel, -1, idt, style = wx.TE_RIGHT)
            self.Identificador.SetMaxLength(15)
            self.Identificador.Disable()
            h_sizer.Add(self.Identificador, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL)

            LabelResponsavelTecnico = wx.StaticText(panel, label = "Responsável Técnico", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(LabelResponsavelTecnico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.responsavel = wx.TextCtrl(panel, -1, self.list[22], style = wx.TE_RIGHT)
            self.responsavel.SetMaxLength(30)
            self.responsavel.Disable()
            h10_sizer.Add(self.responsavel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelFormCrea = wx.StaticText(panel, label = "Formação/CREA", style = wx.ALIGN_RIGHT)
            h10_sizer.Add(LabelFormCrea, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.formacao = wx.TextCtrl(panel, -1, self.list[23], style = wx.TE_RIGHT)
            self.formacao.SetMaxLength(30)
            self.formacao.Disable()
            h10_sizer.Add(self.formacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h10_sizer, 1, wx.EXPAND | wx.ALL)

            LabelNatAmostra = wx.StaticText(panel, label = "Natureza da Amostra", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(LabelNatAmostra, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.cp = wx.TextCtrl(panel, -1, self.list[3], style = wx.TE_RIGHT)
            self.cp.SetMaxLength(30)
            self.cp.Disable()
            h1_sizer.Add(self.cp, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelTeorUmi = wx.StaticText(panel, label = "Teor de Umidade (%)", style = wx.ALIGN_RIGHT)
            h1_sizer.Add(LabelTeorUmi, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.teordeumidade = wx.TextCtrl(panel, -1, self.list[4], style = wx.TE_RIGHT)
            self.teordeumidade.SetMaxLength(5)
            self.teordeumidade.Disable()
            h1_sizer.Add(self.teordeumidade, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h1_sizer, 1, wx.EXPAND | wx.ALL)

            LabelPesoEspecifico = wx.StaticText(panel, label = "Peso específico seco (kN/m³)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(LabelPesoEspecifico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.pesoespecifico = wx.TextCtrl(panel, -1, self.list[5], style = wx.TE_RIGHT)
            self.pesoespecifico.SetMaxLength(5)
            self.pesoespecifico.Disable()
            h2_sizer.Add(self.pesoespecifico, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelUmidadeOtima = wx.StaticText(panel, label = "Umidade Ótima (%)", style = wx.ALIGN_RIGHT)
            h2_sizer.Add(LabelUmidadeOtima, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.umidadeotima = wx.TextCtrl(panel, -1, self.list[6], style = wx.TE_RIGHT)
            self.umidadeotima.SetMaxLength(5)
            self.umidadeotima.Disable()
            h2_sizer.Add(self.umidadeotima, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h2_sizer, 1, wx.EXPAND | wx.ALL)

            LabelEnergCompact = wx.StaticText(panel, label = "Energia de compactação", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(LabelEnergCompact, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.energiacompactacao = wx.TextCtrl(panel, -1, self.list[7], style = wx.TE_RIGHT)
            self.energiacompactacao.SetMaxLength(30)
            self.energiacompactacao.Disable()
            h3_sizer.Add(self.energiacompactacao, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelGrauCompact = wx.StaticText(panel, label = "Grau de compactação (%)", style = wx.ALIGN_RIGHT)
            h3_sizer.Add(LabelGrauCompact, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.graucompactacao = wx.TextCtrl(panel, -1, self.list[8], style = wx.TE_RIGHT)
            self.graucompactacao.SetMaxLength(5)
            self.graucompactacao.Disable()
            h3_sizer.Add(self.graucompactacao, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h3_sizer, 1, wx.EXPAND | wx.ALL)

            LabelTipoEstabQuimico = wx.StaticText(panel, label = "Tipo de estabilizante químico", style = wx.ALIGN_RIGHT)
            h03_sizer.Add(LabelTipoEstabQuimico, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.tipoEstabilizante = wx.TextCtrl(panel, -1, self.list[19], style = wx.TE_RIGHT)
            self.tipoEstabilizante.SetMaxLength(15)
            self.tipoEstabilizante.Disable()
            h03_sizer.Add(self.tipoEstabilizante, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelTempoCura = wx.StaticText(panel, label = "Tempo de cura (dias)", style = wx.ALIGN_RIGHT)
            h03_sizer.Add(LabelTempoCura, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.tempoCura = wx.TextCtrl(panel, -1, self.list[21], style = wx.TE_RIGHT)
            self.tempoCura.SetMaxLength(5)
            self.tempoCura.Disable()
            h03_sizer.Add(self.tempoCura, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h03_sizer, 1, wx.EXPAND | wx.ALL)

            h04_sizer.AddStretchSpacer(16)
            LabelPesoEstabiQuimico = wx.StaticText(panel, label = "Peso do estabilizante químico (%)", style = wx.ALIGN_RIGHT)
            h04_sizer.Add(LabelPesoEstabiQuimico, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.pesoEstabilizante = wx.TextCtrl(panel, -1, self.list[20], style = wx.TE_RIGHT)
            self.pesoEstabilizante.SetMaxLength(5)
            self.pesoEstabilizante.Disable()
            h04_sizer.Add(self.pesoEstabilizante, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h04_sizer, 1, wx.EXPAND | wx.ALL)

            h4_sizer.AddStretchSpacer(16)
            LabelDataColeta = wx.StaticText(panel, label = "Data da coleta ou recebimento", style = wx.ALIGN_RIGHT)
            h4_sizer.Add(LabelDataColeta, 12, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            dateC = datetime.datetime.strptime(self.list[9], '%d-%m-%Y')
            self.date = wx.adv.DatePickerCtrl(panel, id = wx.ID_ANY, dt = dateC, size = wx.DefaultSize, style = wx.adv.DP_SHOWCENTURY | wx.adv.DP_DROPDOWN , validator = wx.DefaultValidator, name = "datectrl")
            self.date.Disable()
            h4_sizer.Add(self.date, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h4_sizer, 1, wx.EXPAND | wx.ALL)

            LabelDiametroCP = wx.StaticText(panel, label = "Diâmetro C.P. (mm)", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(LabelDiametroCP, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.diametro = wx.TextCtrl(panel, -1, str(self.list[13]), style = wx.TE_RIGHT | wx.TE_READONLY)
            self.diametro.Disable()
            h5_sizer.Add(self.diametro, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL)
            LabelAlturaCP = wx.StaticText(panel, label = "Altura C.P. (mm)", style = wx.ALIGN_RIGHT)
            h5_sizer.Add(LabelAlturaCP, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.altura = wx.TextCtrl(panel, -1, str(self.list[14]), style = wx.TE_RIGHT | wx.TE_READONLY)
            self.altura.Disable()
            h5_sizer.Add(self.altura, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h5_sizer, 1, wx.EXPAND | wx.ALL)

            LabelObserv = wx.StaticText(panel, label = "Observações", style = wx.ALIGN_RIGHT)
            h9_sizer.Add(LabelObserv, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
            self.obs = wx.TextCtrl(panel, -1, self.list[15], style = wx.TE_RIGHT)
            self.obs.SetMaxLength(120)
            self.obs.Disable()
            h9_sizer.Add(self.obs, 5, wx.ALIGN_CENTER_VERTICAL | wx.ALL)

            v_sizer.Add(h9_sizer, 1, wx.EXPAND | wx.ALL)

            self.editar = wx.Button(panel, -1, 'Editar')
            self.editar.Bind(wx.EVT_BUTTON, self.Editar)
            self.salvar = wx.Button(panel, -1, 'Salvar')
            self.salvar.Bind(wx.EVT_BUTTON, self.Salvar)
            self.salvar.Disable()
            self.Ensaio = wx.Button(panel, -1, 'Ensaio')
            self.Ensaio.Bind(wx.EVT_BUTTON, self.Prosseguir)
            
            if int(self.list[1]) != 0:
                self.Ensaio.Disable()

            h11_sizer.Add(self.editar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            h11_sizer.Add(self.salvar, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            h11_sizer.Add(self.Ensaio, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
            v_sizer.Add(h11_sizer, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
            sizer.Add(v_sizer, 1,  wx.EXPAND | wx.ALL, 15)

            panel.SetSizer(sizer)
            self.Centre()
            self.Show()

    #--------------------------------------------------
        def Editar(self, event):
            self.editar.Disable()
            self.Ensaio.Disable()
            self.salvar.Enable()
            if int(self.list[1]) == 0:
                self.diametro.Enable()
                self.altura.Enable()
            self.cp.Enable()
            self.responsavel.Enable()
            self.formacao.Enable()
            self.teordeumidade.Enable()
            self.pesoespecifico.Enable()
            self.umidadeotima.Enable()
            self.energiacompactacao.Enable()
            self.graucompactacao.Enable()
            self.date.Enable()
            self.obs.Enable()
            self.tipoEstabilizante.Enable()
            self.tempoCura.Enable()
            self.pesoEstabilizante.Enable()

    #--------------------------------------------------
        def Prosseguir(self, event):
            identificador = self.Identificador.GetValue()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            diametro = float(diametro)
            altura = float(altura)
            self.Close(True)
            TelaRealizacaoEnsaioDNIT135(identificador).ShowModal()
            # frame = TelaRealizacaoEnsaioDNIT181(identificador, diametro, altura).ShowModal()

    #--------------------------------------------------
        def Salvar(self, event):
            identificador = self.Identificador.GetValue()
            cp = self.cp.GetValue()
            tecnico = self.responsavel.GetValue()
            formacao = self.formacao.GetValue()
            teordeumidade = self.teordeumidade.GetValue()
            pesoespecifico = self.pesoespecifico.GetValue()
            umidadeotima = self.umidadeotima.GetValue()
            energiacompactacao = self.energiacompactacao.GetValue()
            graucompactacao = self.graucompactacao.GetValue()
            data = self.date.GetValue()
            diametro = self.diametro.GetValue()
            diametro = format(diametro).replace(',','.')
            diametro = format(diametro).replace('-','')
            altura = self.altura.GetValue()
            altura = format(altura).replace(',','.')
            altura = format(altura).replace('-','')
            obs = self.obs.GetValue()
            tipoEstabilizante = self.tipoEstabilizante.GetValue()
            tempoCura = self.tempoCura.GetValue()
            pesoEstabilizante = self.pesoEstabilizante.GetValue()
            condicional = 1

            try:
                diametro = float(diametro)
                altura = float(altura)

            except ValueError:
                print('Os valores digitados em algum dos campos nao esta da maneira esperada')
                menssagError = wx.MessageDialog(self, 'Os valores digitados em algum dos campos não está da maneira esperada.', 'EDP', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
                diametro = -1
                condicional = -1

            if diametro!='' and altura!='' and diametro>=95 and diametro<=155 and altura>=190 and altura<=310:
                '''Atualiza os dados iniciais de um ensaio'''
                bancodedados.update_dados_181(identificador, cp, teordeumidade, pesoespecifico, umidadeotima, energiacompactacao, graucompactacao, data, diametro, altura, obs, tecnico, formacao, tipoEstabilizante, tempoCura, pesoEstabilizante)
                if int(self.list[1]) == 0:
                    self.Ensaio.Enable()
                self.editar.Enable()
                self.salvar.Disable()
                self.diametro.Disable()
                self.altura.Disable()
                self.cp.Disable()
                self.responsavel.Disable()
                self.formacao.Disable()
                self.teordeumidade.Disable()
                self.pesoespecifico.Disable()
                self.umidadeotima.Disable()
                self.energiacompactacao.Disable()
                self.graucompactacao.Disable()
                self.date.Disable()
                self.obs.Disable()
                self.tipoEstabilizante.Disable()
                self.tempoCura.Disable()
                self.pesoEstabilizante.Disable()
            else:
                '''Diálogo para informar que os campos diametro e altura estão vazios ou não estão na faixa adequada.'''
                if condicional>0:
                    dlg = wx.MessageDialog(None, 'Os valores de Diâmetro e de Altura devem ser preenchidos corretamente.', 'EDP', wx.OK | wx .CENTRE| wx.YES_DEFAULT | wx.ICON_INFORMATION)
                    result = dlg.ShowModal()
    
