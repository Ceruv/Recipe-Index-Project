# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 00:37:02 2021

@author: Ryan
"""

from tkinter import Frame, Canvas, Tk, messagebox
from os import path
import random
from sqlite3 import connect
from PIL import  Image, ImageTk
from widget_creation import windowconfiguration, labelcreation, labelframecreation, dropdownboxcreation, interactivebuttoncreation, entryboxcreation, scrollbarcanvascreation
from appearance_config import mainbgcolor, mainfgcolor, applicationfont
from recipe_window_creation import recipeview


#Define filterframe and bottomframe frame storages
bottomframelist_hmpg= []

#Define bottomframe checks
global bottomframe_viewall
global bottomframe_searchresults
bottomframe_viewall = False
bottomframe_searchresults = False

#Define recipe database path
recipedbpath='./Recipes.db'

#Create root window, set title, icon, background color
root = Tk()
windowconfiguration(root, 'Recipe Index Project (v2.1.1-alpha)', './resources/img/Ico.ico', mainbgcolor, '', '', '', '', '')

#Create homepage logo and title
logoframe_hmpg = Frame(root, width=53,height=30,borderwidth=0, highlightthickness=0)
logoframe_hmpg.grid(row=0,column=0, columnspan=2)
logocanvas_hmpg = Canvas(logoframe_hmpg,width=161,height=140, bg=mainbgcolor,border=-2)
logocanvas_hmpg.pack()
logoimg_hmpg = ImageTk.PhotoImage(Image.open('./resources/img/Ico.ico'))
logocanvas_hmpg.create_image(81,70,image=logoimg_hmpg)

labelcreation('title_hmpg', root, 'RECIPE INDEX PROJECT', 'Impact','18','bold',mainfgcolor, mainbgcolor,2, 2,20,'none','grid',1,0,1,'center','','')


#View all function
def bottomframe(viewallorsearch):
    global bottomframe_viewall
    global bottomframe_searchresults

    #If recipe database does not exist, tell user to submit a new recipe before continuing
    if not path.exists(recipedbpath):
        messagebox.showinfo(title= 'Recipe Database Missing', message='Please submit a new recipe before continuing.')
        return

    #If bottom frame space is free, pass this
    if not bottomframe_viewall and not bottomframe_searchresults:
        pass
    #Or else, delete the bottom frame
    else:
        bottomframelist_hmpg[0].destroy()
        bottomframelist_hmpg.pop(0)
        #If the bottomframe was a viewall frame, and the command is a viewall command, do not generate a new frame and mark bottom as non-viewall
        if bottomframe_viewall and viewallorsearch =='viewall':
            bottomframe_viewall = False
            return
        #Or else, if the bottom frame was a search frame, and the command is a search command, generate a new search filter frame and search frame
        elif bottomframe_searchresults and viewallorsearch == 'search':
            bottomframelist_hmpg[0].destroy()
            bottomframelist_hmpg.pop(0)
        #Or else, if the bottom frame was a search frame, and the command is a viewall command, generate a new viewall frame and mark bottom as non-searchresult
        elif bottomframe_searchresults and viewallorsearch == 'viewall':
            bottomframelist_hmpg[0].destroy()
            bottomframelist_hmpg.pop(0)
            bottomframe_searchresults = False
        #Or else, if the bottom frame was a viewall frame, and the command is a search command, generate a new viewall frame and mark bottom as non-viewall
        elif bottomframe_viewall and viewallorsearch == 'search':
            bottomframe_viewall = False


    #Create list to store frames for scrollregion
    frameslist_hmpg = []
    canvaslist_hmpg =[]

    #If the bottomframe is designated as a viewall frame, set text to reflect this. Or else, if it is a search frame, set text to reflect that
    if viewallorsearch =='viewall':
        labeltext = 'Recipes'
    elif viewallorsearch == 'search':
        labeltext = 'Search Results:'

    #Generate the master label frame, and generate the label
    labelframecreation('bottomframe_hmpg', root, '', applicationfont, 0, 'bold', 'groove', mainfgcolor, mainbgcolor, 'grid', 9, 0, 1, 'append', bottomframelist_hmpg)
    labelcreation('viewalllabel_hmpg', bottomframelist_hmpg[0], labeltext, applicationfont, 10, 'bold', mainbgcolor, mainfgcolor, 0, 0, 40, 'flat', 'grid', 0, 0, 1, 'center', '', '')

    #Generate the scrollregion frames
    scrollbarcanvascreation('infoframe_hmpg', bottomframelist_hmpg[0], 'scrollbar_hmpg', 'canvas_hmpg', 'scrollframe_hmpg', frameslist_hmpg, canvaslist_hmpg, 265, 270, 'vertical', 'alt', mainfgcolor, mainbgcolor, mainbgcolor, mainbgcolor, mainfgcolor, 'grid',1,0,1)

    #Connect to the database and establish a cursor
    bfconn = connect(recipedbpath)
    bfcurs = bfconn.cursor()

    #If the frame is a viewall frame, list all recipes in order of time appended
    if viewallorsearch =='viewall':
        bfcurs.execute('''SELECT recipe_title FROM basicinfo''')
        bfrecipelist = bfcurs.fetchall()

        #Generate buttons for each entry
        for recipename in bfrecipelist:
            interactivebuttoncreation(recipename[0], frameslist_hmpg[1], recipename[0], applicationfont, 8, 'normal', mainfgcolor, mainbgcolor, 'pack', 1, 1, 1, 50,2, lambda recipename=recipename: recipeview('viewing',recipename[0]), '', '')

        bottomframe_viewall = True

    #Or else, if the frame is a search frame, execute a query
    elif viewallorsearch == 'search':

        #Get the keyword from the search bar
        search_keyword = str(entryboxlist[0].get()).lower()

        #Fetch data from ingredient table
        bfcurs.execute('''SELECT * FROM ingredients''')
        bfrecipelist = bfcurs.fetchall()

        #Define gridrow counter for use in search result button generation
        searchbutton_gridrow = 0

        #Define list to store generated button info
        global generatedsearchbuttons
        generatedsearchnames = []
        generatedsearchbuttons = []

        #Comb through recipe names in list to see if it contains the keyword
        for entry in bfrecipelist:
            recipename  = entry[0]
            queriedname = str(recipename).lower()
            if search_keyword in queriedname:
                if recipename not in generatedsearchnames:
                    generatedsearchnames.append(recipename)
                    interactivebuttoncreation(recipename, frameslist_hmpg[1], recipename, applicationfont, 8, 'normal', mainfgcolor, mainbgcolor, 'grid', searchbutton_gridrow, 0, 1, 50, 2, lambda recipename=recipename: recipeview('viewing',recipename), 'append', generatedsearchbuttons)
                    searchbutton_gridrow += 1

        #Comb through ingredients to see if it contains the keyword
        for entry in bfrecipelist:
            recipename = entry[0]
            ingr = str(entry[2]).lower()
            if search_keyword in ingr:
                if recipename not in generatedsearchnames:
                    generatedsearchnames.append(recipename)
                    interactivebuttoncreation(recipename, frameslist_hmpg[1], recipename, applicationfont, 8, 'normal', mainfgcolor, mainbgcolor, 'grid', searchbutton_gridrow, 0, 1, 50, 2, lambda recipename=recipename: recipeview('viewing',recipename), 'append', generatedsearchbuttons)
                    searchbutton_gridrow += 1

        #Define list for listbox referencing
        searchfilterlistboxlist_hmpg = []

        #Search filter update function
        def filterupdate(e):
            searchfiltersactivated = []
            for box in searchfilterlistboxlist_hmpg:
                if box.get() != 'Uncategorised':
                    searchfiltersactivated.append(str(box.get()))

            #Connect to the database and establish a cursor
            fuconn = connect(recipedbpath)
            fucurs = fuconn.cursor()
            fucurs.execute('''SELECT * FROM tags''')
            furecipelist = fucurs.fetchall()

            #Define gridrow counter for use in search result button generation
            searchbutton_gridrow = 0

            #Define list for storage of recipe names that adhere to filter conditions
            filtermatchrecipes =[]

            #Get a list of recipes that adhere to the filters
            for entry in furecipelist:
                filtermatch = all(elem in entry for elem in searchfiltersactivated)
                if filtermatch:
                    filtermatchrecipes.append(entry[0])

            #Get a list of recipe names that adhere to the searchbar query
            fucurs.execute('''SELECT * FROM ingredients''')
            furecipelist = fucurs.fetchall()
            #Redefine keyword and wipe generated search buttons and their entries
            search_keyword = str(entryboxlist[0].get()).lower()

            #Destroy all existing search buttons
            global generatedsearchbuttons
            for generatedbutton in generatedsearchbuttons:
                generatedbutton.destroy()

            #Define and clear lists for use in search result button creation
            generatedsearchnames = []
            generatedsearchbuttons =[]


            #Comb through recipe names in list to see if it contains the keyword
            for entry in furecipelist:
                recipename  = entry[0]
                queriedname = str(recipename).lower()
                if search_keyword in queriedname:
                    if recipename not in generatedsearchnames:
                        generatedsearchnames.append(recipename)

            #Comb through ingredients to see if it contains the keyword
            for entry in bfrecipelist:
                recipename = entry[0]
                ingr = str(entry[2]).lower()
                if search_keyword in ingr:
                    if recipename not in generatedsearchnames:
                        generatedsearchnames.append(recipename)

            #If a recipe passes the entrybox and tag check, then generate a search result button for it
            for entry in filtermatchrecipes:
                if entry in generatedsearchnames:
                    interactivebuttoncreation(entry, frameslist_hmpg[1], entry, applicationfont, 8, 'normal', mainfgcolor, mainbgcolor, 'grid', searchbutton_gridrow, 0, 1, 50, 2, lambda entry=entry: recipeview('viewing',entry), 'append', generatedsearchbuttons)
                    searchbutton_gridrow +=1



        #Generate labelframe for search filters
        labelframecreation('searchfilter_hmpg', root, '', applicationfont, 8, 'normal', 'groove', mainfgcolor, mainbgcolor, 'grid', 8, 0, 1, 'append', bottomframelist_hmpg)

        #Generate label within search filter labelframe
        labelcreation('searchfilterlabel_hmpg', bottomframelist_hmpg[1], 'Search Filters', applicationfont, 10, 'bold', mainbgcolor, mainfgcolor, 0, 0, 40, 'flat', 'grid', 0, 0, 2, 'center', '', '')

        #Generate tag labels and listboxes
        #Cuisine listbox
        labelcreation('cuisinetaglabel_hmpg', bottomframelist_hmpg[1], 'Cuisine', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 1, 0, 1, 'center', '', '')
        dropdownboxcreation('Cuisinelistbox_hmpg', bottomframelist_hmpg[1], 'cuisine', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 2, 0, 1, 'append', searchfilterlistboxlist_hmpg)

        #Mealtype listbox
        labelcreation('mealtypetaglabel_hmpg', bottomframelist_hmpg[1], 'Meal Type', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 1, 1, 1, 'center', '', '')
        dropdownboxcreation('mealtypelistbox_hmpg', bottomframelist_hmpg[1], 'meal', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 2, 1, 1, 'append', searchfilterlistboxlist_hmpg)

        #Coursetype listbox
        labelcreation('coursetypetaglabel_hmpg', bottomframelist_hmpg[1], 'Course', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 3, 0, 1, 'center', '', '')
        dropdownboxcreation('coursetypelistbox_hmpg', bottomframelist_hmpg[1], 'course', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 4, 0, 1, 'append', searchfilterlistboxlist_hmpg)

        #Diet listbox
        labelcreation('diettaglabel_hmpg', bottomframelist_hmpg[1], 'Diet', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 3, 1, 1, 'center', '', '')
        dropdownboxcreation('dietlistbox_hmpg', bottomframelist_hmpg[1], 'diet', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 4, 1, 1, 'append', searchfilterlistboxlist_hmpg)

        #Main ingredient listbox
        labelcreation('mainingredienttaglabel_hmpg', bottomframelist_hmpg[1], 'Main Ingredient', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 5, 0, 1, 'center', '', '')
        dropdownboxcreation('mainingredientlistbox_hmpg', bottomframelist_hmpg[1], 'mainingredient', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 6, 0, 1, 'append', searchfilterlistboxlist_hmpg)

        #Muslim diet listbox
        labelcreation('halalstatustaglabel_hmpg', bottomframelist_hmpg[1], 'Halal Status', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 5, 1, 1, 'center', '', '')
        dropdownboxcreation('halalstatuslistbox_hmpg', bottomframelist_hmpg[1], 'halalstatus', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 6, 1, 1, 'append', searchfilterlistboxlist_hmpg)

        #Main ingredient listbox
        labelcreation('kosherstatustaglabel_hmpg', bottomframelist_hmpg[1], 'Kosher Status', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 7, 0, 1, 'center', '', '')
        dropdownboxcreation('kosherstatuslistbox_hmpg', bottomframelist_hmpg[1], 'kosherstatus', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 8, 0, 1, 'append', searchfilterlistboxlist_hmpg)

        #Buddhist diet listbox
        labelcreation('buddhiststatustaglabel_hmpg', bottomframelist_hmpg[1], 'Beef inclusion', applicationfont, 10, 'bold', mainfgcolor, mainbgcolor, -2, 2, 20, 'flat', 'grid', 7, 1, 1, 'center', '', '')
        dropdownboxcreation('buddhiststatuslistbox_hmpg', bottomframelist_hmpg[1], 'buddhiststatus', mainbgcolor, mainfgcolor, 15, 20, 0, 'grid', 8, 1, 1, 'append', searchfilterlistboxlist_hmpg)

        #Bind search commands to the events: 'tags selection', 'entrybox input'
        searchfilterlistboxlist_hmpg[0].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[1].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[2].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[3].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[4].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[5].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[6].bind('<<ComboboxSelected>>', filterupdate)
        searchfilterlistboxlist_hmpg[7].bind('<<ComboboxSelected>>', filterupdate)
        entryboxlist[0].bind("<KeyRelease>",filterupdate)

        #Update search results variable
        bottomframe_searchresults = True

    #Close the connection with the database
    bfconn.close()


#Random recipe function
def randomrecipe():
    #If recipe databse does not exist, tell user to submit a new recipe before continuing
    if not path.exists(recipedbpath):
        messagebox.showinfo(title= 'Recipe Database Missing', message='Please submit a new recipe before continuing.')
    else:
        #Open connection and create a cursor
        rrconn = connect(recipedbpath)
        rrcurs = rrconn.cursor()

        #Fetch data from basicinfo table
        rrcurs.execute('''SELECT recipe_title FROM basicinfo''')
        randomrecipelist = rrcurs.fetchall()

        #Get the number of entries stored within the database and generate a number within the confines of the list numbers to select a random recipe
        randomrecipenumber = random.randint(0,len(randomrecipelist)-1)
        randomrecipename = randomrecipelist[randomrecipenumber]

        #Bring up the page of the recipe selected
        recipeview('viewing',randomrecipename[0])

        #Close the connection
        rrconn.close()

#Search bar and button
#Create list used to store entrybox call details
entryboxlist = []
#Create search entrybox
entryboxcreation('searchentry_hmpg', root,60, 5,mainfgcolor, mainbgcolor, 'grid',2, 0,1,'append', entryboxlist)

#Create function buttons
interactivebuttoncreation('searchbutton_hmpg',root,'Search', applicationfont, 10, 'normal', mainfgcolor, mainbgcolor,'grid', 3,0,1,53, 2, lambda: bottomframe('search'), '','')
interactivebuttoncreation('viewallbutton_hmpg',root,'View All Recipes', applicationfont, 10, 'normal', mainfgcolor, mainbgcolor,'grid', 4,0,3,53,2, lambda: bottomframe('viewall'), '','')
interactivebuttoncreation('randomrecipebutton_hmpg',root,'Random Recipe', applicationfont, 10, 'normal', mainfgcolor, mainbgcolor,'grid', 5,0,3,53,2, randomrecipe, '','')
interactivebuttoncreation('newrecipebutton_hmpg',root,'Submit New Recipe', applicationfont, 10, 'normal', mainfgcolor, mainbgcolor,'grid', 6,0,3,53,2, lambda: recipeview('new','newrecipe'), '','')
interactivebuttoncreation('settingsbutton_hmpg',root,'Settings', applicationfont, 10, 'normal', mainfgcolor, mainbgcolor,'grid', 7,0,3,53,2, '', '','')

root.mainloop()
