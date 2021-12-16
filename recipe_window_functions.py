# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:01:25 2021

@author: Ryan
"""

from tkinter import messagebox, filedialog, END
from os import path, remove
from datetime import datetime
from sqlite3 import connect
from PIL import ImageTk, Image
from appearance_config import mainbgcolor, mainfgcolor, applicationfont
from widget_creation import entryboxcreation, interactivebuttoncreation, standardbuttoncreation, labelcreation, scrollbarcanvascreation, labelframecreation


#Update scrollregion function
def scrollregionupdate(canvas,scrollframe):
    canvas.update_idletasks()
    canvas.configure(scrollregion=scrollframe.bbox('all'))

#Change servings function
def changeservings(basicinfo_entryboxlist,buttonslist,ingredientamountlist, ingredientitemlist, window, framelist):

    #Get the number of servings in old label
    oldservingsamount = basicinfo_entryboxlist[0].cget('text')

    #Delete old label
    basicinfo_entryboxlist[0].destroy()
    basicinfo_entryboxlist.pop()

    #Create new entrybox in place of that label
    entryboxcreation('Changeservingsentrybox', framelist[3], 20, 2, mainfgcolor, mainbgcolor, 'grid', 1, 0, 1, 'append', basicinfo_entryboxlist)

    #Insert old servings amount into the new entrybox
    basicinfo_entryboxlist[0].insert(0,oldservingsamount)

    #Change command and text of the 'change' button
    buttonslist[0].configure(text = 'Confirm', command = lambda: scaleservings(basicinfo_entryboxlist,buttonslist,ingredientamountlist, ingredientitemlist, window, framelist))


def scaleservings(basicinfo_entryboxlist,buttonslist,ingredientamountlist, ingredientitemlist, window, framelist):

    #Check if input in entrybox is made up of integers. If it is not, tell user to amend that mistake. Or else, continue with function.
    if not basicinfo_entryboxlist[0].get().isdigit():
        messagebox.showwarning(title= 'Error' ,message= 'Please only use integers within the servings entry box.')
        return
    else:
        #Replace entrybox with label and change the 'confirm' button back to the 'change' button
        newservingsamount = basicinfo_entryboxlist[0].get()
        buttonslist[0].configure(text = 'Change', command = lambda: changeservings(basicinfo_entryboxlist,buttonslist,ingredientamountlist, ingredientitemlist, window, framelist))
        basicinfo_entryboxlist[0].destroy()
        basicinfo_entryboxlist.pop()
        labelcreation('Servingsamount', framelist[3], newservingsamount, applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, -2, 0, 10, 'flat', 'grid', 1, 0, 1, 'center', 'append', basicinfo_entryboxlist)

        #Define original servings amount
        originalservings = ingredientitemlist[0]

        #Calculate multiplier
        scalemultiplier = float(newservingsamount) / float(originalservings)

        #Delete all old amount labels
        for label in ingredientamountlist:
            label.destroy()

        #Clear old label entries
        ingredientamountlist =[]

        #Define gridrow counter for label generation
        gridrowcounter = 2

        #Create new labels
        for amount in ingredientitemlist[1:]:
            labelcreation('ingramtlabel_viewrecipe', framelist[8], str(amount*scalemultiplier)[:5], applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 0, 0, 5, 'flat', 'grid', gridrowcounter, 1, 1, 'center', 'append', ingredientamountlist)
            gridrowcounter +=1


#Add ingredient row function
def addingr(buttonslist, framelist, canvaslist, ingritemlist, ingramtlist, ingrunitlist, ingrdeletebuttonlist, counterlist):

    print('Adding new ingredient row')

    #Define line for button to utilise in deleterow command
    uniqueingrlineid = str(counterlist[0]-1)

    #Change location of 'add ingredient' button
    buttonslist[0].grid(row=counterlist[0]+1,column=0, columnspan=4)

    #Generate entryboxes and create deletion button for that particular row
    entryboxcreation('iidbox_recipeview', framelist[8], 15, 5, mainfgcolor, mainbgcolor, 'grid', counterlist[0], 0, 1, 'append', ingritemlist)
    entryboxcreation('iadbox_recipeview', framelist[8], 15, 5, mainfgcolor, mainbgcolor, 'grid', counterlist[0], 1, 1, 'append', ingramtlist)
    entryboxcreation('iudbox_recipeview', framelist[8], 15, 5, mainfgcolor, mainbgcolor, 'grid', counterlist[0], 2, 1, 'append', ingrunitlist)
    standardbuttoncreation('cancelbutton_recipeview', framelist[8], 'X', 'Times New Roman', 12, 'bold', mainbgcolor, 'Red', mainbgcolor, mainfgcolor, 'grid', counterlist[0], 3, 1, 2, lambda: deleterow('ingredient', ingritemlist, ingramtlist, ingrunitlist, ingrdeletebuttonlist, uniqueingrlineid, counterlist, canvaslist, framelist),'append', ingrdeletebuttonlist)

    #Reduce the relevant counter by 1 to reflect the changes
    counterlist[0] +=1

    #Update the scrollregion
    scrollregionupdate(canvaslist[0],framelist[1])


#Add anote function
def addanote(buttonslist, framelist, canvaslist, anoteidlist, anotelist, anotedeletebuttonlist, counterlist):

    print('Adding new anote row')

    #Define line for button to utilise in deleterow command
    uniquenotelineid = int(counterlist[1])

    #Change location of 'add ingredient' button
    buttonslist[1].grid(row=counterlist[1]+1,column=0, columnspan=3)

    #Generate entryboxes and create deletion button for that particular row
    labelcreation('anidlabel_recipeview', framelist[9], f'{counterlist[1]+1}', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 0, 2, 2, 'flat', 'grid', counterlist[1], 0, 1, 'center','append',anoteidlist)
    entryboxcreation('anbox_recipeview', framelist[9], 65,5, mainfgcolor, mainbgcolor, 'grid', counterlist[1], 1, 1, 'append', anotelist)
    standardbuttoncreation('cancelbutton_recipeview',framelist[9],'X', 'Times New Roman', 12, 'bold', mainbgcolor, 'Red', mainbgcolor, mainfgcolor, 'grid', counterlist[1], 2, 1, 2, lambda: deleterow('anote', anoteidlist, anotelist, anotedeletebuttonlist, '', uniquenotelineid, counterlist,canvaslist, framelist),'append', anotedeletebuttonlist)

    #Reduce the relevant counter by 1 to reflect the changes
    counterlist[1] +=1

    #Update the scrollregion
    scrollregionupdate(canvaslist[0],framelist[1])


#Add preparation step row
def addstep(buttonslist, framelist, canvaslist, stepidlist, steplist, stepdeletebuttonlist, counterlist):

    print('Adding new preperation step row')

    #Define line for button to utilise in deleterow command
    uniquesteplineid = int(counterlist[2])

    #Change location of 'add ingredient' button
    buttonslist[2].grid(row=counterlist[2]+1,column=0, columnspan=3)

    #Generate entryboxes and create deletion button for that particular row
    labelcreation('apidlabel_recipeview', framelist[10], f'{counterlist[2]+1}', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 0, 2, 2, 'flat', 'grid', counterlist[2], 0, 1, 'center','append',stepidlist)
    entryboxcreation('apbox_recipeview', framelist[10],124, 5, mainfgcolor, mainbgcolor, 'grid', counterlist[2], 1, 1, 'append', steplist)
    standardbuttoncreation('cancelbutton_recipeview',framelist[10],'X', 'Times New Roman', 12, 'bold', mainbgcolor, 'Red', mainbgcolor, mainfgcolor, 'grid', counterlist[2], 2, 1, 2, lambda: deleterow('step', stepidlist, steplist, stepdeletebuttonlist, '', uniquesteplineid, counterlist,canvaslist, framelist),'append', stepdeletebuttonlist)

    #Reduce the relevant counter by 1 to reflect the changes
    counterlist[2] +=1

    #Update the scrollregion
    scrollregionupdate(canvaslist[0],framelist[1])

#Universal delete row function
def deleterow(targetbox, widgetlist1, widgetlist2, widgetlist3, widgetlist4, targetline, counterlist,canvaslist, framelist):

    #Set the line the function will start working on
    initialline = int(targetline)

    #If the target box is the ingredient box, set the counter to the ingredient counter and commence the moving of data for the two extra rows
    if targetbox == 'ingredient':
        newlastline= int(counterlist[0])-2
        print('deleting ingredient row')
        for destentrybox in widgetlist1[initialline:newlastline]:
            sourceentrybox = widgetlist1[widgetlist1.index(destentrybox)+1]
            destentrybox.delete(0,END)
            destentrybox.insert(0,str(sourceentrybox.get()))

        for destentrybox in widgetlist3[initialline:newlastline]:
            destentrybox.delete(0,END)
            sourceentrybox = widgetlist3[widgetlist3.index(destentrybox)+1]
            destentrybox.insert(0,str(sourceentrybox.get()))

    #Or else, if the target box is the anote box, set counter to the anote counter
    elif targetbox == 'anote':
        initialline = int(targetline)
        newlastline= int(counterlist[1])-1
        print('deleting anote row')

    #Or else, if the target box is the steps box, set counter to the steps counter
    elif targetbox == 'step':
        initialline = int(targetline)
        newlastline= int(counterlist[2]-1)
        print('deleting preparation step row')

    #Commence the moving of data for the entrybox rows
    for destentrybox in widgetlist2[initialline:newlastline]:
        destentrybox.delete(0,END)
        sourceentrybox = widgetlist2[widgetlist2.index(destentrybox)+1]
        destentrybox.insert(0,str(sourceentrybox.get()))

    #Destroy all relevant widget on the targeted row
    widgetlist1[-1].destroy()
    widgetlist2[-1].destroy()
    widgetlist3[-1].destroy()

    #Delete all relevant entries from their respective lists
    widgetlist1.pop()
    widgetlist2.pop()
    widgetlist3.pop()

    #If the target box is the ingredient box, delete the extra widget and their entries, and reduce the relevant counter by 1 to reflect the changes
    if targetbox == 'ingredient':
        widgetlist4[-1].destroy()
        widgetlist4.pop()
        counterlist[0] -=1

    #Or else, if the target box is the anote box, reduce the relevant counter by 1 to reflect the changes
    elif targetbox == 'anote':
        counterlist[1] -=1

    #Or else, if the target box is the steps box, reduce the relevant counter by 1 to reflect the changes
    elif targetbox == 'step':
        counterlist[2] -=1

    #Update the scrollregion
    scrollregionupdate(canvaslist[0],framelist[1])

#Addphoto function
def addphoto(windowtype, windowname, blobdata, aphinitialdirectory, framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist):

    #Set image as a global variable. NOTE: If this is not done, image will not render properly
    global finalimage

    #If the windowtype is defined as 'new', ask user to specify file to be uploaded and open the file
    if windowtype == 'new':
        windowname.filename = filedialog.askopenfilename(initialdir=aphinitialdirectory, title = 'Select An Image To Upload', filetypes =(('JPEG files','*.jpg'),('ICO files','*.ico')))
        if windowname.filename == '':
            return windowname.filename

    else:
        #Create a new temp file for this image within the resources directory and open the file
        with open('./resources/tempfile.jpg', 'wb') as imagefile:
            imagefile.write(blobdata)
        windowname.filename = './resources/tempfile.jpg'


    #Append image filepath to image filepath list
    imagepathlist.append(windowname.filename)

    #Get the selected file, and get the photo's dimensions
    uploadedimage = Image.open(windowname.filename)
    imgwidth, imgheight = uploadedimage.size

    #Define the target width of the photo
    targetwidth = 700

    #If the photo's width is less than the target width, set the image scale multiplier to 1
    if targetwidth > imgwidth:
        imagescale = 1
    #Or else, if the photo's width is more than or equal to the target width, set the image scale multiplier to accomodate for the target width
    else:
        imagescale = targetwidth / imgwidth

    #Resize the photo according to the image scale multiplier
    resized_uploadedimage = uploadedimage.resize((int(imgwidth * imagescale), int(imgheight * imagescale)), Image.ANTIALIAS)

    #Convert the resized image to a tkinter compatible image for use in label
    finalimage = ImageTk.PhotoImage(resized_uploadedimage)

    #Generate the image-bearing label
    labelcreation('image_recipeview', framelist[6], '', applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, 0, '', '', 'solid', 'grid', 0, 0, 2, 'center', 'append', imagelabellist)
    imagelabellist[-1].configure(image = finalimage)

    #Configure 'upload photo' button into a change photo button
    imagebuttonlist[0].configure(text = 'Change Photo', command = lambda: changephoto('change', windowname, aphinitialdirectory, framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist))

    #Create 'delete photo' button
    interactivebuttoncreation('dphbutton_recipeview',framelist[6], 'Delete Photo', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'grid', 2, 0, 2, 99, 2, lambda: changephoto('delete', windowname, aphinitialdirectory, framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist), 'append', imagebuttonlist)

    #Update the scrollregion
    scrollregionupdate(canvaslist[0],framelist[1])

#Change or delete photo function
def changephoto(changeordelete, windowname, aphinitialdirectory, framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist):
    #If the function is a change function, generate a new label and delete existing image data
    if changeordelete == 'change':
        addphoto('new',windowname,'', aphinitialdirectory, framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist)
        if windowname.filename =='':
            return
        imagelabellist[0].destroy()
        imagelabellist.pop(0)
        imagepathlist.pop(0)

    #Or else, if the function is a delete function, restore the 'change photo' function back to the 'upload photo' button. Delete all existing image data
    elif changeordelete == 'delete':
        imagelabellist[0].destroy()
        imagelabellist.pop(0)
        imagepathlist.pop(0)
        imagebuttonlist[1].destroy()
        imagebuttonlist.pop(1)
        imagebuttonlist[0].configure(text = 'Upload Photo', command = lambda: addphoto('new', windowname,'','.', framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist))


def submitchecks(windowtype, recipename, windowname, ingritemlist, ingramtlist, ingrunitlist, anotelist, steplist, basicinfolist, taglistboxlist, imagepathlist):
    #Define check variables
    ingremptybox = False
    amtemptybox = False
    amtnotinteger = False
    unitemptybox = False
    noteemptybox = False
    prepemptybox = False

    #Run ingredient item entrybox fill check
    for ingr in ingritemlist:
        if ingr.get() == '':
            ingremptybox = True

    #Run ingredient amount entrybox fill and digit check
    for amt in ingramtlist:
        if amt.get() == '':
            amtemptybox = True
        if not amt.get().isdigit():
            amtnotinteger = True

    #Run ingredient unit entrybox fill check
    for unit in ingrunitlist:
        if unit.get() == '':
            unitemptybox = True

    #Run anote entrybox fill check
    for note in anotelist:
        if note.get() == '':
            noteemptybox = True

    #Run preperaton step entrybox fill check
    for prep in steplist:
        if prep.get() == '':
            prepemptybox = True

    #add icon=**** to change icon
    #If the recipename entrybox is left blank, tell the user to fill it in
    if basicinfolist[0].get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please enter a name for your recipe.')

    #Or else, if the servings entrybox is left blank, tell the user to fill it in
    elif basicinfolist[1].get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please specify the number of servings this recipe would produce.')

    #Or else, if the servings entrybox is filled in with a non-integer, tell the user to only use integers
    elif not basicinfolist[1].get().isdigit():
        messagebox.showwarning(title= 'Error' ,message= 'Please only use integers within the servings entry box.')

    #Or else, if the time required entrybox is left blank, tell the user to fill it in
    elif basicinfolist[2].get() == '':
        messagebox.showwarning(title= 'Error' ,message= 'Please specify the estimated time required to make this dish.')

    #Or else, if there are no ingredients added, tell the user to add an ingredient in
    elif ingritemlist == []:
        messagebox.showwarning(title= 'Error' ,message= 'Please add at least one ingredient.')

    #Or else, if an ingredient item entrybox is left blank, tell the user to fill it in
    elif ingremptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient item box unfilled. Please fill it out before proceeding.')

    #Or else, if an ingredient amount entrybox is left blank, tell the user to fill it in
    elif amtemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient amount box unfilled. Please fill it out before proceeding.')

    #Or else, if an ingredient amount entrybox is filled in with a non-integer, tell user to only use integers
    elif amtnotinteger:
        messagebox.showwarning(title= 'Error' ,message= 'Please only use integers within the amount entry box(es).')

    #Or else, if an ingredient unit entrybox is left blank, tell the user to fill it in
    elif unitemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an ingredient unit box unfilled. Please fill it out before proceeding.')

    #Or else, if an anote entrybox is left blank, tell the user to fill it in
    elif noteemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left an additional note box unfilled. Please fill it out or delete all empty fields before proceeding.')

    #Or else, if there are no preparation steps added, tell the user to add a preparation step in
    elif steplist == []:
        messagebox.showwarning(title= 'Error' ,message= 'Please add at least one preparation step.')

    #Or else, if a preparation step entrybox is left blank, tell the user to fill it in
    elif prepemptybox:
        messagebox.showwarning(title= 'Error' ,message= 'You have left a preparation step box unfilled. Please fill it out before proceeding.')

    #Or else, confirm with user that they wish to submit the recipe
    else:
        confirmsubmit = messagebox.askokcancel(title= 'Confirmation' ,message= 'Submit recipe?')

        #If the user confirms that they wish to submit the recipe, run the database amendment function. Else, do nothing.
        if confirmsubmit:
            editdatabase(windowtype, recipename, windowname, ingritemlist, ingramtlist, ingrunitlist, anotelist, steplist, basicinfolist, taglistboxlist, imagepathlist)
        else:
            return


#Database amendment function
def editdatabase(windowtype, recipename, windowname, ingritemlist, ingramtlist, ingrunitlist, anotelist, steplist, basicinfolist, taglistboxlist, imagepathlist):

    #Define table creation check variable
    createtables = False

    #Define recipe database path
    recipedbpath = './Recipes.db'

    #If the recipe database path exists, do nothing. Else, activate the table creation check
    if path.exists(recipedbpath):
        pass
    else:
        createtables = True

    #Open connection, create cursor
    rdbconn = connect(recipedbpath)
    rdbcurs = rdbconn.cursor()

    #If the table creation check is activated, create the tables required to store the data within.
    if createtables:
        rdbcurs.executescript('''CREATE TABLE basicinfo (
            recipe_title text,
            servings integer,
            time text,
            description text,
            timecreated text,
            timelastmodified text
            );

            CREATE TABLE ingredients (
            recipe_title text,
            ingredientnumber integer,
            item text,
            amount integer,
            unit text
            );

            CREATE TABLE anotes (
            recipe_title text,
            anotenumber integer,
            anote text
            );    

            CREATE TABLE steps(
            recipe_title text,
            stepnumber integer,
            steps text
            );
            
            CREATE TABLE tags(
            recipe_title text,
            cuisine text,
            meal text,
            course text,
            diet text,
            mainingredient text,
            halalstatus text,
            kosherstatus text,
            buddhiststatus text
            );

            CREATE TABLE photos(
            recipe_title text,
            photo blob
            )
            
            ''')

    #Or else, do some additional checks
    else:
        #Set namechanged and confirm overwrite checks to false
        confirmoverwrite = False

        #If the user was editing a recipe, check if the recipe name has changed
        if windowtype == 'editing':
            #If the name has changed, set the target deletion name to the old name
            targetdeletionname = recipename
        #Or else if it is a new recipe, check if an entry with the same recipe name exists within the database
        elif windowtype =='new':
            rdbcurs.execute(''' SELECT recipe_title FROM basicinfo WHERE recipe_title = ?''', (f'{basicinfolist[0].get()}',))
            result=rdbcurs.fetchone()
            #If one such entry exists, ask user if they wish to overwrite that entry
            if result:
                confirmoverwrite = messagebox.askokcancel(title= 'Confirmation' ,message= 'There is an existing recipe with the same name.' '+\n' +' Overwrite?')
                #If an overwrite is authorised by the user, set the target deletion name to the current name
                if confirmoverwrite:
                    targetdeletionname = basicinfolist[0].get()
                else:
                    return
        #If the user is editing a recipe, preserve the time created
        if windowtype == 'editing':
            databasefetch(recipename, rdbcurs, 'basicinfo')
            timerecord = rdbcurs.fetchone()
            timecreatedoriginal = timerecord[4]

        #If they wish to overwrite it, then delete all relevant entries from all tables with the recipe name as the primary key. If not, do nothing.
        if confirmoverwrite or windowtype == 'editing':
            rdbcurs.execute('''DELETE FROM basicinfo WHERE recipe_title = ?''', (f'{targetdeletionname}',))
            rdbcurs.execute('''DELETE FROM ingredients WHERE recipe_title = ?''', (f'{targetdeletionname}',))
            rdbcurs.execute('''DELETE FROM anotes WHERE recipe_title = ?''', (f'{targetdeletionname}',))
            rdbcurs.execute('''DELETE FROM steps WHERE recipe_title = ?''', (f'{targetdeletionname}',))
            rdbcurs.execute('''DELETE FROM tags WHERE recipe_title = ?''', (f'{targetdeletionname}',))
            rdbcurs.execute('''DELETE FROM photos WHERE recipe_title = ?''', (f'{targetdeletionname}',))

    #Define a variable as the current time
    timenow = datetime.now()

    #If this is a new recipe, set the time created as now and the time modified as ''
    if windowtype == 'new':
        timecreatedoriginal = timenow.strftime("%d/%m/%Y , %H:%M:%S")
        #Set time modified as nil
        timemodified = ''

    #If not, use the pre-existing original time created and set the time modified as the current time
    else:
        timemodified = timenow.strftime("%d/%m/%Y , %H:%M:%S")



    #Insert the recipe name, servings produced, and time required for the dish into the basicinfo table
    rdbcurs.execute('''INSERT INTO basicinfo VALUES (:recipe_title, :servings, :time, :description, :timecreated, :timelastmodified)''',
                        {'recipe_title' : basicinfolist[0].get(),
                         'servings' : basicinfolist[1].get(),
                         'time' : basicinfolist[2].get(),
                         'description' : basicinfolist[3].get('1.0',END),
                         'timecreated' : timecreatedoriginal,
                         'timelastmodified' : timemodified
                         })


    #Insert ingredient information from the ingredient lists into the ingredient table
    for ingr in ingritemlist:
        rdbcurs.execute('''INSERT INTO ingredients VALUES (:recipe_title, :ingredientnumber, :item, :amount, :unit)''',
                        {'recipe_title': basicinfolist[0].get(),
                         'ingredientnumber': ingritemlist.index(ingr)+1,
                         'item' : ingr.get(),
                         'amount': int(ingramtlist[ingritemlist.index(ingr)].get()),
                         'unit': ingrunitlist[ingritemlist.index(ingr)].get()})
        print('Adding ingredient to database')

    #Insert anote information from the anote lists into the anotes table
    for anote in anotelist:
        rdbcurs.execute("INSERT INTO anotes VALUES (:recipe_title, :anotenumber,:anote)",
                        {'recipe_title':  basicinfolist[0].get(),
                         'anotenumber': int(anotelist.index(anote)+1),
                         'anote': anote.get()})
        print('Adding note to database')

    #Insert step information from the step lists into the steps table
    for step in steplist:
        rdbcurs.execute("INSERT INTO steps VALUES (:recipe_title, :stepnumber,:step)",
                        {'recipe_title':  basicinfolist[0].get(),
                         'stepnumber': int(steplist.index(step)+1),
                         'step': step.get()})
        print('Adding step to database')

    rdbcurs.execute('''INSERT INTO tags VALUES (:recipe_title, :cuisine, :meal, :course, :diet, :mainingredient, :halalstatus, :kosherstatus, :buddhiststatus)''',
                        {'recipe_title' : basicinfolist[0].get(),
                         'cuisine' : taglistboxlist[0].get(),
                         'meal' : taglistboxlist[1].get(),
                         'course' : taglistboxlist[2].get(),
                         'diet' : taglistboxlist[3].get(),
                         'mainingredient' : taglistboxlist[4].get(),
                         'halalstatus' : taglistboxlist[5].get(),
                         'kosherstatus' : taglistboxlist[6].get(),
                         'buddhiststatus' : taglistboxlist[7].get()
                         })
    if imagepathlist == []:
        pass
    else:
        for photopath in imagepathlist:
            databasephoto =  open(photopath, 'rb')

            photoblobdata = databasephoto.read()

            rdbcurs.execute("INSERT INTO photos VALUES (:recipe_title, :photo)",
                            {'recipe_title':  basicinfolist[0].get(),
                             'photo': photoblobdata
                             })
            print('Image added to database')

    #Commit changes, close connection
    rdbconn.commit()
    rdbconn.close()

    #Close the window
    windowname.destroy()


#Close window function
def closewindow(windowname):

    #Confirm with user that they wish to close the window
    confirmcancel = messagebox.askokcancel(title= 'Confirmation' ,message= 'WARNING: All progress will be lost.' +'\n' + 'Proceed?')

    #If the user confirms that they wish to close the window, close it. Else, do nothing.
    if confirmcancel:
        windowname.destroy()

        #If the tempfile exists, delete it
        if path.exists('./resources/tempfile.jpg'):
            remove('./resources/tempfile.jpg')
    else:
        pass

#Window layout creation function
def windowlayoutcreation(windowtype,window, framelist, canvaslist, basicinfo_entryboxlist, buttonslist,ingredientamountlist, ingredientitemlist):

    #Assign canvas dimensions, labelgridrows, label creations, and headernames based on the window type specified
    if windowtype in ('new', 'editing'):
        canvaswidth = 1000
        canvasheight = 800
        rnframeheader = 'RECIPE NAME'
        sheader = 'SERVINGS'
        trheader = 'TIME REQUIRED'
        ingrheader = 'INGREDIENTS'
        tagheader = 'TAGS'
        descheader = 'DESCRIPTION'
        anheader = 'ADDITIONAL NOTES'
        pheader = 'PREPARATION STEPS'
        ingrlabelgridrows = 0
        itemandunitheaderwidth = 13
        amountheaderwidth = itemandunitheaderwidth


    elif windowtype == 'viewing':
        canvaswidth= 968
        canvasheight=900
        rnframeheader = ''
        sheader = ''
        trheader = ''
        tagheader = ''
        descheader = ''
        ingrheader = ''
        anheader = ''
        pheader = ''
        ingrlabelgridrows = 1
        itemandunitheaderwidth= 23
        amountheaderwidth=8


    #Generate frame, canvas, and scroll frame to host widgets
    #Generate scrollbar and scrollbarcanvas
    scrollbarcanvascreation('infoframe',window,'sb','canvas','scrollframe',framelist, canvaslist, canvaswidth, canvasheight,'vertical', 'alt', mainfgcolor, mainbgcolor, mainbgcolor, mainbgcolor, mainfgcolor, 'pack', 1,1,1)

    #Generate label frames to contain input boxes and widgets
    #Recipe name label frame
    labelframecreation('rnframe',framelist[1], rnframeheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 0,0, 2, 'append', framelist)

    #Servings label frame
    labelframecreation('sframe',framelist[1], sheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 1,0, 1, 'append', framelist)

    #Time required frame
    labelframecreation('trframe',framelist[1], trheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 1,1, 1, 'append', framelist)

    #Tag frame
    labelframecreation('tagframe',framelist[1], tagheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 0,0, 1, 'append', framelist)

    #Photo frame
    labelframecreation('photoframe',framelist[1], '', applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 2,0, 2, 'append', framelist)

    #Description frame
    labelframecreation('descframe',framelist[1], descheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 3,0, 2, 'append', framelist)

    #Ingredients frame
    labelframecreation('iframe',framelist[1], ingrheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 4,0, 1, 'append', framelist)
    #Ingredient headers
    labelcreation('itemheader', framelist[8], 'ITEM', applicationfont, 10, 'italic', mainfgcolor, mainbgcolor, 4, 1, itemandunitheaderwidth, 'groove', 'grid', ingrlabelgridrows, 0, 1, 'center','','')
    labelcreation('amountheader', framelist[8], 'AMOUNT', applicationfont, 10, 'italic', mainfgcolor, mainbgcolor, 4, 1, amountheaderwidth, 'groove', 'grid', ingrlabelgridrows, 1, 1, 'center','','')
    labelcreation('unitheader', framelist[8], 'UNIT', applicationfont, 10, 'italic', mainfgcolor, mainbgcolor, 4, 1, itemandunitheaderwidth, 'groove', 'grid', ingrlabelgridrows, 2, 1, 'center','','')

    #Additional notes frame
    labelframecreation('anframe',framelist[1], anheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 4,1, 1, 'append', framelist)

    #Preparation steps frame
    labelframecreation('pframe',framelist[1], pheader, applicationfont, 12, 'bold', 'groove',mainfgcolor, mainbgcolor, 'grid', 5,0, 2, 'append', framelist)

    #Generate headers if window is used to view a recipe. Additionally, generate a change servings button
    if windowtype == 'viewing':
        labelframecreation('datetimeframe',framelist[1], '', applicationfont, 12, 'bold', 'flat',mainfgcolor, mainbgcolor, 'grid', 7,0, 2, 'append', framelist)
        labelcreation('Servings', framelist[3], 'Servings', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 20, 'flat', 'grid', 0, 0, 1, 'center','','')
        interactivebuttoncreation('Changeservings', framelist[3], 'Change', applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 'grid', 2, 0, 1, 23, 0, lambda: changeservings(basicinfo_entryboxlist,buttonslist,ingredientamountlist, ingredientitemlist, window, framelist), 'append', buttonslist)
        labelcreation('Timerequired', framelist[4], 'Time Required', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 20, 'flat', 'grid', 0, 0, 1, 'center','','')
        labelcreation('Timerequiredpadding', framelist[4], ' ', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 4, 0, 20, 'flat', 'grid', 2, 0, 1, 'center','','')
        labelcreation('Tags', framelist[5], 'Tags:', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 6, 'flat', 'grid', 0, 0, 1, 'center','','')
        labelcreation('Description', framelist[7], 'Description:', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 100, 'flat', 'grid', 0, 0, 1, 'center','','')
        labelcreation('Ingredients', framelist[8], 'Ingredients', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 50, 'flat', 'grid', 0, 0, 3, 'center','','')
        labelcreation('Additionalnotes', framelist[9], 'Additional Notes', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 67, 'flat', 'grid', 0, 0, 3, 'center','','')
        labelcreation('Preparationsteps', framelist[10], 'Preparation Steps', applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, 4, 1, 119, 'flat', 'grid', 0, 0, 2, 'center','','')
        framelist[5].grid(columnspan=2, row = 6, column=0, padx=10)
    else:
        framelist[5].grid(rowspan=len(framelist)-5, row = 0, column = 2, sticky='n')

    #If the tempfile exists, delete it
    #if path.exists('./resources/tempfile.jpg'):
        #remove('./resources/tempfile.jpg')

#Database fetch function
def databasefetch(recipename, cursor, databasetable):

    #Assign command based on the table specified in the command
    if databasetable == 'basicinfo':
        executecommand = '''SELECT * from basicinfo
                    JOIN ingredients ON ingredients.recipe_title = basicinfo.recipe_title
                    WHERE basicinfo.recipe_title = ?
                    ORDER BY ingredientnumber ASC
                    '''
    elif databasetable == 'anote':
        executecommand = '''SELECT * from anotes
                    WHERE recipe_title = ?
                    ORDER BY anotenumber ASC
                    '''
    elif databasetable == 'steps':
        executecommand = '''SELECT * from steps
                    WHERE recipe_title = ?
                    ORDER BY stepnumber ASC
                    '''
    elif databasetable == 'tags':
        executecommand = '''SELECT * from tags
                    WHERE recipe_title = ?
                    '''
    elif databasetable == 'photos':
        executecommand = '''SELECT * from photos
                    WHERE recipe_title = ?
                    '''
    #Execute the command
    cursor.execute(executecommand,(f'{recipename}',))
