# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 03:57:46 2021

@author: Ryan
"""
from tkinter import Tk
from widget_creation import windowconfiguration, windowlayoutcreation
from color_config import mainbgcolor, mainfgcolor

def viewrecipe(recipename):
    viewrecipe= Tk()
    windowconfiguration(viewrecipe, recipename, './resources/img/Ico.ico', mainbgcolor, '', '', '', '', '')
    
    framelist_viewrecipe = []
    canvaslist_viewrecipe = []
    basicinfo_viewrecipe = []
    
    windowlayoutcreation(viewrecipe, framelist_viewrecipe, canvaslist_viewrecipe, basicinfo_viewrecipe)
    viewrecipe.mainloop()