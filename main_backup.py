#!/usr/bin/env python
#Program Filename: main.py
#Authors: Casey Balza, Daryl Cooke, Nickolas Jurczak
#Date: 9/28/2015
#Description: A ncurses based program that mimics the use of phpmyadmin.

import curses
import MySQLdb
import psycopg2
import os
import subprocess
import sys
import time
from utils.DatabaseOrchestrator import DatabaseOrchestrator
from utils.initiateProgram import versionCheck
from utils.initiateProgram import terminalColors



stop = versionCheck()#If everything needed is installed and correct version continue with program, else halt.

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
	
#clears screen and outputs exit menu
def exit_window(new_menu, old_menu):
	stdscr.clear
	processmenu(new_menu, old_menu)
#end exit_window

#closes program
def exit_program():
	curses.endwin() #Terminating ncurses application
	sys.exit()
#end exit_program()

######################## MENU FUNCTIONS #######################################################
# Source to help create menus http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/

h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
FORM = "form"
TEXT = "text"


login_form = {
	'title': "Login", 'type': FORM, 'subtitle': "Please login to your db account",
	'fields':[
		{'title': "Username: ", 'type': TEXT},
		{'title': "Password: ", 'type': TEXT}
	],
	'options': [
		{'title': "Back", 'type': COMMAND, 'command': 'processMenu(main_menu)'},
		{'title': "Continue", 'type': COMMAND, 'command': 'testfun()'}
	]
}

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

exit_menu = {
	'title': "Exit program?", 'type': MENU, 'subtitle': "Please select an action...",
	'options':[
  		{ 'title': "Yes", 'type': COMMAND, 'command': 'exit_program()' },
  ]#end of exit_menu options
}#end of exit_menu data

def runform(form):

	fieldcount = len(form['fields'])# how many fields there are in the form
	optioncount = len(form['options'])# how many options there are

	pos=0
	oldpos=None
	x = None
	optionselect = 0
	results = []

	# Display all fields

	for index in range(fieldcount):
		
		if index < fieldcount:
			stdscr.addstr(5+index,20, "%s" % (form['fields'][index]['title']), n)
			index += 1

	stdscr.border(0)
	stdscr.addstr(2,35, form['title'], curses.A_STANDOUT) # Title for this menu
	stdscr.addstr(4,16, form['subtitle'], curses.A_BOLD) # Subtitle for this menu
	stdscr.addstr(28,23, "Created By: Casey Balza, Daryle Cooke, & Nick Jurczak", curses.color_pair(2))

	#display options			

	for index in range(optioncount):
		textstyle = n
	
		if pos==fieldcount:
			if optionselect==index:
				textstyle = h
		stdscr.addstr(5+5*fieldcount,20+(index*20), "%s" % (form['options'][index]['title']), textstyle)
	stdscr.refresh()

	for index in range(fieldcount):
		if form['fields'][index]['type'] == TEXT:
			win = curses.newwin(1,30,5+index,20+len(form['fields'][index]['title']))
			tb = curses.textpad.Textbox(win)
			text = None
			def check(input):
				if input == 13:
					tb.gather()
			tb.do_command(check)
			text = tb.edit()
			results.append(text)
			

# This function displays the appropriate menu and returns the option selected
def runmenu(menu, parent, start):

	# work out what text to display as the last menu option
	if parent is None:
		lastoption = 0 #display no lastoption
	elif parent == "No":
		lastoption = "No"
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
			count = 0
			for index in range(optioncount):
				index += start
				textstyle = n

				if pos==count:
					textstyle = h
				if count < 7 and index < optioncount:
					stdscr.addstr(5+count,20, "%d - %s" % (count+1, menu['options'][index]['title']), textstyle)
					count += 1

				elif count == 7:
					stdscr.addstr(5+count,20, "%d - %s" % (count+1, "MORE"), textstyle)				
					count += 1

			
			# Now display Exit/Return at bottom of menu
			if lastoption != 0:
				textstyle = n

				if pos==count:
					textstyle = h
				stdscr.addstr(5+count,20, "%d - %s" % (count+1, lastoption), textstyle)
				stdscr.refresh()
				# finished updating screen

		x = stdscr.getch() # Gets user input

		# What is user input?
		max = 0
		if optioncount <= 8:
			max = ord(str(optioncount+1))
		else:
			max = ord('9')
		if x >= ord('1') and x <= max:
			pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
		elif x == 258: # down arrow
			if pos < count:
				pos += 1
			else: pos = 0
		elif x == 259: # up arrow
			if pos > 0:
				pos += -1
			else: pos = count
		elif x == 69: # if user entered 'E' (shift + e) from the .getch()
			pos = 69
			return pos
	# return index of the selected item
	if pos == 8 or pos == optioncount:
		return -1
	elif pos == 7:
		return -2
	else:
		pos += start

		return pos
