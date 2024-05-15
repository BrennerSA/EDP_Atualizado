# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import wx.adv
# import bancodedados
from novoensaio import TelaNovoEnsaio

'''Tela Novo Ensaio'''
class TelaNovo(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, 'Software Marshall - Novo Ensaio', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION)

            self.panel = wx.Panel(self)
            self.SetSize((580,240))
            self.Centre()
            self.Show()

            self.FontTitle =wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
            self.title = wx.StaticText(self.panel, -1, 'ENSAIOS', (20,20), (540,-1), wx.ALIGN_CENTER)
            self.title.SetFont(self.FontTitle)
            self.normatext = wx.StaticText(self.panel, -1, 'NORMA', (20,62.5), (50,-1))
            ensaios = ['DNER-ME 043/95 - Misturas betuminosas a quente - ensaio Marshall',
                        'DNER-ME 107/94 - Misturas betuminosa a frio, com emulsão asfáltica - ensaio Marshall',
                        'DNIT 136/2018 - ME - Determinação da resistência à tração por compressão diametral']
            self.caixaensaio = wx.ComboBox(self.panel, -1,'SELECIONE A NORMA',(80,60),(480,-1),choices = ensaios)
            self.continuar = wx.Button(self.panel, -1, 'Continuar', (20, 180), (540,-1))
            self.Bind(wx.EVT_BUTTON, self.Prosseguir, self.continuar)

    #--------------------------------------------------
        def Prosseguir(self, event):
            a = self.caixaensaio.GetValue()

            if(a[0] != 'D'):
                print('Nenhum ensaio foi selecionado')
                menssagError = wx.MessageDialog(self, 'Nenhum ensaio foi selecionado', 'Software Marshall', wx.OK|wx.ICON_INFORMATION)
                aboutPanel = wx.TextCtrl(menssagError, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
                menssagError.ShowModal()
                menssagError.Destroy()
            else:
                self.Close(True)
                con = TelaNovoEnsaio(a)
                con.ShowModal()
