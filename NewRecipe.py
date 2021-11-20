# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 02:40:29 2021

@author: Ryan
"""
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import os

#Function: Add Additional Ingredient
def addingr():
    global aibutton_gridrow
    global aibutton_newrecipe
    global ai_gridrow    
    aibutton_gridrow += 1
    aibutton_location = aibutton_newrecipe.grid(row=aibutton_gridrow+1,column=1,columnspan=3)    
    uniqueingrlineid = str(ai_gridrow)
    
    iid= Entry(iframe_newrecipe, width=10,borderwidth=10)
    iid.grid(row=ai_gridrow+1, column= 0)
    iidlist.append(iid)
    
    iad = Entry(iframe_newrecipe, width=10,borderwidth=10)
    iad.grid(row=ai_gridrow+1, column= 1)  
    iadlist.append(iad)
    
    iud = Entry(iframe_newrecipe, width=10,borderwidth=10)
    iud.grid(row=ai_gridrow+1, column= 2)
    iudlist.append(iud)
    
    di = Button(iframe_newrecipe, text='X',command = lambda: deletelineingr(uniqueingrlineid))
    di.grid(row=ai_gridrow+1,column =3)
    dilist.append(di)
    
    ai_gridrow +=1


#Function: Add Additional Step
def addprep():
    global apbutton_gridrow
    global apbutton_newrecipe
    global aprep_gridrow
    apbutton_gridrow += 1
    apbutton_location = apbutton_newrecipe.grid(row=apbutton_gridrow,column=0,columnspan=3)
    uniquepreplineid = str(aprep_gridrow)
    
    lprep = Label(pframe_newrecipe, text=f'{apbutton_gridrow}')
    lprep.grid(row=aprep_gridrow, column=0)
    laplist.append(lprep)
    
    aprep = Entry(pframe_newrecipe, width=100,borderwidth=10)
    aprep.grid(row=aprep_gridrow,column=1)
    aplist.append(aprep)
    
    dp = Button(pframe_newrecipe, text='X',command = lambda: deletelineprep(uniquepreplineid))
    dp.grid(row=aprep_gridrow,column =2)
    dplist.append(dp)
    
    aprep_gridrow += 1    
  
    
#Function: Add Additional Note
def addnote():
    global anbutton_gridrow
    global aanbutton_newrecipe
    global anote_gridrow
    anbutton_gridrow += 1
    aanbutton_newrecipe.grid(row=anbutton_gridrow,column=0, columnspan=3)
    uniquenotelineid = str(anote_gridrow)
    
    lnote = Label(anframe_newrecipe, text=f'{anbutton_gridrow}')
    lnote.grid(row=anote_gridrow, column=0)        
    lanlist.append(lnote)    
    
    anote = Entry(anframe_newrecipe, width=50,borderwidth=10)
    anote.grid(row=anote_gridrow,column=1)
    anlist.append(anote)

    dan = Button(anframe_newrecipe, text='X', command = lambda: deletelinenote(uniquenotelineid))
    dan.grid(row=anote_gridrow,column =2) 
    danlist.append(dan)    
    
    anote_gridrow += 1

def deletelinenote(linenote):
    global anbutton_gridrow
    global anote_gridrow

    targlinenote =  int(linenote)
    newlastline = int(anbutton_gridrow)-1
    print(targlinenote)
    print(newlastline)
    
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(anlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = anlist[entryboxnext+1]
            entrybox.insert(0, str(originbox.get())) 
    else:
        for entryboxnext, entrybox in enumerate(anlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = anlist[entryboxnext+2]
            entrybox.insert(0, str(originbox.get())) 

        
    lanlist[-1].destroy()
    anlist[-1].destroy()
    danlist[-1].destroy()
    lanlist.pop()
    anlist.pop()
    danlist.pop()
            
    anbutton_gridrow -= 1
    anote_gridrow -= 1
    
    
def deletelineprep(lineprep):
    global apbutton_gridrow
    global aprep_gridrow

    targlinenote =  int(lineprep)
    newlastline = int(apbutton_gridrow)-1
    
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(aplist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = aplist[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:
        for entryboxnext, entrybox in enumerate(aplist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = aplist[entryboxnext+2]
            entrybox.insert(0, str(originbox.get())) 
    laplist[-1].destroy()
    aplist[-1].destroy()
    dplist[-1].destroy()
    laplist.pop()
    aplist.pop()
    dplist.pop()
            
    apbutton_gridrow -= 1
    aprep_gridrow -= 1
    
    
def deletelineingr(lineingr):
    global aibutton_gridrow
    global ai_gridrow
    print(lineingr)
    targlinenote =  int(lineingr)
    newlastline = int(aibutton_gridrow)-1
    
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(iidlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iidlist[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:
        for entryboxnext, entrybox in enumerate(iidlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iidlist[entryboxnext+2]
            entrybox.insert(0, str(originbox.get()))
            print(originbox)
            
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(iadlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iadlist[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:        
        for entryboxnext, entrybox in enumerate(iadlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iadlist[entryboxnext+2]
            entrybox.insert(0, str(originbox.get()))
            print(originbox)
            
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(iudlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iudlist[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:        
        for entryboxnext, entrybox in enumerate(iudlist[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iudlist[entryboxnext+2]
            entrybox.insert(0, str(originbox.get()))
        
    iidlist[-1].destroy()
    iadlist[-1].destroy()
    iudlist[-1].destroy()
    dilist[-1].destroy()
    iidlist.pop()
    iadlist.pop()
    iudlist.pop()
    dilist.pop()
            
    aibutton_gridrow -= 1
    ai_gridrow -= 1

    
#Function: Submit Recipe to Database
def submitcheck():
    #Create new database file based on recipe title. NOTE INSTALL OS modules
    global recipetitle
    recipetitle = rnbox_newrecipe.get()
    ingremptybox = False
    amtemptybox = False
    unitemptybox = False
    noteemptybox = False
    prepemptybox = False
    
    
    for ingr in iidlist:
        if ingr.get() == '':
            ingremptybox = True
            
    for amt in iadlist:
        if amt.get() == '':
            amtemptybox = True
    
    for unit in iudlist:
        if unit.get() == '':
            unitemptybox = True
            
    for note in anlist:
        if note.get() == '':
            noteemptybox = True
    
    for prep in aplist:
        if prep.get() == '':
            prepemptybox = True
    
#add icon=**** to change icon
    if recipetitle == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please enter a name for your recipe.')
    elif sbox_newrecipe.get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please specify the number of servings this recipe would produce.')
    elif trbox_newrecipe.get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please specify the estimated time required to make this dish.')
    elif iidlist == []:
        messagebox.showwarning(title= 'Error' ,message= 'Please add at least one ingredient.')
    elif ingremptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient item box unfilled. Please fill it out before proceeding.')        
    elif amtemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient amount box unfilled. Please fill it out before proceeding.')
    elif unitemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient unit box unfilled. Please fill it out before proceeding.')
    elif noteemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an additional note box unfilled. Please fill it out or delete all empty fields before proceeding.')
    elif aplist == []:
        messagebox.showwarning(title= 'Error' ,message= 'Please add at least one preparation step.')
    elif prepemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left a preparation step box unfilled. Please fill it out before proceeding.')
    else: 
        confirms = messagebox.askokcancel(title= 'Confirmation' ,message= 'Submit recipe?')
        if confirms:
            submitdatabase()
        else:
            pass
        
        
def submitdatabase():
    global recipedbpath
    recipedbpath = r'./Recipes' + f'/{recipetitle}.db'
    if os.path.exists(recipedbpath):
        confirmo = messagebox.askokcancel(title= 'Confirmation' ,message= 'There is an existing recipe with the same name.' '+\n' +' Overwrite?')        
        if not confirmo:
            pass
        else:
            os.remove(recipedbpath)
            writedatabase()
    else:
        writedatabase()

def writedatabase():
    
    global recipedbpath
    #Open connection, create cursor
    rdbconn = sqlite3.connect(recipedbpath)
    rdbcurs = rdbconn.cursor()
    
    rdbcurs.execute('''CREATE TABLE basicinfo (
        recipe_title text,
        servings integer,
        time text
        )
                    ''')
                    
    rdbcurs.execute('''CREATE TABLE ingredientitems (
        ingredient text
        )
                    ''')   
                    
    rdbcurs.execute('''CREATE TABLE ingredientamounts (
        amount integer
        )
                    ''')    
                    
    rdbcurs.execute('''CREATE TABLE ingredientunits (
        unit text
        )
                    ''')    
                    
    rdbcurs.execute('''CREATE TABLE additionalnotes (
        notes text
        ) 
                    ''')    
                      
    rdbcurs.execute('''CREATE TABLE preparationsteps (
        steps text
        )   
                    ''')    
    #Seperate databases          
    rdbcurs.execute("INSERT INTO basicinfo VALUES (:rtitle, :servings, :time)",
                    {
                        'rtitle' : recipetitle,
                        'servings' : sbox_newrecipe.get(),
                        'time' : trbox_newrecipe.get()
        })
    
    for ingr in iidlist:
        rdbcurs.execute("INSERT INTO ingredientitems VALUES (:items )",
                    {
                        'items' : ingr.get()
                        })
    
    for amt in iadlist:
        rdbcurs.execute("INSERT INTO ingredientamounts VALUES (:amount )",
                    {
                        'amount' : amt.get()
                        })
    
    for unit in iudlist:
        rdbcurs.execute("INSERT INTO ingredientunits VALUES (:unit )",
                    {
                        'unit' : unit.get()
                        })
        
    for note in anlist:
        rdbcurs.execute("INSERT INTO additionalnotes VALUES (:notes )",
                    {
                        'notes' : note.get()
                        })
    
    for prep in aplist:
        rdbcurs.execute("INSERT INTO preparationsteps VALUES (:steps )",
                    {
                        'steps' : prep.get()
                        })
    #Commit changes, close connection
    rdbconn.commit()
    rdbconn.close()
    newrecipe.destroy()
    

def cancelcreation():
    confirmc = messagebox.askokcancel(title= 'Confirmation' ,message= 'WARNING: All progress will be lost.' +'\n' + 'Proceed?') 
    if confirmc:
        newrecipe.destroy()
    else:
        pass
                                                        
#Function: Submit New Recipe
def submitnewrecipe():
    
    global newrecipe
    
    newrecipe = Tk()
    newrecipe.title('Submit New Recipe')
    newrecipe.iconbitmap('./resources/img/Ico.ico')
    #newrecipe.geometry('600x900')
    global rnbox_newrecipe
    global sbox_newrecipe
    global trbox_newrecipe
    
    global aanbutton_newrecipe
    global anframe_newrecipe
    global lanlist
    global anlist
    global danlist
    global anbutton_gridrow
    global anote_gridrow
    
    anote_gridrow = 0
    anbutton_gridrow = 0   
    lanlist = []
    anlist = []    
    danlist = []   
    
    global apbutton_newrecipe
    global pframe_newrecipe
    global laplist
    global aplist
    global dplist
    global apbutton_gridrow   
    global aprep_gridrow
    
    aprep_gridrow = 0
    apbutton_gridrow = 0   
    laplist = []
    aplist = []    
    dplist = []   
    
    global aibutton_newrecipe
    global iframe_newrecipe
    global iidlist
    global iadlist
    global iudlist
    global dilist
    global aibutton_gridrow   
    global ai_gridrow
    
    ai_gridrow = 0
    aibutton_gridrow = 0   
    iidlist = []    
    iadlist = []    
    iudlist = []
    dilist = []    
    
    #Recipe Name Frame
    rnframe_newrecipe = LabelFrame(newrecipe, text='RECIPE NAME')
    rnframe_newrecipe.grid(row=0,column=0,columnspan=2)
    rnbox_newrecipe = Entry(rnframe_newrecipe, width=100,borderwidth=10)
    rnbox_newrecipe.grid(row=0,column=0)
    
    #Servings Frame
    sframe_newrecipe = LabelFrame(newrecipe, text='SERVINGS')
    sframe_newrecipe.grid(row=1,column=0)
    sbox_newrecipe = Entry(sframe_newrecipe, width=10,borderwidth=10)
    sbox_newrecipe.grid(row=0,column=0)
    
    
    #Time Required Frame
    trframe_newrecipe = LabelFrame(newrecipe, text='TIME REQUIRED')
    trframe_newrecipe.grid(row=1,column=1)
    trbox_newrecipe = Entry(trframe_newrecipe, width=10,borderwidth=10)
    trbox_newrecipe.grid(row=0,column=0)
    
    
    #Ingredient Frame
    iframe_newrecipe = LabelFrame(newrecipe, text='INGREDIENTS')
    iframe_newrecipe.grid(row=2,column=0)
    
    #Descriptors 
    #Ingredients
    iidlabel_newrecipe = Label(iframe_newrecipe, text= 'ITEM')
    iidlabel_newrecipe.grid(row=0,column=0)
    #Amount
    iadlabel_newrecipe = Label(iframe_newrecipe, text= 'AMOUNT')
    iadlabel_newrecipe.grid(row=0,column=1)
    #Unit
    iudlabel_newrecipe = Label(iframe_newrecipe, text= 'UNIT')
    iudlabel_newrecipe.grid(row=0,column=2)

    #Add recipe button
    aibutton_newrecipe = Button(iframe_newrecipe, text='Add New Ingredient', command=addingr)
    aibutton_location = aibutton_newrecipe.grid(row=1,column=1,columnspan=3)
    
    
    #Additional Notes Frame
    anframe_newrecipe = LabelFrame(newrecipe, text='ADDITIONAL NOTES')
    anframe_newrecipe.grid(row=2,column=1)
    #Add Note Button
    aanbutton_newrecipe = Button(anframe_newrecipe, text='Add New Note',command=addnote)
    aanbutton_location = aanbutton_newrecipe.grid(row=0,column=0,columnspan=3)
    
    
    #Preparation Frame
    pframe_newrecipe = LabelFrame(newrecipe, text='PREPARATION')
    pframe_newrecipe.grid(row=3,column=0,columnspan=2)
    #Add Step Button
    apbutton_newrecipe = Button(pframe_newrecipe, text='Add New Step', command=addprep)
    apbutton_location = apbutton_newrecipe.grid(row=0,column=0,columnspan=3)
    
    
    #Submit Recipe Button
    srbutton_newrecipe = Button(newrecipe, text='Submit',command=submitcheck)
    srbutton_newrecipe.grid(row=4,column=0, columnspan=2)
    
    
    #Cancel Button
    cbutton_newrecipe = Button(newrecipe, text='Cancel',command = cancelcreation)
    cbutton_newrecipe.grid(row=5,column=0, columnspan=2)
    
    
    newrecipe.mainloop()


    
    