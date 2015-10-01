#!/usr/bin/env python
#Program Filename: main.py
#Authors: Casey Balza, Daryl Cooke, Nickolas Jurczak
#Date: 9/28/2015
#Description: A ncurses based program that mimics the use of phpmyadmin.

import curses
import MySQLdb
import psycopg2

stdscr = curses.initscr() #initialize ncurses
curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
curses.cbreak() # Runs each key as it is pressed rather than waiting for the return key to pressed)
curses.start_color() #allow colors
stdscr.keypad(1) # Capture input from keypad allow to move around on menus

#Create color pairs.
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)


######################## MENU FUNCTIONS #######################################################
# Source to help create menus http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/

h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"

main_menu = {
	'title': "Main Menu", 'type': MENU, 'subtitle': "Please select an option...",
	'options':[
  		{ 'title': "Use MySQL databases", 'type': COMMAND, 'command': 'use_mysql()' },
    	{ 'title': "Use PostgreSQL databases", 'type': COMMAND, 'command': 'use_psql()' },
		#Menu with a submenu
        { 'title': "Sebmenu preview", 'type': MENU, 'subtitle': "Please select an option...",
        	'options': [
        		{ 'title': "Option1", 'type': COMMAND, 'command': 'testfun()' },
          		{ 'title': "Option2", 'type': COMMAND, 'command': 'testfun()' },
          		{ 'title': "Option3", 'type': COMMAND, 'command': 'testfun()' },
			]#end submenu
        }
  ]#end of menu options
}#end of menu data


# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent):

	# work out what text to display as the last menu option
	if parent is None:
		lastoption = "Exit"
	else:
		lastoption = "Return to %s" % parent['title']

	optioncount = len(menu['options']) # how many options in this menu

	pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called, position 			  returns to 0, when runmenu ends the position is returned and tells the program what opt$
	oldpos=None # used to prevent the screen being redrawn every time
	x = None #control for while loop, let's you scroll through options until return key is pressed then returns 		     pos to program

	# Loop until return key is pressed
	while x !=ord('\n'):
		if pos != oldpos:
			oldpos = pos
			stdscr.border(0)
			stdscr.addstr(2,35, menu['title'], curses.A_STANDOUT) # Title for this menu
			stdscr.addstr(4,16, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu
			stdscr.addstr(28,23, "Created By: Casey Balza, Daryl Cooke, & Nickolas Jurczak", curses.color_pair(2))

			# Display all the menu items, showing the 'pos' item highlighted
			for index in range(optioncount):
				textstyle = n

				if pos==index:
					textstyle = h
				stdscr.addstr(5+index,20, "%d - %s" % (index+1, menu['options'][index]['title']), textstyle)

			# Now display Exit/Return at bottom of menu
			textstyle = n

			if pos==optioncount:
				textstyle = h

			stdscr.addstr(5+optioncount,20, "%d - %s" % (optioncount+1, lastoption), textstyle)
			stdscr.refresh()
			# finished updating screen

		x = stdscr.getch() # Gets user input

		# What is user input?
		if x >= ord('1') and x <= ord(str(optioncount+1)):
			pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
		elif x == 258: # down arrow
			if pos < optioncount:
				pos += 1
			else: pos = 0
		elif x == 259: # up arrow
			if pos > 0:
				pos += -1
			else: pos = optioncount

	# return index of the selected item
	return pos
#end runmenu()

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
	optioncount = len(menu['options'])
	exitmenu = False
	while not exitmenu: #Loop until the user exits the menu
		getin = runmenu(menu, parent)
		if getin == optioncount:
			exitmenu = True
		elif menu['options'][getin]['type'] == COMMAND:
			curses.def_prog_mode()    # save curent curses environment
			stdscr.clear() #clears previous screen
			result = (menu['options'][getin]['command']) # Get command into variable
			eval(result)#Call the command
			stdscr.clear() #clears previous screen on key press and updates display based on pos
			curses.reset_prog_mode()   # reset to 'current' curses environment
			curses.curs_set(1)         # reset doesn't do this right
			curses.curs_set(0)
		elif menu['options'][getin]['type'] == MENU:
			stdscr.clear() #clears previous screen on key press and updates display based on pos
			processmenu(menu['options'][getin], menu) # display the submenu
			stdscr.clear() #clears previous screen on key press and updates display based on pos
		elif menu['options'][getin]['type'] == EXITMENU:
		  	exitmenu = True
#end processmenu()

################### END OF MENU FUNCTIONS #######################################################

#Test function
def testfun():
	stdscr.clear()
	stdscr.refresh()
	stdscr.addstr(2,2, "WORKING", curses.A_STANDOUT)
	stdscr.getch()
#end testfun()

#Displays information from MySQL server
def use_mysql():

	#Connect to MySQL database
	db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="password",
                     db="")

	#Must create cursor object to allow queries from mysql db
	cur = db.cursor()

	stdscr.refresh()

	#Create window for outputting MySQL databases.
	stdscr2 = curses.newwin(13, 25, 15, 3)
	stdscr2.border(0)
	stdscr2.bkgd(' ', curses.color_pair(2))
	stdscr2.refresh()
	
	#Create window for outputting MySQL db classicmodels Tables.
	stdscr3 = curses.newwin(13, 24, 15, 29)
	stdscr3.border(0)
	stdscr3.bkgd(' ', curses.color_pair(5))
	stdscr3.refresh()
	
	#Create window for outputting MySQL db classicmodels customerName Table.
	stdscr4 = curses.newwin(13, 24, 15, 54)
	stdscr4.border(0)
	stdscr4.bkgd(' ', curses.color_pair(6))
	stdscr4.refresh()

	#Output to windows
	stdscr2.addstr(1,5, 'MySQL databases', curses.A_STANDOUT)
	stdscr2.refresh()
	
	cur.execute("SHOW DATABASES;")
	i = 3
	for row in cur.fetchall():
		stdscr2.addstr(i,3, row[0])
		i += 1
	stdscr2.refresh()

	stdscr3.addstr(1,1, '"classicmodels" tables', curses.A_STANDOUT)
	stdscr3.refresh()

	cur.execute("USE classicmodels;")
	cur.execute("SHOW TABLES;")
	i = 3
	for row in cur.fetchall():
		stdscr3.addstr(i,3, row[0])
		i += 1
	stdscr3.refresh()

	stdscr4.addstr(1,1, '"customerName"', curses.A_STANDOUT)
	stdscr4.addstr(2,1, '"from "customers"', curses.A_STANDOUT)
	stdscr4.refresh()

	cur.execute("SELECT customerName FROM customers ORDER BY customerNumber ASC LIMIT 5")
	i = 3
	for row in cur.fetchall():
		stdscr4.addstr(i,1, row[0])
		i += 1
	stdscr4.refresh()
	
	stdscr.getch()