#end runmenu()

# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
	if menu['type'] == MENU:
		optioncount = len(menu['options'])
		exitmenu = False
		start = 0
		while not exitmenu: #Loop until the user exits the menu
			getin = runmenu(menu, parent, start)
			if getin == -1 or getin == optioncount:
				exitmenu = True
			elif getin == 69: #if user input 'E' (shift + e) bring up exit menu
				stdscr.clear()
				saying = "No"
				exit_window(exit_menu, saying) #open exit window
				stdscr.clear()#Clear screen of exit menu if user did not exit
			elif getin == -2:
				start += 7
				stdscr.clear()
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
	
	elif menu['type'] == FORM:
		testfun()
#end processmenu()


################### END OF MENU FUNCTIONS #######################################################

#Test function
def testfun():
	stdscr.clear()
	stdscr.refresh()
	stdscr.addstr(2,2, "WORKING", curses.A_STANDOUT)
	stdscr.getch()
#end testfun()

def show_table_contents(table, databaseType):
        if databaseType == "MySQL":
            tableContents = mySQL_DB_Orchestrator.get_table_for_viewing(table)
        if databaseType == "PostgresSQL":
            tableContents = postgresSQL_DB_Orchestrator.get_table_for_viewing(table)
        stdscr.clear()
        stdscr.refresh()
        schemaRow = curses.newwin(5, columns, 0, 0)
        width = columns // 5
        rowFormat = "%-{}s %-{}s %-{}s %-{}s %-{}s".format(width, width, width, width, width)
        schemaRow.addstr(1, 1, rowFormat % (tableContents[0][0][0], tableContents[0][1][0], tableContents[0][2][0], tableContents[0][3][0], tableContents[0][4][0]))
        schemaRow.refresh()

        for x in range(1, 20):
            itemRow = curses.newwin(3, columns, 5 + ((x - 1) * 2), 0)
            itemRow.addstr(1, 1, rowFormat % (tableContents[1][x][0], tableContents[1][x][1], tableContents[1][x][2], tableContents[1][x][3], tableContents[1][x][4]))
            itemRow.refresh()

        #Put column names in first column
        stdscr.getch()

def show_tables(dbs, databaseType):
        if databaseType == "MySQL":
            mySQL_DB_Orchestrator.select_database(dbs)
        if databaseType == "PostgresSQL":
            postgresSQL_DB_Orchestrator.select_database(dbs)

        dbs_menu = {
                'title': dbs + " tables", 'type': MENU, 'subtitle': "Please select a table or action...",
                'options':[]#end of menu options
        }#end of menu data

        if databaseType == "MySQL":
            tables = mySQL_DB_Orchestrator.show_tables()
        if databaseType == "PostgresSQL":
            tables = postgresSQL_DB_Orchestrator.show_tables()

        dbs_menu['options'].append({'title': "CUSTOM QUERY", 'type': COMMAND, 'command': 'testfun()' })
        for table in tables:
                action = os.path.join('show_table_contents(\"{}\", \"{}\")'.format(table, databaseType))
                dbs_menu['options'].append({'title': table, 'type': COMMAND, 'command': action })
        processmenu(dbs_menu, main_menu)
#end show_tables(dbs)

#Displays information from MySQL server
def use_mysql():
	mysql_menu = {
		'title': "MySql databases", 'type': MENU, 'subtitle': "Please select a database to use...",
		'options':[]#end of menu options
	}#end of menu data

        databases = mySQL_DB_Orchestrator.show_databases()
        for database in databases:
            action = os.path.join('show_tables(\"{}\", \"{}\")'.format(database, "MySQL"))
            mysql_menu['options'].append({'title': database, 'type': COMMAND, 'command': action })
        processmenu(mysql_menu, main_menu)
#end use_mysql()

def use_psql():
        postgressql_menu = {
                'title': "PostgresSQL databases", 'type': MENU, 'subtitle': "Please select a database to use...",
                'options':[]#end of menu options
        }#end of menu data

        databases = postgresSQL_DB_Orchestrator.show_databases()
        for database in databases:
            action = os.path.join('show_tables(\"{}\", \"{}\")'.format(database, "PostgresSQL"))
            postgressql_menu['options'].append({'title': database, 'type': COMMAND, 'command': action})
        processmenu(postgressql_menu, main_menu)
#end use_psql()

#MAIN PROGRAM
if stop == 0:

	mySQL_DB_Orchestrator = DatabaseOrchestrator("localhost", "root", "password", "", "MySQL")
	postgresSQL_DB_Orchestrator = DatabaseOrchestrator("", "ubuntu", "", "postgres", "PostgresSQL")
	rows, columns = os.popen('stty size', 'r').read().split()
	rows = int(rows)
	columns = int(columns)
	processmenu(main_menu)


curses.endwin() #Terminating ncurses application
