from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import os
import ListRecipe
from shutil import rmtree


#Function: Add Additional Ingredient

def addingr_edit():
    global aibutton_gridrow_edit
    global aibutton_editrecipe
    global ai_gridrow_edit    
    aibutton_gridrow_edit += 1
    aibutton_location = aibutton_editrecipe.grid(row=aibutton_gridrow_edit+1,column=1,columnspan=3)    
    uniqueingrlineid = str(ai_gridrow_edit)
    
    iid= Entry(iframe_editrecipe, width=10,borderwidth=10)
    iid.grid(row=ai_gridrow_edit+1, column= 0)
    iidlist_edit.append(iid)
    
    iad = Entry(iframe_editrecipe, width=10,borderwidth=10)
    iad.grid(row=ai_gridrow_edit+1, column= 1)  
    iadlist_edit.append(iad)
    
    iud = Entry(iframe_editrecipe, width=10,borderwidth=10)
    iud.grid(row=ai_gridrow_edit+1, column= 2)
    iudlist_edit.append(iud)
    
    di = Button(iframe_editrecipe, text='X',command = lambda: deletelineingr_edit(uniqueingrlineid))
    di.grid(row=ai_gridrow_edit+1,column =3)
    dilist_edit.append(di)
    
    ai_gridrow_edit +=1


#Function: Add Additional Step
def addprep_edit():
    global apbutton_gridrow_edit
    global apbutton_editrecipe
    global aprep_gridrow_edit
    apbutton_gridrow_edit += 1
    apbutton_location_edit = apbutton_editrecipe.grid(row=apbutton_gridrow_edit,column=0,columnspan=3)
    uniquepreplineid = str(aprep_gridrow_edit)
    
    lprep = Label(pframe_editrecipe, text=f'{apbutton_gridrow_edit}')
    lprep.grid(row=aprep_gridrow_edit, column=0)
    laplist_edit.append(lprep)
    
    aprep = Entry(pframe_editrecipe, width=100,borderwidth=10)
    aprep.grid(row=aprep_gridrow_edit,column=1)
    aplist_edit.append(aprep)
    
    dp = Button(pframe_editrecipe, text='X',command = lambda: deletelineprep_edit(uniquepreplineid))
    dp.grid(row=aprep_gridrow_edit,column =2)
    dplist_edit.append(dp)
    
    aprep_gridrow_edit += 1    
  
    
#Function: Add Additional Note
def addnote_edit():
    global anbutton_gridrow_edit
    global aanbutton_editrecipe
    global anote_gridrow_edit
    anbutton_gridrow_edit += 1
    aanbutton_editrecipe.grid(row=anbutton_gridrow_edit,column=0, columnspan=3)
    uniquenotelineid = str(anote_gridrow_edit)
    
    lnote = Label(anframe_editrecipe, text=f'{anbutton_gridrow_edit}')
    lnote.grid(row=anote_gridrow_edit, column=0)        
    lanlist_edit.append(lnote)    
    
    anote = Entry(anframe_editrecipe, width=50,borderwidth=10)
    anote.grid(row=anote_gridrow_edit,column=1)
    anlist_edit.append(anote)

    dan = Button(anframe_editrecipe, text='X', command = lambda: deletelinenote_edit(uniquenotelineid))
    dan.grid(row=anote_gridrow_edit,column =2) 
    danlist_edit.append(dan)    
    
    anote_gridrow_edit += 1

