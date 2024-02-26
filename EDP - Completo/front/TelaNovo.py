# -*- coding: utf-8 -*-

'''Bibliotecas'''
import wx
from front.TelaNovoEnsaioDNIT134 import TelaNovoEnsaioDNIT134
from front.TelaNovoEnsaioDNIT179 import TelaNovoEnsaioDNIT179
from front.TelaNovoEnsaioDNIT181 import TelaNovoEnsaioDNIT181
from front.TelaNovoEnsaioDNIT135 import TelaNovoEnsaioDNIT135
from front.TelaNovoEnsaioDNIT183 import TelaNovoEnsaioDNIT183
import back.HexForRGB as HexRGB
import banco.bdPreferences as bdPreferences

#normas = ['DNIT 134/2018ME', 'DNIT 135/2018ME', 'DNIT 179/2018IE', 'DNIT 184/2018ME', 'DNIT 416/2019ME']
normas = ['DNIT 134/2018ME', 'DNIT 179/2018IE', 'DNIT 181/2018ME','DNIT 135/2018ME','DNIT 183/2018ME']

'''Tela Selecão de Ensaio'''
class TelaNovo(wx.Dialog):
    #--------------------------------------------------
        def __init__(self,mainref, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'EDP - Novo Ensaio', style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)
            self.Bind(wx.EVT_CLOSE, self.onExit)
            self.mainref=mainref
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
            self.SetSize((250,200))
            v_sizer = wx.BoxSizer(wx.VERTICAL)
            h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            h1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            title = wx.StaticText(panel, label = "ENSAIOS DINÂMICOS", style = wx.ALIGN_CENTRE)
            title.SetFont(FontTitle)
            '''title.SetBackgroundColour("green")'''
            v_sizer.Add(title, 1, wx.EXPAND | wx.ALL, 15)

            texto1 = wx.StaticText(panel, label = "NORMA", style = wx.ALIGN_CENTER_VERTICAL)
            h_sizer.Add(texto1, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            self.combo = wx.ComboBox(panel, choices = normas, style = wx.EXPAND | wx.CB_READONLY)
            h_sizer.Add(self.combo, 7, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)

            v_sizer.Add(h_sizer, 1, wx.EXPAND | wx.ALL, 12)
            v_sizer.AddStretchSpacer(1)
            continuar = wx.Button(panel, -1, 'Continuar')
            v_sizer.Add(continuar, 1,  wx.EXPAND| wx.ALL, 15)

            panel.SetSizer(v_sizer)
            self.Centre()
            self.Show()

            continuar.Bind(wx.EVT_BUTTON, self.Prosseguir)

    #--------------------------------------------------
        def Prosseguir(self, event):
            a = self.combo.GetSelection()

            if a == 0:
                # '''Acessa a DNIT 134/2018ME'''
                self.Close(True)
                TelaNovoEnsaioDNIT134(self.mainref).ShowModal()
            elif a == 1:
                # '''Acessa a DNIT 179/2018IE'''
                self.Close(True)
                TelaNovoEnsaioDNIT179().ShowModal()
            elif a == 2:
                # '''Acessa a DNIT 181/2018ME'''
                self.Close(True)
                TelaNovoEnsaioDNIT181().ShowModal()
            elif a == 3:
                # Acessa a DNIT 135/2018ME
                self.Close(True)
                TelaNovoEnsaioDNIT135(self.mainref).ShowModal()
            elif a == 4:
                # Acessa a DNIT 183/2018ME
                self.Close(True)
                TelaNovoEnsaioDNIT183().ShowModal()

        #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
