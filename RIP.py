# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 01:57:01 2021

@author: Ryan
"""

from tkinter import *
import sqlite3
from NewRecipe import *
from ListRecipe import *
from PIL import  Image, ImageTk


global root
bottom_viewall = False
bottom_history =False


def viewall():
    global bottom_viewall
    global viewallrecipe_gridrow    
    viewallrecipe_gridrow = 0    
    
    if not bottom_viewall:
        global viewallframe_hmpg
        viewallframe_hmpg = LabelFrame(root, text='Recipes')
        viewallframe_hmpg.grid(row=7,column=0, columnspan=3)
        bottom_viewall = True
        for recipe in os.listdir(r'./Recipes'):
            recipepath = r'./Recipes' + f'/{recipe}.db'
            recipe = Button(viewallframe_hmpg, text = recipe[:-3], command = lambda recipe=recipe: accessrecipe(recipe[:-3]))
            recipe.grid(row=viewallrecipe_gridrow, column=1)
            viewallrecipe_gridrow +=1        
    else:        
        viewallframe_hmpg.destroy()
        bottom_viewall = False


#Basic stuff
root = Tk()
root.title('Recipe Index Project (Alpha ver. 0.01)')
root.iconbitmap('./resources/img/Ico.ico')


#Homepage items (hmpg)
welcomeimg_hmpg = ImageTk.PhotoImage(Image.open('./resources/img/Ico.ico'))
welcomelogo_hmpg = Label(root, image=welcomeimg_hmpg).grid(row=0,column=0,columnspan=3)
welcometext_hmpg = Label(root, text='RECIPE INDEX PROJECT').grid(row=1,column=0, columnspan=3)

searchbar_hmpg = Entry(root, width = 50, borderwidth = 5)
searchbar_hmpg.grid(row=3,column=0)
searchbutton_hmpg = Button(root, text='Search')
searchbutton_hmpg.grid(row=3,column=2)

viewallrecipes_hmpg = Button(root, text='View All', command = viewall)
viewallrecipes_hmpg.grid(row=4,column=0, columnspan=3)


newrecipe_hmpg = Button(root, text='Submit New Recipe', command=submitnewrecipe)
newrecipe_hmpg.grid(row=5,column=0, columnspan=3)

history_hmpg = Button(root, text='History')
history_hmpg.grid(row=6,column=0, columnspan=3)





root.mainloop()