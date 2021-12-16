# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 05:02:58 2021

@author: Ryan
"""
from tkinter import Toplevel, Label, END
from sqlite3 import connect
from PIL import ImageTk, Image
from appearance_config import mainbgcolor, mainfgcolor, applicationfont
from widget_creation import  windowconfiguration, textboxcreation, dropdownboxcreation, interactivebuttoncreation, entryboxcreation, labelcreation
from recipe_window_functions import scrollregionupdate, windowlayoutcreation, addphoto, closewindow, addingr, addanote, addstep, submitchecks, databasefetch


#Edit recipe window switch functions
def editwindowtransit(windowname, recipename):
    #Destroy the recipe view window
    windowname.destroy()
    #Generate edit recipe window
    recipeview('editing', recipename)

#View recipe widget creation function
def viewrecipewidgetcreation(windowname, recipename, framelist, canvaslist, basicinfolist, ingritemlist, ingramtlist):

    #Define recipe database path
    recipedbpath = './Recipes.db'

    #Open connection, create cursor
    vdbconn = connect(recipedbpath)
    vdbcurs = vdbconn.cursor()

    #Fetch data from basicinfo and ingredient table
    databasefetch(recipename, vdbcurs, 'basicinfo')
    currentrecord = vdbcurs.fetchall()
    timedetailstext = f'Created on {currentrecord[0][4]}'
    if currentrecord[0][5] != '':
        timedetailstext +=  f'  //  Last modified on {currentrecord[0][5]}'

    #Generate basicinfo labels
    labelcreation('rnlabel_recipeview', framelist[2], currentrecord[0][0], applicationfont, 12, 'bold', mainbgcolor, mainfgcolor, -2, 0, 120, 'flat', 'grid', 0, 0, 1, 'center', '', '')
    labelcreation('slabel_recipeview', framelist[3], currentrecord[0][1], applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, -2, 0, 10, 'flat', 'grid', 1, 0, 1, 'center', 'append', basicinfolist)
    labelcreation('trlabel_recipeview', framelist[4], currentrecord[0][2], applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, -2, 0, 10, 'flat', 'grid', 1, 0, 1, 'center', '', '')
    textboxcreation('desclabel_recipeview', framelist[7], mainbgcolor, mainfgcolor, 10, 100, 2, 'grid', 1, 0, 1, 'readonly','insert',currentrecord[0][3], '', '')
    labelcreation('cuisinelabel_viewrecipe', framelist[11], timedetailstext, applicationfont, 10, 'italic', mainfgcolor, mainbgcolor, 2, '', '', 'flat', 'grid', 0, 1, 1, 'w', '', '')

    #Append initial serving info into list for scale serving function
    ingritemlist.append(currentrecord[0][1])

    #Define gridrow counter for use in ingredient label creation
    gridrowcounter = 2

    #Generate ingredient labels
    for ingredient in currentrecord:
        labelcreation('ingritemlabel_viewrecipe', framelist[8], ingredient[8], applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 0, 0, 23, 'flat', 'grid', gridrowcounter, 0, 1, 'center', '', '')
        labelcreation('ingramtlabel_viewrecipe', framelist[8], ingredient[9], applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 0, 0, 8, 'flat', 'grid', gridrowcounter, 1, 1, 'center', 'append', ingramtlist)
        labelcreation('ingrunitlabel_viewrecipe', framelist[8], ingredient[10], applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 0, 0, 23, 'flat', 'grid', gridrowcounter, 2, 1, 'center', '', '')
        ingritemlist.append(ingredient[9])
        gridrowcounter +=1

    #Reset gridrow counter for next label creation use
    gridrowcounter = 1

    #Fetch data from anote table
    databasefetch(recipename, vdbcurs, 'anote')
    currentrecord = vdbcurs.fetchall()

    #If there are not anotes, generate a label to insert into the anote frame indicating this. Or else, generate anote labels
    if currentrecord == []:
        labelcreation('anotelabel_viewrecipe', framelist[9], 'There are no notes for this recipe :(', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 0, 0, 50, 'flat', 'grid', gridrowcounter, 1, 1, 'center', '', '')
    else:
        for anote in currentrecord:
            idtext = f'{anote[1]}.'
            labelcreation('anoteidlabel_viewrecipe', framelist[9], idtext, applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 0, 0, 2, 'flat', 'grid', gridrowcounter, 0, 1, 'w', '', '')
            labelcreation('anotelabel_viewrecipe', framelist[9], anote[2], applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 0, 0, 75, 'flat', 'grid', gridrowcounter, 1, 1, 'w', '', '')
            gridrowcounter +=1
        #Reset gridrow counter for steps label creation use
        gridrowcounter = 1

    #Fetch data from steps table
    databasefetch(recipename, vdbcurs, 'steps')
    currentrecord = vdbcurs.fetchall()

    #Generate steps labels
    for step in currentrecord:
        idtext = f'{step[1]}.'
        labelcreation('stepidlabel_viewrecipe', framelist[10], idtext, applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 0, 0, 2, 'flat', 'grid', gridrowcounter, 0, 1, 'w', '', '')
        labelcreation('steplabel_viewrecipe', framelist[10], step[2], applicationfont, 10, 'normal', mainfgcolor, mainbgcolor, 0, 0, 135, 'flat', 'grid', gridrowcounter, 1, 1, 'w', '', '')
        gridrowcounter +=1

    #Generate tag label
    databasefetch(recipename, vdbcurs, 'tags')
    currentrecord = vdbcurs.fetchall()
    tagstext = ''
    for record in currentrecord:
        for tag in record[1:]:
            if tag !='Uncategorised':
                if tagstext == '':
                    tagstext += f' {tag}'
                else:
                    tagstext += f' / {tag}'

    if tagstext == '':
        tagstext = ' This recipe has no tags :('

    labelcreation('cuisinelabel_viewrecipe', framelist[5], tagstext, applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, 2, 0, 110, 'flat', 'grid', 0, 1, 1, 'w', '', '')


    #Fetch data from photos table
    databasefetch(recipename, vdbcurs, 'photos')
    currentrecord = vdbcurs.fetchall()
    #If there is no photo, generate a label telling users of this
    if currentrecord == []:
        labelcreation('photo_viewrecipe', framelist[6], 'This recipe has no attached photo :(', applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, 0, 0, 100, 'flat', 'grid', 0, 0, 1, 'n', '', '')
    else:
        for record in currentrecord:
            global finalrecipeimage

            #Define photo data
            blobdata = record[1]

            #Create temporary file for the image
            with open('./resources/tempfile.jpg', 'wb') as imagefile:
                imagefile.write(blobdata)

            #Open the temporary file
            filename = './resources/tempfile.jpg'
            recipeimage = Image.open(filename)

            #Get the size of the photo
            imgwidth, imgheight = recipeimage.size
            #Define the target width of the photo
            targetwidth = 900

            #If the photo's width is less than the target width, set the image scale multiplier to 1
            if targetwidth > imgwidth:
                imagescale = 1
            #Or else, if the photo's width is more than or equal to the target width, set the image scale multiplier to accomodate for the target width
            else:
                imagescale = targetwidth / imgwidth

            #Resize the photo according to the image scale multiplier
            resized_recipeimage = recipeimage.resize((int(imgwidth * imagescale), int(imgheight * imagescale)), Image.ANTIALIAS)

            #Convert the resized image to a tkinter compatible image for use in label
            finalrecipeimage = ImageTk.PhotoImage(resized_recipeimage)

            #Generate image label
            Label(framelist[6], image= finalrecipeimage, borderwidth=0).grid(row=0,column=0)


    #Edit Recipe Button
    interactivebuttoncreation('submitbutton_recipeview',windowname, 'Edit', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'pack', 0, 0, 2, 140, 2, lambda: editwindowtransit(windowname,recipename), '', '')
    #Cancel Button
    interactivebuttoncreation('cancelbutton_recipeview',windowname, 'Cancel', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'pack', 0, 0, 2, 140, 2, lambda: closewindow(windowname), '', '')

    #Update scrollregion
    scrollregionupdate(canvaslist[0],framelist[1])

    #Close connection
    vdbconn.close()


#Submit new recipe widget creation function
def newrecipewidgetcreation(windowtype, recipename, windowname, framelist, canvaslist, basicinfolist, buttonlist, ingritemlist, ingramtlist, ingrunitlist, ingrdeletebuttonlist, counterlist, anoteidlist, anotelist, anotedeletebuttonlist, stepidlist, steplist, stepdeletebuttonlist, taglistboxlist, imagelabellist, imagepathlist, imagebuttonlist):
    #Define entrybox names
    rnbox = f'rnbox_{windowname}'
    sbox = f'sbox_{windowname}'
    trbox = f'trbox_{windowname}'

    #Generate entryboxes for basicinfo frames
    #Create recipe name, servings, and time required entryboxes
    entryboxcreation(str(rnbox), framelist[2], 132, 5, mainfgcolor, mainbgcolor, 'grid', 0, 0, 1, 'append', basicinfolist)
    entryboxcreation(str(sbox), framelist[3], 20, 5, mainfgcolor, mainbgcolor, 'grid', 0, 0, 1, 'append', basicinfolist)
    entryboxcreation(str(trbox), framelist[4], 20, 5, mainfgcolor, mainbgcolor, 'grid', 0, 0, 1, 'append', basicinfolist)

    #Generate tag labels and listboxes
    #Cuisine listbox
    labelcreation('cuisinetaglabel_recipeview', framelist[5], 'Cuisine', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 0, 0, 2, 'center', '', '')
    dropdownboxcreation('Cuisinelistbox_recipeview', framelist[5], 'cuisine', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 1, 0, 1, 'append', taglistboxlist)

    #Mealtype listbox
    labelcreation('mealtypetaglabel_recipeview', framelist[5], 'Meal Type', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 2, 0, 2, 'center', '', '')
    dropdownboxcreation('mealtypelistbox_recipeview', framelist[5], 'meal', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 3, 0, 1, 'append', taglistboxlist)

    #Coursetype listbox
    labelcreation('coursetypetaglabel_recipeview', framelist[5], 'Course', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 4, 0, 2, 'center', '', '')
    dropdownboxcreation('coursetypelistbox_recipeview', framelist[5], 'course', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 5, 0, 1, 'append', taglistboxlist)

    #Diet listbox
    labelcreation('diettaglabel_recipeview', framelist[5], 'Diet', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 6, 0, 2, 'center', '', '')
    dropdownboxcreation('dietlistbox_recipeview', framelist[5], 'diet', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 7, 0, 1, 'append', taglistboxlist)

    #Main ingredient listbox
    labelcreation('mainingredienttaglabel_recipeview', framelist[5], 'Main Ingredient', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 8, 0, 2, 'center', '', '')
    dropdownboxcreation('mainingredientlistbox_recipeview', framelist[5], 'mainingredient', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 9, 0, 1, 'append', taglistboxlist)

    #Muslim diet listbox
    labelcreation('halalstatustaglabel_recipeview', framelist[5], 'Halal Status', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 10, 0, 2, 'center', '', '')
    dropdownboxcreation('halalstatuslistbox_recipeview', framelist[5], 'halalstatus', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 11, 0, 1, 'append', taglistboxlist)

    #Main ingredient listbox
    labelcreation('kosherstatustaglabel_recipeview', framelist[5], 'Kosher Status', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 12, 0, 2, 'center', '', '')
    dropdownboxcreation('kosherstatuslistbox_recipeview', framelist[5], 'kosherstatus', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 13, 0, 1, 'append', taglistboxlist)

    #Buddhist diet listbox
    labelcreation('buddhiststatustaglabel_recipeview', framelist[5], 'Beef inclusion', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 25, 'flat', 'grid', 14, 0, 2, 'center', '', '')
    dropdownboxcreation('buddhiststatuslistbox_recipeview', framelist[5], 'buddhiststatus', mainbgcolor, mainfgcolor, 15, 25, 0, 'grid', 15, 0, 1, 'append', taglistboxlist)


    #Add photo upload button
    interactivebuttoncreation('aphbutton_recipeview',framelist[6], 'Upload Photo', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'grid', 1, 0, 2, 99, 2, lambda: addphoto(windowtype, windowname, '','.', framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist), 'append', imagebuttonlist)
    #Add description entrybox
    textboxcreation('descriptiontb_recipeview', framelist[7], mainbgcolor, mainfgcolor, 10, 100, 2, 'pack', 1, 1, 1, 'write','','', 'append', basicinfolist)
    #Add 'new additional ingredient' button
    interactivebuttoncreation('aibutton_recipeview', framelist[8], 'Add New Ingredient', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'grid', 1, 0, 4, 50, 2, '', 'append', buttonlist)
    buttonlist[0].configure(command = lambda: addingr(buttonlist,framelist, canvaslist, ingritemlist, ingramtlist, ingrunitlist,ingrdeletebuttonlist, counterlist))
    #Add 'new additional note' button
    interactivebuttoncreation('anbutton_recipeview', framelist[9], 'Add New Note', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'grid', 0, 0, 3, 63, 2, '', 'append', buttonlist)
    buttonlist[1].configure(command = lambda: addanote(buttonlist, framelist, canvaslist, anoteidlist, anotelist, anotedeletebuttonlist, counterlist))
    #Add 'new addition step' button
    interactivebuttoncreation('apbutton_recipeview', framelist[10], 'Add New Step', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'grid', 0, 0, 2, 114, 2, '', 'append', buttonlist)
    buttonlist[2].configure (command = lambda: addstep(buttonlist, framelist, canvaslist, stepidlist, steplist, stepdeletebuttonlist, counterlist))
    #Submit Recipe Button
    interactivebuttoncreation('submitbutton_recipeview',windowname, 'Submit', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'pack', 0, 0, 2, 144, 2, lambda: submitchecks(windowtype, recipename, windowname, ingritemlist, ingramtlist, ingrunitlist, anotelist, steplist, basicinfolist, taglistboxlist, imagepathlist), '', '')
    #Cancel Button
    interactivebuttoncreation('cancelbutton_recipeview',windowname, 'Cancel', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, 'pack', 0, 0, 2, 144, 2, lambda: closewindow(windowname), '', '')


#Edit recipe widget creation function
def editrecipewidgetcreation(windowtype, recipename, windowname, framelist, canvaslist, basicinfolist, buttonlist, ingritemlist, ingramtlist, ingrunitlist, ingrdeletebuttonlist, counterlist, anoteidlist, anotelist, anotedeletebuttonlist, stepidlist, steplist, stepdeletebuttonlist, taglistboxlist, imagelabellist, imagepathlist, imagebuttonlist):

    #Generate basicinfo entryboxes and addrow buttons
    newrecipewidgetcreation(windowtype, recipename, windowname, framelist, canvaslist, basicinfolist, buttonlist, ingritemlist, ingramtlist, ingrunitlist, ingrdeletebuttonlist, counterlist, anoteidlist, anotelist, anotedeletebuttonlist, stepidlist, steplist, stepdeletebuttonlist, taglistboxlist, imagelabellist, imagepathlist, imagebuttonlist)

    #Define recipe database path
    recipedbpath = './Recipes.db'

    #Open connection, create cursor
    edbconn = connect(recipedbpath)
    edbcurs = edbconn.cursor()

    #Fetch data from basicinfo table
    databasefetch(recipename, edbcurs, 'basicinfo')
    currentrecord = edbcurs.fetchall()
    #Insert basicinfo into basicinfo entryboxes
    basicinfolist[0].insert(0,currentrecord[0][0])
    basicinfolist[1].insert(0,currentrecord[0][1])
    basicinfolist[2].insert(0,currentrecord[0][2])
    basicinfolist[3].insert('1.0', currentrecord[0][3])

    #Create new ingredient rows and input data within
    for ingredient in currentrecord:
        addingr(buttonlist, framelist, canvaslist, ingritemlist, ingramtlist, ingrunitlist, ingrdeletebuttonlist, counterlist)
        currentcounter = counterlist[0]-2
        #Insert relevant data into respective ingredient entryboxes
        ingritemlist[currentcounter].insert(0,ingredient[8])
        ingramtlist[currentcounter].insert(0,ingredient[9])
        ingrunitlist[currentcounter].insert(0,ingredient[10])

    #Fetch data from anote table
    databasefetch(recipename, edbcurs, 'anote')
    currentrecord = edbcurs.fetchall()

    #Create new anote rows and input data within
    for anote in currentrecord:
        addanote(buttonlist, framelist, canvaslist, anoteidlist, anotelist, anotedeletebuttonlist, counterlist)
        currentcounter = counterlist[1]-1
        #Insert relevant data into respective anote entrybox
        anotelist[currentcounter].insert(0,anote[2])

    #Fetch data from steps table
    databasefetch(recipename, edbcurs, 'steps')
    currentrecord = edbcurs.fetchall()

    #Create new step rows and input data within
    for step in currentrecord:
        addstep(buttonlist, framelist, canvaslist, stepidlist, steplist, stepdeletebuttonlist, counterlist)
        currentcounter = counterlist[2]-1
        #Insert relevant data into respective step entrybox
        steplist[currentcounter].insert(0,step[2])

    #Fetch data from photos table
    databasefetch(recipename, edbcurs, 'photos')
    currentrecord = edbcurs.fetchall()
    #If there is no photo, generate a label telling users of this
    if currentrecord == []:
        labelcreation('photo_viewrecipe', framelist[6], 'This recipe has no attached photo :(', applicationfont, 12, 'bold', mainfgcolor, mainbgcolor, 0, 0, 100, 'flat', 'grid', 0, 0, 1, 'n', '', '')
    else:
        for record in currentrecord:
            global finalrecipeimage
            blobdata = record[1]
            addphoto(windowtype, windowname, blobdata, '', framelist, imagelabellist, imagepathlist, canvaslist, imagebuttonlist)

    #Fetch data from tags table
    databasefetch(recipename, edbcurs, 'tags')
    currentrecord = edbcurs.fetchall()
    #Define local counter variable for use in tag listbox value insertion
    taglistboxcounter = 0

    for record in currentrecord:
        for tag in record[1:]:
            taglistboxlist[taglistboxcounter].delete(0,END)
            taglistboxlist[taglistboxcounter].insert(0,tag)
            taglistboxcounter +=1

    #Close connection
    edbconn.close()

#Main window creation function
def recipeview(windowtype,windowname):
    #Set title of the window based on the nature of the window
    if windowtype == 'new':
        recipename = ''
        windowtitle = 'Submit New Recipe'
    elif windowtype == 'viewing':
        recipename = str(windowname)
        windowtitle = 'Viewing: ' + str(windowname)
    elif windowtype == 'editing':
        recipename = str(windowname)
        windowtitle = f'Editing: {windowname}'

    #Create and configure the window
    windowname = Toplevel()
    windowconfiguration(windowname, windowtitle, './resources/img/Ico.ico', mainbgcolor, '', '', '', '', '')

    #Set counter for buttons and entrybox creation
    #Create list for counter storage
    #index 0,1, and 2 corresponds to ingredient, anotes, and preparation steps respectively
    counterlist_recipeview = []
    counterlist_recipeview.append(1)
    counterlist_recipeview.append(0)
    counterlist_recipeview.append(0)

    #Lists to store important frames, canvases, and widgets
    framelist_recipeview = []
    canvaslist_recipeview = []
    basicinfo_recipeview = []
    buttons_recipeview=[]
    ingredientitemlist_recipeview= []
    ingredientamountlist_recipeview= []
    ingredientunitlist_recipeview= []
    ingredientdeletebuttons_recipeview = []
    anoteidlist_recipeview = []
    anotelist_recipeview = []
    anotedeletebuttons_recipeview=[]
    stepidlist_recipeview = []
    steplist_recipeview = []
    stepdeletebuttons_recipeview = []
    tagboxlist_recipeview = []
    imagelabellist_recipeview = []
    imagepathlist_recipeview = []
    imagebuttonlist_recipeview = []

    #Generate layout
    windowlayoutcreation(windowtype, windowname, framelist_recipeview, canvaslist_recipeview, basicinfo_recipeview, buttons_recipeview,ingredientamountlist_recipeview, ingredientitemlist_recipeview)

    if windowtype == 'viewing':
        #Fill frames with information
        viewrecipewidgetcreation(windowname, recipename, framelist_recipeview, canvaslist_recipeview, basicinfo_recipeview , ingredientitemlist_recipeview,ingredientamountlist_recipeview)
    elif windowtype == 'new':
        newrecipewidgetcreation(windowtype, recipename, windowname, framelist_recipeview, canvaslist_recipeview, basicinfo_recipeview ,buttons_recipeview, ingredientitemlist_recipeview,ingredientamountlist_recipeview, ingredientunitlist_recipeview,ingredientdeletebuttons_recipeview, counterlist_recipeview, anoteidlist_recipeview, anotelist_recipeview, anotedeletebuttons_recipeview, stepidlist_recipeview, steplist_recipeview, stepdeletebuttons_recipeview, tagboxlist_recipeview, imagelabellist_recipeview, imagepathlist_recipeview, imagebuttonlist_recipeview)
    elif windowtype == 'editing':
        editrecipewidgetcreation(windowtype, recipename, windowname, framelist_recipeview, canvaslist_recipeview, basicinfo_recipeview ,buttons_recipeview, ingredientitemlist_recipeview,ingredientamountlist_recipeview, ingredientunitlist_recipeview,ingredientdeletebuttons_recipeview, counterlist_recipeview, anoteidlist_recipeview, anotelist_recipeview, anotedeletebuttons_recipeview, stepidlist_recipeview, steplist_recipeview, stepdeletebuttons_recipeview, tagboxlist_recipeview, imagelabellist_recipeview, imagepathlist_recipeview, imagebuttonlist_recipeview)


    #Ensure that the window loops
    windowname.mainloop()
