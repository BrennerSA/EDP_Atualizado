# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
import HexForRGB as HexRGB
import bdPreferences as bdPreferences 

'''Tela Dialogo Dinamico'''
class dialogoDinamico(wx.Dialog):
    #--------------------------------------------------
        def __init__(self, indicador, info, texto0, texto1, texto2, texto3, texto4,conexao, *args, **kwargs):
            wx.Dialog.__init__(self, None, -1, "%s" %info, style = wx.CLOSE_BOX)

            colors = bdPreferences.ListColors()
            colorBackground = colors[2]
            self.conexao=conexao

            self.SetBackgroundColour(colorBackground)
            
            self.v_sizer = wx.BoxSizer(wx.VERTICAL)
            self.v_sizer2 = wx.BoxSizer(wx.VERTICAL)
            self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.h_sizer2= wx.BoxSizer(wx.HORIZONTAL)
            self.Bind(wx.EVT_CLOSE, self.onExit)

            FontTitle = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo2 = wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD)
            FontCorpo1 = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)

            if indicador == 1:
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                TextoCorpo3 = wx.StaticText(self, label = texto3, style = wx.ALIGN_CENTRE)
                TextoCorpo3.SetFont(FontCorpo1)
                Button = wx.Button(self, id = wx.ID_CANCEL, label = "OK", style = wx.BORDER_NONE)
                Button2=wx.Button(self, label= "Cancelar", style=wx.BORDER_NONE)
                Button2.Hide()
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo3, 1, wx.CENTER)
                self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((400,185))

            if indicador == 2:
                FontCorpo2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                Button = wx.Button(self, label = "OK", style = wx.BORDER_NONE)
                Button2=wx.Button(self, label= "Cancelar", style=wx.BORDER_NONE)
                Button2.Hide()
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 2, wx.CENTER)
                self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER)
                self.v_sizer.Add(Button2,1,wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((620,185))

            if indicador == 3:
                FontCorpo2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                Button = wx.Button(self, label = "OK", style = wx.BORDER_NONE)
                Button2=wx.Button(self, label= "Cancelar", style=wx.BORDER_NONE)
                Button2.Hide()
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 2, wx.CENTER)
                self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((620,185))

            if indicador==4:
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                TextoCorpo3 = wx.StaticText(self, label = texto3, style = wx.ALIGN_CENTRE)
                TextoCorpo3.SetFont(FontCorpo1)
                panel=wx.Panel(self)
                progress_bar = wx.Gauge(panel, range=100)
                # Button = wx.Button(self, id = wx.ID_CANCEL, label = "OK", style = wx.BORDER_NONE)
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo3, 1, wx.CENTER)
                self.v_sizer.Add(progress_bar, 1, wx.ALL | wx.CENTER)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                self.SetSize((400,185))
                # self.Bind(wx.EVT_BUTTON, self.Button, Button)
                self.SetSizer(self.h_sizer)
            
            if indicador==5:
                FontCorpo2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
                TextoTitle = wx.StaticText(self, label = texto0, style = wx.ALIGN_CENTRE)
                TextoTitle.SetFont(FontTitle)
                TextoTitle.SetForegroundColour((0,51,188))
                TextoCorpo1 = wx.StaticText(self, label = texto1, style = wx.ALIGN_CENTRE)
                TextoCorpo1.SetFont(FontCorpo1)
                TextoCorpo2 = wx.StaticText(self, label = texto2, style = wx.ALIGN_CENTRE)
                TextoCorpo2.SetFont(FontCorpo2)
                TextoCorpo2.SetForegroundColour((231,160,48))
                self.Button = wx.Button(self, label = "OK", style = wx.BORDER_NONE)
                self.Button3=wx.Button(self, label= "Subir/Parar", style=wx.BORDER_NONE)
                self.Button4=wx.Button(self, label= "Descer/Parar", style=wx.BORDER_NONE)
                self.v_sizer.Add(TextoTitle, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo1, 1, wx.CENTER)
                self.v_sizer.Add(TextoCorpo2, 2, wx.CENTER)
                # self.v_sizer.Add(Button, 1, wx.ALL | wx.CENTER | wx.LEFT)
                # self.v_sizer.Add(Button2,1,wx.ALL | wx.CENTER)
                self.h_sizer2.Add(self.Button, 0, wx.ALL | wx.CENTER)
                self.h_sizer2.Add(wx.StaticText(self,size=(50, 50)), proportion=5, flag=wx.EXPAND)
                self.h_sizer2.Add(self.Button3, 0, wx.ALL | wx.CENTER)
                self.h_sizer2.Add(wx.StaticText(self,size=(50, 50)), proportion=5, flag=wx.EXPAND)
                self.h_sizer2.Add(self.Button4, 0, wx.ALL | wx.CENTER)
                self.v_sizer2.Add(self.h_sizer2,1, wx.CENTER)
                self.v_sizer.Add(self.v_sizer2,0,  wx.EXPAND | wx.ALL, 1)
                self.h_sizer.Add(self.v_sizer, 1,  wx.EXPAND | wx.ALL, 10)
                
                
                self.SetSize((620,185))

            if indicador != 4:
                self.Bind(wx.EVT_BUTTON, self.Ok, self.Button)
                self.Bind(wx.EVT_BUTTON,self.Subir,self.Button3)
                self.Bind(wx.EVT_BUTTON,self.Descer,self.Button4)
                self.SetSizer(self.h_sizer)
                self.isUp=False
                self.isDown=False


            self.Centre()
            self.Show()
            
    #--------------------------------------------------
        def Ok(self, event):
            self.conexao.write('P')
            self.EndModal(wx.ID_OK)
            self.Destroy()
        
    #--------------------------------------------------
        def onExit(self, event):
            '''Opcao Sair'''
            self.Destroy()
        

        def Subir(self, event):
            if not self.isUp:
                self.conexao.write('U')
                print("subindo")
                self.Button3.SetLabel("Parar")
                self.isUp=True
            else:
                self.conexao.write('P')
                print("parando")
                self.Button3.SetLabel("Subir")
                self.isUp=False
            

        def Descer(self,event):
            if not self.isDown:
                self.conexao.write('D')
                print("descendo")
                self.Button4.SetLabel("Parar")
                self.isDown=True
            else:
                self.conexao.write('P')
                print("parando")
                self.Button4.SetLabel("Descer")
                self.isDown=False
