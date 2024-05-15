# -*- coding: utf-8 -*-

'''Bibliotecas'''

import wx
# import bancodedados
import bancodedadosnovo
import wx.lib.mixins.listctrl as listmix
from wx.lib.agw import ultimatelistctrl as ULC
from novo import TelaNovo
from telagrafico import TelaRealizacaoEnsaioDNER04395
from cabecalhos import Cab
from editarensaio import EditarEnsaio
from Csv import Csv
from Pdf import Pdf

'''Classe da Lista editável'''
class EditableListCtrl(ULC.UltimateListCtrl, listmix.ListCtrlAutoWidthMixin):
    #--------------------------------------------------
        def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
            ULC.UltimateListCtrl.__init__(self, parent, ID, pos, size, agwStyle = ULC.ULC_REPORT | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT | ULC.ULC_HRULES | ULC.ULC_VRULES | ULC.ULC_NO_HIGHLIGHT)

        def UpdateListCtrl(self):
            self.DeleteAllItems()
            lista = bancodedadosnovo.get_values()#bancodedados.ListaVisualizacao()
            index = 0

            for key, row in lista:
                   pos = self.list_ctrl.InsertStringItem(index, 'E'+str(key)+'/'+row[2])
                   self.SetStringItem(index, 1, row[0])
                   self.SetStringItem(index, 2, row[1])
                   buttonEDT = wx.Button(self, id = key, label="")
                   buttonGRF = wx.Button(self, id = 4000+key, label="")
                   buttonPDF = wx.Button(self, id = 10000+key, label="")
                   buttonCSV = wx.Button(self, id = 15000+key, label="")
                   buttonDEL = wx.Button(self, id = 20000+key, label="")
                   buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
                   buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
                   buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
                   buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
                   buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
                   self.SetItemWindow(pos, col=3, wnd=buttonPDF, expand=True)
                   self.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
                   self.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                   self.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
                   self.SetItemData(index, key)
                   index += 1

            if len(lista) >=8:
               self.SetColumnWidth(0, width=145)
               self.SetColumnWidth(1, width=155)
               self.SetColumnWidth(2, width=100)
               self.SetColumnWidth(3, width=40)
               self.SetColumnWidth(4, width=40)
               self.SetColumnWidth(5, width=40)
               self.SetColumnWidth(6, width=40)
            else:
               self.SetColumnWidth(0, width=155)
               self.SetColumnWidth(1, width=160)
               self.SetColumnWidth(2, width=100)
               self.SetColumnWidth(3, width=40)
               self.SetColumnWidth(4, width=40)
               self.SetColumnWidth(5, width=40)
               self.SetColumnWidth(6, width=40)

