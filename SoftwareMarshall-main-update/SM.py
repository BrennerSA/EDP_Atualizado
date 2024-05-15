# -*- coding: utf-8 -*-

'''Bibliotecas'''

import sys
import wx
import matplotlib
import datetime
import serial
import numpy
import math
import sqlite3
import reportlab

import front.tela as tela

'''Inicializacao do programa'''
class main():
     app = wx.App()
     app.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
     tela.Tela(None)
     app.MainLoop()

main()