def deletelinenote_edit(linenote):
    global anbutton_gridrow_edit
    global anote_gridrow_edit

    targlinenote =  int(linenote)
    newlastline = int(anbutton_gridrow_edit)-1
    
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(anlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = anlist_edit[entryboxnext+1]
            entrybox.insert(0, str(originbox.get())) 
    else:    
        for entryboxnext, entrybox in enumerate(anlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = anlist_edit[entryboxnext+2]
            entrybox.insert(0, str(originbox.get())) 
            
    lanlist_edit[-1].destroy()
    anlist_edit[-1].destroy()
    danlist_edit[-1].destroy()
    lanlist_edit.pop()
    anlist_edit.pop()
    danlist_edit.pop()
            
    anbutton_gridrow_edit -= 1
    anote_gridrow_edit -= 1
    
    
def deletelineprep_edit(lineprep):
    global apbutton_gridrow_edit
    global aprep_gridrow_edit

    targlinenote =  int(lineprep)
    newlastline = int(apbutton_gridrow_edit)-1
    
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(aplist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = aplist_edit[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:    
        for entryboxnext, entrybox in enumerate(aplist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = aplist_edit[entryboxnext+2]
            entrybox.insert(0, str(originbox.get())) 
        
    laplist_edit[-1].destroy()
    aplist_edit[-1].destroy()
    dplist_edit[-1].destroy()
    laplist_edit.pop()
    aplist_edit.pop()
    dplist_edit.pop()
            
    apbutton_gridrow_edit -= 1
    aprep_gridrow_edit -= 1
    
    
def deletelineingr_edit(lineingr):
    global aibutton_gridrow_edit
    global ai_gridrow_edit
    targlinenote =  int(lineingr)
    newlastline = int(aibutton_gridrow_edit)-1

    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(iidlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iidlist_edit[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:
        for entryboxnext, entrybox in enumerate(iidlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iidlist_edit[entryboxnext+2]
            entrybox.insert(0, str(originbox.get()))
            
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(iadlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iadlist_edit[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:                
        for entryboxnext, entrybox in enumerate(iadlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iadlist_edit[entryboxnext+2]
            entrybox.insert(0, str(originbox.get()))
       
    if targlinenote == 0:
        for entryboxnext, entrybox in enumerate(iudlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iudlist_edit[entryboxnext+1]
            entrybox.insert(0, str(originbox.get()))  
    else:                
        for entryboxnext, entrybox in enumerate(iudlist_edit[targlinenote:newlastline]):
            entrybox.delete(0,END)
            originbox = iudlist[entryboxnext+2]
            entrybox.insert(0, str(originbox.get()))
        
    iidlist_edit[-1].destroy()
    iadlist_edit[-1].destroy()
    iudlist_edit[-1].destroy()
    dilist_edit[-1].destroy()
    iidlist_edit.pop()
    iadlist_edit.pop()
    iudlist_edit.pop()
    dilist_edit.pop()
            
    aibutton_gridrow_edit -= 1
    ai_gridrow_edit -= 1

    

def canceledit():
    confirmc = messagebox.askokcancel(title= 'Confirmation' ,message= 'WARNING: All progress will be lost.' +'\n' + 'Proceed?') 
    if confirmc:
        editrecipe.destroy()
    else:
        pass


def submitcheckedit():
    global recipetitle_edit
    recipetitle_edit = rnbox_editrecipe.get()
    ingremptybox_edit = False
    amtemptybox_edit = False
    unitemptybox_edit = False
    noteemptybox_edit = False
    prepemptybox_edit = False
    
    for ingr in iidlist_edit:
        if ingr.get() == '':
            ingremptybox_edit = True
            
    for amt in iadlist_edit:
        if amt.get() == '':
            amtemptybox_edit = True
    
    for unit in iudlist_edit:
        if unit.get() == '':
            unitemptybox_edit = True
            
    for note in anlist_edit:
        if note.get() == '':
            noteemptybox_edit = True
    
    for prep in aplist_edit:
        if prep.get() == '':
            prepemptybox_edit = True
    
#add icon=**** to change icon
    if recipetitle_edit == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please enter a name for your recipe.')
    elif sbox_editrecipe.get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please specify the number of servings this recipe would produce.')
    elif trbox_editrecipe.get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please specify the estimated time required to make this dish.')
    elif iidlist_edit == []:
        messagebox.showwarning(title= 'Error' ,message= 'Please add at least one ingredient.')
    elif ingremptybox_edit:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient item box unfilled. Please fill it out before proceeding.')        
    elif amtemptybox_edit:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient amount box unfilled. Please fill it out before proceeding.')
    elif unitemptybox_edit:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient unit box unfilled. Please fill it out before proceeding.')
    elif noteemptybox_edit:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an additional note box unfilled. Please fill it out or delete all empty fields before proceeding.')
    elif aplist_edit == []:
        messagebox.showwarning(title= 'Error' ,message= 'Please add at least one preparation step.')
    elif prepemptybox_edit:
        messagebox.showwarning(title= 'Error' ,message= 'You have left a preparation step box unfilled. Please fill it out before proceeding.')
    else: 
        confirms_edit = messagebox.askokcancel(title= 'Confirmation' ,message= 'Submit changes?')
        if confirms_edit:
            submitdatabase_edit()
        else:
            pass
        
def submitdatabase_edit():
    global viewrecipe
    global old_recipedbpath_edit
    global old_recipename   
    global new_recipedbpath_edit
        
    old_recipedb = old_recipename +'.db'
    new_recipedb = rnbox_editrecipe.get() +'.db'
    
    old_recipedbpath_edit= r'./Recipes' +f'/{old_recipedb}'    
    new_recipedbpath_edit= r'./Recipes' +f'/{new_recipedb}'
    
    if os.path.exists(new_recipedbpath_edit):
        confirmo_edit = messagebox.askokcancel(title= 'Confirmation' ,message= 'There is an existing recipe with the same name.' '+\n' +' Overwrite?')        
        if not confirmo_edit:
            pass
        else:
            os.remove(old_recipedbpath_edit)
            writedatabase_edit()
    else:
        os.remove(old_recipedbpath_edit)
        writedatabase_edit()
    

def writedatabase_edit():
    global new_recipedbpath_edit
    #Open connection, create cursor
    edbconn = sqlite3.connect(new_recipedbpath_edit)
    edbcurs = edbconn.cursor()
    
    edbcurs.execute('''CREATE TABLE basicinfo (
        recipe_title text,
        servings integer,
        time text
        )
                    ''')
                    
    edbcurs.execute('''CREATE TABLE ingredientitems (
        ingredient text
        )
                    ''')   
                    
    edbcurs.execute('''CREATE TABLE ingredientamounts (
        amount integer
        )
                    ''')    
                    
    edbcurs.execute('''CREATE TABLE ingredientunits (
        unit text
        )
                    ''')    
                    
    edbcurs.execute('''CREATE TABLE additionalnotes (
        notes text
        ) 
                    ''')    
                      
    edbcurs.execute('''CREATE TABLE preparationsteps (
        steps text
        )   
                    ''')      
    
    #Seperate databases          
    edbcurs.execute("INSERT INTO basicinfo VALUES (:rtitle, :servings, :time)",
                    {
                        'rtitle' : recipetitle_edit,
                        'servings' : sbox_editrecipe.get(),
                        'time' : trbox_editrecipe.get()
        })
    
    for ingr in iidlist_edit:
        edbcurs.execute("INSERT INTO ingredientitems VALUES (:items )",
                    {
                        'items' : ingr.get()
                        })
    
    for amt in iadlist_edit:
        edbcurs.execute("INSERT INTO ingredientamounts VALUES (:amount )",
                    {
                        'amount' : amt.get()
                        })
    
    for unit in iudlist_edit:
        edbcurs.execute("INSERT INTO ingredientunits VALUES (:unit )",
                    {
                        'unit' : unit.get()
                        })
        
    for note in anlist_edit:
        edbcurs.execute("INSERT INTO additionalnotes VALUES (:notes )",
                    {
                        'notes' : note.get()
                        })
    
    for prep in aplist_edit:
        edbcurs.execute("INSERT INTO preparationsteps VALUES (:steps )",
                    {
                        'steps' : prep.get()
                        })
    #Commit changes, close connection
    edbconn.commit()
    edbconn.close()
    editrecipe.destroy()   


def editdatabase(recipe):
    print('function running')
    global editrecipe
    global old_recipename

    editrecipe = Tk()
    
    old_recipename= f'{recipe}'
    old_recipedbpath_edit = r'./Recipes' + f'/{recipe}.db'
    erconn = sqlite3.connect(old_recipedbpath_edit)
    ercurs = erconn.cursor()    
        
    ercurs.execute('SELECT *, oid FROM basicinfo')
    currentrecord = ercurs.fetchall()  
    for record in currentrecord:
        title = record[0]
        
    editrecipe.title(f'Editing recipe: {title}')
    editrecipe.iconbitmap('./resources/img/Ico.ico')

    global rnbox_editrecipe
    global sbox_editrecipe
    global trbox_editrecipe
        
    global aanbutton_editrecipe
    global anframe_editrecipe
    global lanlist_edit
    global anlist_edit
    global danlist_edit
    global anbutton_gridrow_edit
    global anote_gridrow_edit
        
    anote_gridrow_edit = 0
    anbutton_gridrow_edit = 0   
    lanlist_edit = []
    anlist_edit = []    
    danlist_edit = []   
        
    global apbutton_editrecipe
    global pframe_editrecipe
    global laplist_edit
    global aplist_edit
    global dplist_edit
    global apbutton_gridrow_edit   
    global aprep_gridrow_edit
    
    aprep_gridrow_edit = 0
    apbutton_gridrow_edit = 0   
    laplist_edit = []
    aplist_edit = []    
    dplist_edit = []   
    
    global aibutton_editrecipe
    global iframe_editrecipe
    global iidlist_edit
    global iadlist_edit
    global iudlist_edit
    global dilist_edit
    global aibutton_gridrow_edit  
    global ai_gridrow_edit
    
    ai_gridrow_edit = 0
    aibutton_gridrow_edit = 0   
    iidlist_edit = []    
    iadlist_edit = []    
    iudlist_edit = []
    dilist_edit = []   
    
    #Recipe Name Frame
    rnframe_editrecipe = LabelFrame(editrecipe, text='RECIPE NAME')
    rnframe_editrecipe.grid(row=0,column=0,columnspan=2)
    rnbox_editrecipe = Entry(rnframe_editrecipe)
    rnbox_editrecipe.insert(0,recipe)
    rnbox_editrecipe.grid(row=0,column=0)
    
    #Servings Frame
    sframe_editrecipe = LabelFrame(editrecipe, text='SERVINGS')
    sframe_editrecipe.grid(row=1,column=0)
    sbox_editrecipe = Entry(sframe_editrecipe, width=10,borderwidth=10)
    sbox_editrecipe.grid(row=0,column=0)

    #Time Required Frame
    trframe_editrecipe = LabelFrame(editrecipe, text='TIME REQUIRED')
    trframe_editrecipe.grid(row=1,column=1)
    trbox_editrecipe = Entry(trframe_editrecipe, width=10,borderwidth=10)
    trbox_editrecipe.grid(row=0,column=0)

    for record in currentrecord:
        sbox_editrecipe.insert(0, record[1])
        trbox_editrecipe.insert(0, record[2])
        
    #Ingredient Frame
    iframe_editrecipe = LabelFrame(editrecipe, text='INGREDIENTS')
    iframe_editrecipe.grid(row=2,column=0)
        
    #Descriptors 
    #Ingredients
    iidlabel_editrecipe = Label(iframe_editrecipe, text= 'ITEM')
    iidlabel_editrecipe.grid(row=0,column=0)
    #Amount
    iadlabel_editrecipe = Label(iframe_editrecipe, text= 'AMOUNT')
    iadlabel_editrecipe.grid(row=0,column=1)
    #Unit
    iudlabel_editrecipe = Label(iframe_editrecipe, text= 'UNIT')
    iudlabel_editrecipe.grid(row=0,column=2)
    
    

    #Add recipe button
    aibutton_editrecipe = Button(iframe_editrecipe, text='Add New Ingredient', command=addingr_edit)
    aibutton_location = aibutton_editrecipe.grid(row=1,column=1,columnspan=3)
    
    
    #Additional Notes Frame
    anframe_editrecipe = LabelFrame(editrecipe, text='ADDITIONAL NOTES')
    anframe_editrecipe.grid(row=2,column=1)
    #Add Note Button
    aanbutton_editrecipe = Button(anframe_editrecipe, text='Add New Note',command=addnote_edit)
    aanbutton_location = aanbutton_editrecipe.grid(row=0,column=0,columnspan=3)
    
    
    #Preparation Frame
    pframe_editrecipe = LabelFrame(editrecipe, text='PREPARATION')
    pframe_editrecipe.grid(row=3,column=0,columnspan=2)
    #Add Step Button
    apbutton_editrecipe = Button(pframe_editrecipe, text='Add New Step', command=addprep_edit)
    apbutton_location = apbutton_editrecipe.grid(row=0,column=0,columnspan=3)
    
    
    #Submit Recipe Button
    srbutton_editrecipe = Button(editrecipe, text='Submit',command=submitcheckedit)
    srbutton_editrecipe.grid(row=4,column=0, columnspan=2)
    
    
    #Cancel Button
    cbutton_editrecipe = Button(editrecipe, text='Cancel',command = canceledit)
    cbutton_editrecipe.grid(row=5,column=0, columnspan=2)
    
    
    #Throw in existing details
    ercurs.execute('SELECT *, oid FROM ingredientitems')
    currentrecord = ercurs.fetchall()
    for record in currentrecord:
        aibutton_gridrow_edit += 1
        aibutton_location = aibutton_editrecipe.grid(row=aibutton_gridrow_edit+1,column=1,columnspan=3)    
        uniqueingrlineid = str(ai_gridrow_edit)
        
        iid= Entry(iframe_editrecipe, width=10,borderwidth=10)
        iid.grid(row=ai_gridrow_edit+1, column= 0)
        iidlist_edit.append(iid)
        iid.insert(0,record[0])
        
        di = Button(iframe_editrecipe, text='X',command = lambda: deletelineingr_edit(uniqueingrlineid))
        di.grid(row=ai_gridrow_edit+1,column =3)
        dilist_edit.append(di)
        
        ai_gridrow_edit +=1    
        
    ai_gridrow_edit = 0
    
    ercurs.execute('SELECT *, oid FROM ingredientamounts')
    currentrecord = ercurs.fetchall()
    for record in currentrecord:  
        iad= Entry(iframe_editrecipe, width=10,borderwidth=10)
        iad.grid(row=ai_gridrow_edit+1, column= 1)
        iadlist_edit.append(iad)
        iad.insert(0,record[0])        
    
        ai_gridrow_edit +=1  
          
    ai_gridrow_edit = 0
    
    ercurs.execute('SELECT *, oid FROM ingredientunits')
    currentrecord = ercurs.fetchall()
    for record in currentrecord:  
        aibutton_gridrow_edit += 1
        aibutton_location = aibutton_editrecipe.grid(row=aibutton_gridrow_edit+1,column=1,columnspan=3)    
        uniqueingrlineid = str(ai_gridrow_edit)
        
        iud= Entry(iframe_editrecipe, width=10,borderwidth=10)
        iud.grid(row=ai_gridrow_edit+1, column= 2)
        iudlist_edit.append(iud)
        iud.insert(0,record[0])
        
        ai_gridrow_edit +=1            
    

    ercurs.execute('SELECT *, oid FROM additionalnotes')
    currentrecord = ercurs.fetchall()
    for record in currentrecord:      
        anbutton_gridrow_edit += 1
        aanbutton_editrecipe.grid(row=anbutton_gridrow_edit,column=0, columnspan=3)
        uniquenotelineid = str(anote_gridrow_edit)
        
        lnote = Label(anframe_editrecipe, text=f'{anbutton_gridrow_edit}')
        lnote.grid(row=anote_gridrow_edit, column=0)        
        lanlist_edit.append(lnote)    
        
        anote = Entry(anframe_editrecipe, width=50,borderwidth=10)
        anote.grid(row=anote_gridrow_edit,column=1)
        anlist_edit.append(anote)
        anote.insert(0,record[0])
    
        dan = Button(anframe_editrecipe, text='X', command = lambda: deletelinenote_edit(uniquenotelineid))
        dan.grid(row=anote_gridrow_edit,column =2) 
        danlist_edit.append(dan)    
        
        anote_gridrow_edit += 1    
        
    
    ercurs.execute('SELECT *, oid FROM preparationsteps')
    currentrecord = ercurs.fetchall()
    for record in currentrecord:        
        apbutton_gridrow_edit += 1
        apbutton_location_edit = apbutton_editrecipe.grid(row=apbutton_gridrow_edit,column=0,columnspan=3)
        uniquepreplineid = str(aprep_gridrow_edit)
        
        lprep = Label(pframe_editrecipe, text=f'{apbutton_gridrow_edit}')
        lprep.grid(row=aprep_gridrow_edit, column=0)
        laplist_edit.append(lprep)
        
        aprep = Entry(pframe_editrecipe, width=100,borderwidth=10)
        aprep.grid(row=aprep_gridrow_edit,column=1)
        aplist_edit.append(aprep)
        aprep.insert(0,record[0])
        
        dp = Button(pframe_editrecipe, text='X',command = lambda: deletelineprep_edit(uniquepreplineid))
        dp.grid(row=aprep_gridrow_edit,column =2)
        dplist_edit.append(dp)
        
        aprep_gridrow_edit += 1  
        
    
    erconn.commit()
    erconn.close()
    
    #Submit Recipe Button
    srbutton_editrecipe = Button(editrecipe, text='Submit',command=submitcheckedit)
    srbutton_editrecipe.grid(row=4,column=0, columnspan=2)
    
    
    editrecipe.mainloop
        
        

    