'''Tela Inicial'''
class Tela(wx.Frame):
    #------------------------------------------------------
     def __init__(self, *args, **kwargs):
         super(Tela, self).__init__(title = 'Software de Marshall - v1.0', name = 'Facade', style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION, *args, **kwargs)
         self.basic_gui()

     def basic_gui(self):
         self.panel = wx.Panel(self)

         ico = wx.Icon('icons\logo.ico', wx.BITMAP_TYPE_ICO)
         self.SetIcon(ico)

         self.SetSize((620,500))
         self.Centre()
         self.Show()

         '''StatusBar'''
         self.CreateStatusBar()
         self.SetStatusText('Ensaios utilizando prensa de Marshall')

         '''MenuBarra'''
         arquivoMenu = wx.Menu()
         ajudaMenu = wx.Menu()
         menuBar = wx.MenuBar()
         menuBar.Append(arquivoMenu, '&Arquivo')
         menuBar.Append(ajudaMenu, '&Ajuda')

         novoEnsaioMenuItem = arquivoMenu.Append(wx.NewId(),'Novo Ensaio\tCtrl+N', 'Novo Ensaio')
         arquivoMenu.AppendSeparator()
         cabecalhosMenuItem = arquivoMenu.Append(wx.NewId(), 'Cabeçalhos\tCtrl+C','Cabeçalhos')
         arquivoMenu.AppendSeparator()
         atualizarEnsaiosMenuItem = arquivoMenu.Append(wx.NewId(), 'Atualizar Ensaios\tCtrl+A','Atualizar Ensaios')
         arquivoMenu.AppendSeparator()
         exitMenuItem = arquivoMenu.Append(wx.NewId(), 'Sair\tCtrl+S','Sair')
         ajudaMenuItem = ajudaMenu.Append(wx.NewId(),'Ajuda\tCtrl+A','Ajuda')
         self.Bind(wx.EVT_MENU, self.NovoEnsaio, novoEnsaioMenuItem)
         self.Bind(wx.EVT_MENU, self.Cabecalhos, cabecalhosMenuItem)
         self.Bind(wx.EVT_MENU, self.Update, atualizarEnsaiosMenuItem)
         self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
         self.Bind(wx.EVT_MENU, self.ajudaGUI, ajudaMenuItem)
         self.SetMenuBar(menuBar)

         '''Botao Novo Ensaio'''
         FontTitle = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
         self.novoensaio_texto= wx.StaticText(self.panel, -1, 'Novo Ensaio: ',(272,35), (80,-1), wx.ALIGN_CENTER)
         self.button = wx.Button(self.panel, -1, '', (286, 60), (48,48))
         self.button.SetBitmap(wx.Image('icons\icons-adicionar-48px.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
         self.Bind(wx.EVT_BUTTON, self.NovoEnsaio, self.button)

         self.novoensaio_texto.SetFont(FontTitle)

         bancodedadosnovo.clean()

         lista = bancodedadosnovo.get_values()#bancodedados.ListaVisualizacao()#

         '''Lista dos Ensaios'''
         self.list_ctrl = EditableListCtrl(self.panel, size=(575,250), pos=(20,160) )
         if len(lista) >=8:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICADOR', wx.LIST_FORMAT_CENTRE, width=145)
             self.list_ctrl.InsertColumn(1, 'DATA DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=155)
             self.list_ctrl.InsertColumn(2, 'OPERADOR', wx.LIST_FORMAT_CENTRE, width=100)
             self.list_ctrl.InsertColumn(3, 'PDF', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(4, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(5, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(6, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)
         else:
             self.list_ctrl.InsertColumn(0, 'IDENTIFICADOR', wx.LIST_FORMAT_CENTRE, width=155)
             self.list_ctrl.InsertColumn(1, 'DATA DO ENSAIO', wx.LIST_FORMAT_CENTRE, width=160)
             self.list_ctrl.InsertColumn(2, 'OPERADOR', wx.LIST_FORMAT_CENTRE, width=100)
             self.list_ctrl.InsertColumn(3, 'PDF', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(4, 'EDT', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(5, 'CSV', wx.LIST_FORMAT_CENTRE, width=40)
             self.list_ctrl.InsertColumn(6, 'DEL', wx.LIST_FORMAT_CENTRE, width=40)

         index = 0

         for key, row in lista:
             pos = self.list_ctrl.InsertStringItem(index, 'E'+str(key)+'/'+row[2])
             self.list_ctrl.SetStringItem(index, 1, row[0])
             self.list_ctrl.SetStringItem(index, 2, row[1])
             buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
             buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
             buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
             buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
             buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
             buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
             buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
             buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
             buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
             buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
             self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonPDF, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
             self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
             self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
             self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
             self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
             self.Bind(wx.EVT_BUTTON, self.exportPdf, buttonPDF)
             self.list_ctrl.SetItemData(index, key)
             index += 1

        #  self.Bind(wx.EVT_LIST_COL_DRAGGING, self.ColumAdapter, self.list_ctrl)
        #  self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.ColumAdapter2, self.list_ctrl)
        #  self.Bind(wx.EVT_LIST_COL_CLICK, self.ColumAdapter3, self.list_ctrl)
         self.vBox = wx.BoxSizer(wx.VERTICAL)
         self.vBox.Add ((-1, 140))
         self.vBox.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 20)
         self.SetSizer(self.vBox)

    #--------------------------------------------------
     def Editar(self, event):
         id = event.GetId()
         frame = EditarEnsaio(id)
         frame.ShowModal()
         self.Update()
         # dialogo = EditarEnsaio()
         # resultado = dialogo.ShowModal()
         # self.list_ctrl.UpdateListCtrl()

    #--------------------------------------------------
     def exportCSV(self, event):
         id = event.GetId()
         id = id - 15000
         Csv(id)

     def exportPdf(self, event):
         id = event.GetId()
         id = id - 1000
         Pdf(id).ShowModal()

    #--------------------------------------------------
     def Deletar(self, event):
         id = event.GetId()
         id = id - 20000

         '''Diálogo se deseja realmente excluir o Ensaio'''
         dlg = wx.MessageDialog(None, 'Deseja mesmo excluir esse Ensaio?', 'Software Marshall', wx.YES_NO | wx.CENTRE| wx.NO_DEFAULT )
         result = dlg.ShowModal()

         if result == wx.ID_YES:
             bancodedadosnovo.delete(id)
             dlg.Destroy()

             self.Update()

            #  self.list_ctrl.DeleteAllItems()
            #  lista = bancodedadosnovo.get_values()#.ListaVisualizacao()
            #  index = 0

            #  for key, row in lista:
            #         pos = self.list_ctrl.InsertStringItem(index, 'E'+str(key)+'/'+row[2])
            #         self.list_ctrl.SetStringItem(index, 1, row[0])
            #         self.list_ctrl.SetStringItem(index, 2, row[1])
            #         buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
            #         buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
            #         buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
            #         buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
            #         buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
            #         buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
            #         buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
            #         buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
            #         buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
            #         buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
            #         self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonPDF, expand=True)
            #         self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
            #         self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
            #         self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
            #         self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
            #         self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
            #         self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
            #         self.Bind(wx.EVT_BUTTON, self.exportPdf, buttonPDF)
            #         self.list_ctrl.SetItemData(index, key)
            #         index += 1

            #  if len(lista) >=8:
            #     self.list_ctrl.SetColumnWidth(0, width=145)
            #     self.list_ctrl.SetColumnWidth(1, width=155)
            #     self.list_ctrl.SetColumnWidth(2, width=100)
            #     self.list_ctrl.SetColumnWidth(3, width=40)
            #     self.list_ctrl.SetColumnWidth(4, width=40)
            #     self.list_ctrl.SetColumnWidth(5, width=40)
            #     self.list_ctrl.SetColumnWidth(6, width=40)
            #  else:
            #     self.list_ctrl.SetColumnWidth(0, width=155)
            #     self.list_ctrl.SetColumnWidth(1, width=160)
            #     self.list_ctrl.SetColumnWidth(2, width=100)
            #     self.list_ctrl.SetColumnWidth(3, width=40)
            #     self.list_ctrl.SetColumnWidth(4, width=40)
            #     self.list_ctrl.SetColumnWidth(5, width=40)
            #     self.list_ctrl.SetColumnWidth(6, width=40)
         else:
             dlg.Destroy()
    #--------------------------------------------------
     def Update(self):

         self.list_ctrl.DeleteAllItems()
         lista = bancodedadosnovo.get_values()#.ListaVisualizacao()
         index = 0

         for key, row in lista:
                pos = self.list_ctrl.InsertStringItem(index, 'E'+str(key)+'/'+row[2])
                self.list_ctrl.SetStringItem(index, 1, row[0])
                self.list_ctrl.SetStringItem(index, 2, row[1])
                buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
                buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
                buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
                buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
                buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
                buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
                buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
                buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
                buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
                buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
                self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonPDF, expand=True)
                self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
                self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
                self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
                self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
                self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
                self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
                self.Bind(wx.EVT_BUTTON, self.exportPdf, buttonPDF)
                self.list_ctrl.SetItemData(index, key)
                index += 1

         if len(lista) >=8:
            self.list_ctrl.SetColumnWidth(0, width=145)
            self.list_ctrl.SetColumnWidth(1, width=155)
            self.list_ctrl.SetColumnWidth(2, width=100)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)
         else:
            self.list_ctrl.SetColumnWidth(0, width=155)
            self.list_ctrl.SetColumnWidth(1, width=160)
            self.list_ctrl.SetColumnWidth(2, width=100)
            self.list_ctrl.SetColumnWidth(3, width=40)
            self.list_ctrl.SetColumnWidth(4, width=40)
            self.list_ctrl.SetColumnWidth(5, width=40)
            self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def NovoEnsaio(self, event):
        #  quant = bancodedados.quant_ensaios_deletados()
        #  valor_Logico = bancodedados.ler_quant_ensaios() - 1 - quant
         frame = TelaNovo()
        #  self.Hide()
         frame.ShowModal()
         self.Show()
         print("voltou pra tela")
         self.Update()
         

        #  lista = bancodedados.ListaVisualizacao()
        #  index = bancodedados.ler_quant_ensaios() - 1 - quant

        #  '''For apenas para definir os key's'''
        #  for key, row in lista:
        #      pass

        #  if valor_Logico == index:
        #      pass

        #  else:
        #      pos = self.list_ctrl.InsertStringItem(index, lista[index][1][0])
        #      self.list_ctrl.SetStringItem(index, 1, lista[index][1][1])
        #      self.list_ctrl.SetStringItem(index, 2, lista[index][1][3])
        #      buttonEDT = wx.Button(self.list_ctrl, id = key, label="")
        #      buttonGRF = wx.Button(self.list_ctrl, id = 4000+key, label="")
        #      buttonPDF = wx.Button(self.list_ctrl, id = 10000+key, label="")
        #      buttonCSV = wx.Button(self.list_ctrl, id = 15000+key, label="")
        #      buttonDEL = wx.Button(self.list_ctrl, id = 20000+key, label="")
        #      buttonEDT.SetBitmap(wx.Bitmap('icons\icons-editar-arquivo-24px.png'))
        #      buttonGRF.SetBitmap(wx.Bitmap('icons\icons-grafico-24px.png'))
        #      buttonPDF.SetBitmap(wx.Bitmap('icons\icons-exportar-pdf-24px.png'))
        #      buttonCSV.SetBitmap(wx.Bitmap('icons\icons-exportar-csv-24px.png'))
        #      buttonDEL.SetBitmap(wx.Bitmap('icons\icons-lixo-24px.png'))
        #      self.list_ctrl.SetItemWindow(pos, col=3, wnd=buttonPDF, expand=True)
        #      self.list_ctrl.SetItemWindow(pos, col=4, wnd=buttonEDT, expand=True)
        #      self.list_ctrl.SetItemWindow(pos, col=5, wnd=buttonCSV, expand=True)
        #      self.list_ctrl.SetItemWindow(pos, col=6, wnd=buttonDEL, expand=True)
        #      self.Bind(wx.EVT_BUTTON, self.Editar, buttonEDT)
        #      self.Bind(wx.EVT_BUTTON, self.exportCSV, buttonCSV)
        #      self.Bind(wx.EVT_BUTTON, self.Deletar, buttonDEL)
        #      self.Bind(wx.EVT_BUTTON, self.exportPdf, buttonPDF)
        #      self.list_ctrl.SetItemData(index, key)
        #      self.list_ctrl.Update()
        #      valor_Logico = valor_Logico + 1

        #  lista = bancodedados.ListaVisualizacao()
        #  if len(lista) >=8:
        #     self.list_ctrl.SetColumnWidth(0, width=145)
        #     self.list_ctrl.SetColumnWidth(1, width=155)
        #     self.list_ctrl.SetColumnWidth(2, width=100)
        #     self.list_ctrl.SetColumnWidth(3, width=40)
        #     self.list_ctrl.SetColumnWidth(4, width=40)
        #     self.list_ctrl.SetColumnWidth(5, width=40)
        #     self.list_ctrl.SetColumnWidth(6, width=40)
        #  else:
        #     self.list_ctrl.SetColumnWidth(0, width=155)
        #     self.list_ctrl.SetColumnWidth(1, width=160)
        #     self.list_ctrl.SetColumnWidth(2, width=100)
        #     self.list_ctrl.SetColumnWidth(3, width=40)
        #     self.list_ctrl.SetColumnWidth(4, width=40)
        #     self.list_ctrl.SetColumnWidth(5, width=40)
        #     self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def Cabecalhos(self, event):
         '''Abri tela com os Cabeçalhos cadastrados'''
         Cab()

    #--------------------------------------------------
     def ajudaGUI(self, event):
          '''Dialogo ajuda'''
          message1 = ('Software Marshall')
          message2 = ('Esse software foi desenvolvido para realizar ensaios que atendam as normas de ensnaio DNER 043/95, DNER 107/94 e DNIT 136/2018')
          dlg = wx.MessageDialog(self, message1 + message2, 'Software Marshall', wx.OK|wx.ICON_INFORMATION)
          wx.TextCtrl(dlg, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
          dlg.ShowModal()
          dlg.Destroy()

    #--------------------------------------------------
    #  def ColumAdapter(self, event):
    #      lista = bancodedados.ListaVisualizacao()
    #      '''Ajusta os tamanhos das colunas ao arrastar'''
    #      if len(lista) >=8:
    #         self.list_ctrl.SetColumnWidth(0, width=145)
    #         self.list_ctrl.SetColumnWidth(1, width=155)
    #         self.list_ctrl.SetColumnWidth(2, width=100)
    #         self.list_ctrl.SetColumnWidth(3, width=40)
    #         self.list_ctrl.SetColumnWidth(4, width=40)
    #         self.list_ctrl.SetColumnWidth(5, width=40)
    #         self.list_ctrl.SetColumnWidth(6, width=40)
    #      else:
    #         self.list_ctrl.SetColumnWidth(0, width=155)
    #         self.list_ctrl.SetColumnWidth(1, width=160)
    #         self.list_ctrl.SetColumnWidth(2, width=100)
    #         self.list_ctrl.SetColumnWidth(3, width=40)
    #         self.list_ctrl.SetColumnWidth(4, width=40)
    #         self.list_ctrl.SetColumnWidth(5, width=40)
    #         self.list_ctrl.SetColumnWidth(6, width=40)

    # #--------------------------------------------------
    #  def ColumAdapter2(self, event):
    #      lista = bancodedados.ListaVisualizacao()
    #      '''Ajusta os tamanhos das colunas ao clicar com botão esquerdo sobre a coluna'''
    #      if len(lista) >=8:
    #         self.list_ctrl.SetColumnWidth(0, width=145)
    #         self.list_ctrl.SetColumnWidth(1, width=155)
    #         self.list_ctrl.SetColumnWidth(2, width=100)
    #         self.list_ctrl.SetColumnWidth(3, width=40)
    #         self.list_ctrl.SetColumnWidth(4, width=40)
    #         self.list_ctrl.SetColumnWidth(5, width=40)
    #         self.list_ctrl.SetColumnWidth(6, width=40)
    #      else:
    #         self.list_ctrl.SetColumnWidth(0, width=155)
    #         self.list_ctrl.SetColumnWidth(1, width=160)
    #         self.list_ctrl.SetColumnWidth(2, width=100)
    #         self.list_ctrl.SetColumnWidth(3, width=40)
    #         self.list_ctrl.SetColumnWidth(4, width=40)
    #         self.list_ctrl.SetColumnWidth(5, width=40)
    #         self.list_ctrl.SetColumnWidth(6, width=40)

    # #--------------------------------------------------
    #  def ColumAdapter3(self, event):
    #      lista = bancodedados.ListaVisualizacao()
    #      '''Ajusta os tamanhos das colunas ao clicar com o botão direito sobre a coluna'''
    #      if len(lista) >=8:
    #         self.list_ctrl.SetColumnWidth(0, width=145)
    #         self.list_ctrl.SetColumnWidth(1, width=155)
    #         self.list_ctrl.SetColumnWidth(2, width=100)
    #         self.list_ctrl.SetColumnWidth(3, width=40)
    #         self.list_ctrl.SetColumnWidth(4, width=40)
    #         self.list_ctrl.SetColumnWidth(5, width=40)
    #         self.list_ctrl.SetColumnWidth(6, width=40)
    #      else:
    #         self.list_ctrl.SetColumnWidth(0, width=155)
    #         self.list_ctrl.SetColumnWidth(1, width=160)
    #         self.list_ctrl.SetColumnWidth(2, width=100)
    #         self.list_ctrl.SetColumnWidth(3, width=40)
    #         self.list_ctrl.SetColumnWidth(4, width=40)
    #         self.list_ctrl.SetColumnWidth(5, width=40)
    #         self.list_ctrl.SetColumnWidth(6, width=40)

    #--------------------------------------------------
     def onExit(self, event):
          '''Opcao Sair'''
          self.Close(True)
