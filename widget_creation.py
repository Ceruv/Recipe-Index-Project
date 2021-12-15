# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 00:51:01 2021

@author: Ryan
"""

from tkinter import Label, Button, Entry, LabelFrame, Frame, Canvas, Text,  ttk
from appearance_config import mainbgcolor

#Auxilary functions for widget creation
#Fontstatus generation function
def fontstatus(fontboldoritalic):

    #If the input is one of the acceptable inputs, set the fontstylise variable acording to the input
    if fontboldoritalic in ('bold', 'italic', 'normal'):
        fontstylise = fontboldoritalic
    #If not, set the fontstylise variable to normal and state that assignment failed in the console
    else:
        fontstylise = 'normal'
        print("Invalid input detected, setting label style to 'normal'")

    #Return the value of the fontstylise variable
    return fontstylise


#Relief setting function
def reliefsetting(relief):

    #If the relief is defined as 'none' set finalrelief as 'flat'
    if relief =='none':
        finalrelief='flat'
    #If not, set the final relief as the input
    else:
        finalrelief=relief

    #Return the value of the finalrelief variable
    return finalrelief


#Configuration functions
#Window details configuration function
def windowconfiguration(windowname, windowtitle, windowiconpath, backgroundcolor, geometrywidth, geometryheight, widthresizablestatus, heightresizablestatus, screencenterstatus):
    #If window title is not blank, then set the window title according to the input
    if windowtitle != '':
        windowname.title(windowtitle)

    #If there is a window icon path specified, then set the icon for the window
    if windowiconpath != '':
        windowname.iconbitmap(windowiconpath)

    #If a background color is specified, then set the background color according to the input
    if backgroundcolor != '':
        windowname.configure(background = backgroundcolor)

    #If there are geometry dimensions specified, then set the geometry according to the inputs
    if (geometrywidth != '') and (geometryheight != ''):
        if screencenterstatus != 'screencenter':
            windowname.geometry(f'{geometrywidth}x{geometryheight}')
        elif screencenterstatus == 'screencenter':
            #Get screen resolution
            userscreenwidth = windowname.winfo_screenwidth()
            userscreenheight = windowname.winfo_screenheight()

            #Find centre
            centerhorizontal = int(userscreenwidth/2 - geometrywidth/ 2)
            centervertical = int(userscreenheight/2 - geometryheight/ 2)
            windowname.geometry(f'{geometrywidth}x{geometryheight}+{centerhorizontal}+{centervertical}')

    #Set the resizability status of the window according to the inputs
    if heightresizablestatus == 'resizable':
        heightrs = 'True'
    else:
        heightrs = 'False'

    if widthresizablestatus == 'resizable':
        widthrs = 'True'
    else:
        widthrs = 'False'

    windowname.resizable(widthrs,heightrs)


#Label creation function
def labelcreation(name, location, text, font, fontsize,fontboldoritalic, fgcolor, bgcolor,borderwidth, height,width,relief,packorgrid,gridrow,gridcolumn,columnspan,anchor, appendstatus, appendlist):

    #If a font stylisation is specified, set the fontstylise variable according to the input
    fontstylise = fontstatus(fontboldoritalic)

    #Set relief according to the input
    lblrelief = reliefsetting(relief)

    #Set the label's anchor based on the input
    if anchor == 'none':
        lblanchor = 'center'
    else:
        lblanchor = anchor

    #Create a label based on the inputs
    name = Label(location, text = text, font=(font, fontsize, fontstylise), fg= fgcolor, bg= bgcolor, bd = borderwidth, relief=lblrelief,anchor=lblanchor)

    #If no height was specified, do not set a height for the label
    if height=='':
        pass
    #If not, configure the label to have a height according to the input
    else:
        name.configure(height= height)

    #If no width was specified, do not set a width for the label
    if width=='':
        pass
    #If not, configure the label to have a width according to the input
    else:
        name.configure(width=width)

    #Position the widget
    if packorgrid == 'pack':
        name.pack()
    elif packorgrid =='grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan= columnspan, sticky='s')

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#Interactive button creation function
def interactivebuttoncreation(name, destination, text, font, fontsize,fontboldoritalic,bgcolor, fgcolor, packorgrid,gridrow,gridcolumn,columnspan,width, height,desiredcommand,appendstatus, appendlist):

    #Define commands for color change
    def hover_mode(e):
        name['bg']=bgcolor
        name['fg']=fgcolor
    def leave_mode(e):
        name['bg']=fgcolor
        name['fg']=bgcolor

    #If a font stylisation is specified, set the fontstylise variable according to the input
    fontstylise = fontstatus(fontboldoritalic)

    #Create an interactive button based on inputs
    name = Button(destination,width=width, height=height, text=text, font=(font,fontsize,fontstylise), fg=bgcolor, bg=fgcolor, border=0, activeforeground = fgcolor, activebackground = bgcolor)

    #If there is a command specified, configure the button to utilise the command
    if desiredcommand !='':
        name.configure(command= desiredcommand)
    else:
        pass

    #Bind the button to the color change commands
    name.bind('<Enter>',hover_mode)
    name.bind('<Leave>',leave_mode)

    #Position the widget
    if packorgrid == 'grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan=columnspan)
    else:
        name.pack()

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#Standard button creation function
def standardbuttoncreation(name, destination, text, font, fontsize,fontboldoritalic, bgcolor, fgcolor, abgcolor,afgcolor, packorgrid,gridrow,gridcolumn,columnspan,width,desiredcommand,appendstatus, appendlist):

    #If a font stylisation is specified, set the fontstylise variable according to the input
    fontstylise = fontstatus(fontboldoritalic)

    #Create an standard button based on inputs
    name = Button(destination,width=width, text=text, font=(font,fontsize,fontstylise), fg=fgcolor, bg=bgcolor,activebackground = abgcolor, activeforeground = afgcolor, border=0, command= desiredcommand)

    #Position the widget
    if packorgrid == 'grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan=columnspan)
    else:
        name.pack()

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#Entrybox creation function
def entryboxcreation(name, destination,width, borderwidth,fgcolor, bgcolor, packorgrid,gridrow, gridcolumn,columnspan,appendstatus, appendlist):

    #Create an entry box based on inputs
    name = Entry(destination, width = width, borderwidth = borderwidth, fg=fgcolor, bg= bgcolor)

    #Position the widget
    if packorgrid == 'pack':
        name.pack()
    elif packorgrid =='grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan= columnspan)

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#LabelFrame creation function
def labelframecreation(name, destination, text, font, fontsize, fontboldoritalic, relief,fgcolor, bgcolor, packorgrid, gridrow,gridcolumn, columnspan,appendstatus,appendlist):

    #If a font stylisation is specified, set the fontstylise variable according to the input
    fontstylise = fontstatus(fontboldoritalic)

    #Set relief according to the input
    lrelief = reliefsetting(relief)

     #Create an label frame based on inputs
    name = LabelFrame(destination, text=text,font=(font, fontsize, fontstylise), relief = lrelief,fg=fgcolor, bg=bgcolor)

    #Position the widget
    if packorgrid == 'pack':
        name.pack()
    elif packorgrid =='grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan= columnspan, sticky='n', pady = 10)

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#Frame creation function
def framecreation(name, destination, bgcolor, borderwidth, relief, packorgrid, gridrow, gridcolumn, columnspan, appendstatus, appendlist):

    #Set relief according to the input
    frelief = reliefsetting(relief)

    #Create a frame based on inputs
    name = Frame(destination, relief = frelief,bg=bgcolor, bd=borderwidth)

    #Position the widget
    if packorgrid == 'pack':
        name.pack()
    elif packorgrid =='grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan= columnspan)

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#Canvas creation function
def canvascreation(name, destination, bgcolor, width,height, highlightthickness, packorgrid, gridrow, gridcolumn, columnspan, side, fill, expandstatus, appendstatus, appendlist):

    #Create a canvas based on inputs
    name = Canvas(destination, bg=bgcolor, width=width ,height=height,highlightthickness = highlightthickness)

    #Position the widget
    if packorgrid == 'pack':
        name.pack(side=side,fill=fill,expand=expandstatus)
    elif packorgrid =='grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan= columnspan)

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)


#Scrollbar creation function
def scrollbarcanvascreation(infoframename, destination, sbname,canvasname,scrollframename, sbframelist, sbcanvaslist,canvaswidth,canvasheight, sborient, sbtheme, sbfgcolor,sbbgcolor,sbbordercolor,sbthroughcolor, sbarrowcolor, packorgrid, gridrow,gridcolumn, sbcolumnspan):

    #Determine if the scrollbar is a vertical or horizontal scrollbar, and set the relevant variables accordingly
    if sborient == 'vertical':
        scrollbartype = 'Vertical.TScrollbar'
        sbfill = 'y'
        sbside = 'right'
    elif sborient == 'horizontal':
        scrollbartype = 'Horizontal.TScrollbar'
        sbfill = 'x'
        sbside = 'bottom'

    #Create a frame to host the canvas
    framecreation(infoframename, destination, mainbgcolor, -2, 'flat', packorgrid, gridrow, gridcolumn, sbcolumnspan, 'append', sbframelist)

    #Create a canvas to host the scrollframe
    canvascreation(canvasname, sbframelist[0], mainbgcolor, canvaswidth, canvasheight, -2, 'pack', 1, 1, 1, 'left','both', 1, 'append', sbcanvaslist)

    #Set the style of the scrollbar
    sbstyle = ttk.Style()
    sbstyle.theme_use(sbtheme)
    sbstyle.configure(scrollbartype,foreground=sbfgcolor, background=sbbgcolor,bordercolor=sbbordercolor,troughcolor=sbthroughcolor, arrowcolor=sbarrowcolor)

    #Create the scrollbar
    sbname = ttk.Scrollbar(sbframelist[0], orient=sborient)

    #Configure the command of the scrollbar based on the orient
    if sborient == 'vertical':
        sbname.configure(command = sbcanvaslist[0].yview)
    elif sborient == 'horizontal':
        sbname.configure(command = sbcanvaslist[0].xview)

    #Position the widget within the host frame
    sbname.pack(side=sbside,fill= sbfill, expand=1)

    #Configure the canvas scrollcommand based on the orient of the scrollbar
    if sborient == 'vertical':
        sbcanvaslist[0].configure(yscrollcommand=sbname.set)
    elif sborient == 'horizontal':
        sbcanvaslist[0].configure(xscrollcommand=sbname.set)

    #Bind the scrollregion(scrollframe) to the canvas, and create the window to display the information hosted within
    sbcanvaslist[0].bind('<Configure>', lambda e: sbcanvaslist[0].configure(scrollregion = sbcanvaslist[0].bbox('all')))
    framecreation(scrollframename, sbcanvaslist[0], mainbgcolor, -2, 'flat','', 1, 1, 1, 'append', sbframelist)
    sbcanvaslist[0].create_window((0,0),window=sbframelist[1],anchor='nw')


#Text box creation function
def textboxcreation(tbname, destination, tbbgcolor, tbfgcolor, tbheight, tbwidth, tbborderwidth,packorgrid,gridrow, gridcolumn, tbcolumnspan,readonlyorwrite,inserttextstatus,insertedtext, appendstatus, appendlist):

    #Create an text box based on inputs
    tbname = Text(destination, bg=tbbgcolor, fg = tbfgcolor, height=tbheight, width = tbwidth, relief = 'groove', bd=tbborderwidth)

    #Position the widget
    if packorgrid == 'pack':
        tbname.pack()
    elif packorgrid =='grid':
        tbname.grid(row=gridrow,column=gridcolumn, columnspan= tbcolumnspan)

    #If the insert text status is verified as such, insert the specified text into the box
    if inserttextstatus == 'insert':
        tbname.insert('1.0', insertedtext)
    #If the read-only status is verified as such, set the text box to be read-only
    if readonlyorwrite =='readonly':
        tbname.configure(state = 'disabled')

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(tbname)


#Drop-down box creation function
def dropdownboxcreation(name, destination, listtype, bgcolor, fgcolor, height, width, borderwidth, packorgrid, gridrow, gridcolumn, columnspan, appendstatus, appendlist):

    #Determine the list of options based on the 'listtype' input
    if listtype == 'cuisine':
        listoptions = ['Uncategorised','Chinese','Indian', 'Malay', 'American', 'French', 'Fusion']
    elif listtype == 'meal':
        listoptions = ['Uncategorised', 'Breakfast', 'Lunch', 'Dinner', 'Snack', 'Supper']
    elif listtype == 'course':
        listoptions = ['Uncategorised', 'Appetiser', 'Soup', 'Main', 'Sides', 'Dessert', 'Salad', 'Drink', 'Snack']
    elif listtype == 'diet':
        listoptions = ['Uncategorised','Vegan', 'Vegetarian']
    elif listtype == 'mainingredient':
        listoptions = ['Uncategorised','Chicken','Beef','Fish','Crustacean','Shellfish','Vegetables','Grains','Fruit','Alcohol']
    elif listtype == 'halalstatus':
        listoptions = ['Uncategorised', 'Halal', 'Non-halal']
    elif listtype == 'kosherstatus':
        listoptions = ['Uncategorised','Kosher', 'Non-kosher']
    elif listtype == 'buddhiststatus':
        listoptions = ['Uncategorised', 'Includes beef', 'No beef']

    #If no drop-down box has been created, then configure the boxes' style and colors
    if appendlist == []:
        destination.option_add('*TCombobox*Listbox*Background', bgcolor)
        destination.option_add('*TCombobox*Listbox*Foreground', fgcolor)
        destination.option_add('*TCombobox*Listbox*selectBackground', fgcolor)
        destination.option_add('*TCombobox*Listbox*selectForeground', bgcolor)
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TCombobox',fieldforeground=fgcolor, foreground = fgcolor, fieldbackground=bgcolor, background = bgcolor, bordercolor=fgcolor, arrowcolor = fgcolor, selectbackground = fgcolor, selectforeground = bgcolor)

    #Create an drop-down box based on inputs
    name = ttk.Combobox(destination, value = listoptions, height= height, width = width)

    #Set the pre-selected tag to be 'uncategorised'
    name.current(0)

    #Position the widget
    if packorgrid == 'pack':
        name.pack()
    elif packorgrid =='grid':
        name.grid(row=gridrow,column=gridcolumn, columnspan= columnspan)

    #If the appendstatus is set to append, append the widget into the specified list
    if appendstatus == 'append':
        appendlist.append(name)
