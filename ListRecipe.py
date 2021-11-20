# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 15:02:57 2021

@author: Ryan
"""
from tkinter import *
import sqlite3
from EditRecipe import *


def closeforedit(recipe):
    viewrecipe.destroy()
    editdatabase(recipe)

def accessrecipe(recipe):
    global viewrecipe
    viewrecipe = Tk()
    viewrecipe.title(recipe)
    viewrecipe.iconbitmap('./resources/img/Ico.ico')
    
    recipedbpath = r'./Recipes' + f'/{recipe}.db'
    
    vrconn = sqlite3.connect(recipedbpath)
    vrcurs = vrconn.cursor()
    

    
    #Recipe Name Frame
    rnframe_viewrecipe = LabelFrame(viewrecipe, text='RECIPE NAME')
    rnframe_viewrecipe.grid(row=0,column=0,columnspan=2)
    rnlabel_viewrecipe = Label(rnframe_viewrecipe, text= recipe)
    rnlabel_viewrecipe.grid(row=0,column=0)
    
    #Servings Frame
    sframe_viewrecipe = LabelFrame(viewrecipe, text='SERVINGS')
    sframe_viewrecipe.grid(row=1,column=0)

    #Time Required Frame
    trframe_viewrecipe = LabelFrame(viewrecipe, text='TIME REQUIRED')
    trframe_viewrecipe.grid(row=1,column=1)

    
    #Ingredients Frame
    iframe_viewrecipe = LabelFrame(viewrecipe, text='INGREDIENTS')
    iframe_viewrecipe.grid(row=2,column=0)
    

    #Ingredients
    iidlabel_viewrecipe = Label(iframe_viewrecipe, text= 'ITEM')
    iidlabel_viewrecipe.grid(row=0,column=1)
    #Amount
    iadlabel_viewrecipe = Label(iframe_viewrecipe, text= 'AMOUNT')
    iadlabel_viewrecipe.grid(row=0,column=2)
    #Unit
    iudlabel_viewrecipe = Label(iframe_viewrecipe, text= 'UNIT')
    iudlabel_viewrecipe.grid(row=0,column=3)
    
    #Additional Notes Frame
    anframe_viewrecipe = LabelFrame(viewrecipe, text='ADDITIONAL NOTES')
    anframe_viewrecipe.grid(row=2,column=1)
    
    #Preparation Frame
    pframe_viewrecipe = LabelFrame(viewrecipe, text='PREPARATION')
    pframe_viewrecipe.grid(row=3,column=0,columnspan=2)
    
    #Close Button
    clbutton_viewrecipe = Button(viewrecipe, text='Close',command = viewrecipe.destroy)
    clbutton_viewrecipe.grid(row=5,column=0, columnspan=2)
    
    
    vrcurs.execute('SELECT *, oid FROM basicinfo')
    currentrecord = vrcurs.fetchall()   
    for record in currentrecord:
        slabel_viewrecipe = Label(sframe_viewrecipe, text= record[1])
        slabel_viewrecipe.grid(row=0,column=0)       
        trlabel_viewrecipe = Label(trframe_viewrecipe, text= record[2])
        trlabel_viewrecipe.grid(row=0,column=0) 
        
        
    lid_gridrow = 1
    iid_gridrow = 1
    iad_gridrow = 1
    iud_gridrow = 1
        
    vrcurs.execute('SELECT *, oid FROM ingredientitems')
    currentrecord = vrcurs.fetchall()
           
    for record in currentrecord:
        iidlabel_viewrecipe = Label(iframe_viewrecipe, text= record[0])
        iidlabel_viewrecipe.grid(row=iid_gridrow,column=1)
        iid_gridrow +=1      


    vrcurs.execute('SELECT *, oid FROM ingredientamounts')
    currentrecord = vrcurs.fetchall()
    for record in currentrecord:
        iadlabel_viewrecipe = Label(iframe_viewrecipe, text= record[0])
        iadlabel_viewrecipe.grid(row=iad_gridrow,column=2)
        iad_gridrow +=1     
    
    vrcurs.execute('SELECT *, oid FROM ingredientunits')
    currentrecord = vrcurs.fetchall()  
    for record in currentrecord:
        iudlabel_viewrecipe = Label(iframe_viewrecipe, text= record[0])
        iudlabel_viewrecipe.grid(row=iud_gridrow,column=3)
        iud_gridrow +=1                

    anlabel_gridrow = 0    
    
    vrcurs.execute('SELECT *, oid FROM additionalnotes')
    currentrecord = vrcurs.fetchall()
    for record in currentrecord:
        annumber = Label(anframe_viewrecipe, text = str(anlabel_gridrow+1) +'.')
        annumber.grid(row=anlabel_gridrow, column=0)
        anlabel_viewrecipe = Label(anframe_viewrecipe, text= record[0])
        anlabel_viewrecipe.grid(row=anlabel_gridrow,column=1)
        anlabel_gridrow +=1

    plabel_gridrow = 0  
    
    vrcurs.execute('SELECT *, oid FROM preparationsteps')
    currentrecord = vrcurs.fetchall()
    for record in currentrecord:
        pnumber = Label(pframe_viewrecipe, text = str(plabel_gridrow+1)+'.')
        pnumber.grid(row=plabel_gridrow, column=0)
        plabel_viewrecipe = Label(pframe_viewrecipe, text= record[0])
        plabel_viewrecipe.grid(row=plabel_gridrow,column=1)
        plabel_gridrow +=1      
        
    vrconn.commit()
    vrconn.close()      
    
    #Edit Recipe Button
    erbutton_editrecipe = Button(viewrecipe, text='Edit',command= lambda: closeforedit(recipe))
    erbutton_editrecipe.grid(row=4,column=0, columnspan=2)

    viewrecipe.mainloop()