#end use_mysql()

def use_psql():

	#Connect to a postgresql database
	db = psycopg2.connect("dbname='postgres' user='root'")
	#Must create cursor object to allow queries from postgresql db
	cur = db.cursor()

	stdscr.refresh()

	#Create window for outputting PosegreSQL databases.
	stdscr2 = curses.newwin(13, 25, 15, 3)
	stdscr2.border(0)
	stdscr2.bkgd(' ', curses.color_pair(2))
	stdscr2.refresh()
	
	#Create window for outputting PostgreSQL db shakespeare Tables.
	stdscr3 = curses.newwin(13, 24, 15, 29)
	stdscr3.border(0)
	stdscr3.bkgd(' ', curses.color_pair(5))
	stdscr3.refresh()
	
	#Create window for outputting PostgreSQL db shakespeare characterName Table.
	stdscr4 = curses.newwin(13, 24, 15, 54)
	stdscr4.border(0)
	stdscr4.bkgd(' ', curses.color_pair(6))
	stdscr4.refresh()

	stdscr2.addstr(1,3, 'PostgreSQL databases', curses.A_STANDOUT)
	stdscr2.refresh()

	cur.execute("SELECT * FROM pg_database")
	i = 3
	for row in cur.fetchall():
		stdscr2.addstr(i,3, row[0])
		i += 1
	stdscr2.refresh()

	#To use shakespeare db have to reconnect to postgresql with specified db name
	#Connect to a postgresql database
	db = psycopg2.connect("dbname='shakespeare' user='root'")
	#Must create cursor object to allow queries from postgresql db
	cur = db.cursor()

	stdscr3.addstr(1,2, '"shakespeare" tables', curses.A_STANDOUT)
	stdscr3.refresh()

	cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
	i = 3
	for row in cur.fetchall():
		stdscr3.addstr(i,3, row[0])
		i += 1
	stdscr3.refresh()

	stdscr4.addstr(1,3, '"characterName"', curses.A_STANDOUT)
	stdscr4.addstr(2,3, '"from "character"', curses.A_STANDOUT)
	stdscr4.refresh()

	cur.execute("SELECT charName FROM character LIMIT 5")
	i = 3
	for row in cur.fetchall():
		stdscr4.addstr(i,1, row[0])
		i += 1
	stdscr4.refresh()

	stdscr.getch()
#end use_psql()

#MAIN PROGRAM
processmenu(main_menu)

curses.endwin() #Terminating ncurses application


