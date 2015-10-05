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

#ANSI escape sequence colors for changing text color without using curses
#source: stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class terminalColors:
	SUCCESS = '\033[92m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

#Checks if applications are/or installed and are of correct version.
#Sources used:
#stackoverflow.com/questions/5847934/how-to-check-if-python-module-exists-and-can-be-imported
#stackoverflow.com/questions/710609/checking-a-python-module-version-at-runtime
#stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7
def versionCheck():
	stop = 0 #Used to determine if there was a failure, if so halt program.

	#Check to see if required programs are and installed and have correct version.
	check_these_programs = [["python", "mysql", "psql"], ["2.7", "14", "9"]]
	
	for i in range(0, len(check_these_programs[0])):
		j = 1 #used for indexing in 2-D array
		
		#Used to redirect output from subprocess to devnull (don't want it printed to screen), closes after subprocess 			 finishes.
		fnull = open(os.devnull, 'w')
		try:
			subprocess.call([check_these_programs[0][i], "--version"], stdout = fnull, 
																	   stderr=subprocess.STDOUT,
																	   close_fds=True)
		except:#Means program is not installed
			stop = 1 #Failure do not continue with program
			result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
			print check_these_programs[0][i] + " version " + check_these_programs[j][i] + " - " + result
			continue #Skip to next iteration
		else:#Program is installed now need to check versions
			if check_these_programs[0][i] == "python":
				major = sys.version_info.major
				minor = sys.version_info.minor
				if major == 2 and minor == 7:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program
			
			elif check_these_programs[0][i] == "psql":
				proc = subprocess.Popen(["psql", "--version"], stdout=subprocess.PIPE)
				ver = proc.communicate()[0]
				
				#parse output of psql --version to get major version number
				ver = ver.split(" ",4)
				ver = ver[2].split(".", 1)
				ver = ver[0]
				
				if ver == check_these_programs[1][2]:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program

			elif check_these_programs[0][i] == "mysql":
				proc = subprocess.Popen(["mysql", "--version"], stdout=subprocess.PIPE)
				ver = proc.communicate()[0]
				
				#parse output of psql --version to get major version number
				ver = ver.split(" ",3)
				ver = ver[3].split(".", 1)
				ver = ver[0]
				
				if ver == check_these_programs[1][1]:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program


		print check_these_programs[0][i] + " version " + check_these_programs[j][i] + ".* - " + result
		time.sleep(0.5)

	#Check python modules
	check_these_modules = [["curses", "MySQLdb", "psycopg2"],["2.2", "1.2.3", "2.5.3 (dt dec mx pq3 ext)"]]
	for i in range(0, len(check_these_modules[0])):
		j = 1 #used for indexing in 2-D array

		try:
			__import__(check_these_modules[0][i]) #Checking modules are installed.
		except ImportError:
			stop = 1 #Failure do not continue with program
			result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
			print check_these_modules[0][i] + " version " + check_these_modules[j][i] + " - " + result
			continue #Skip to next iteration
		else:#Is installed, but need to check for correct version.
			if check_these_modules[0][i] == "curses":#curses uses different syntax to check for version
				ver = curses.version
			else:
				ver = eval(check_these_modules[0][i] + '.__version__')

			if check_these_modules[j][i] == ver:
				result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
			else:
				result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
				stop = 1 #Failure do not continue with program

			print check_these_modules[0][i] + " version " + check_these_modules[j][i] + " - " + result
			time.sleep(0.5)
		
		j += 1

	
	if stop == 1:
		print terminalColors.FAIL + "ALERT" + terminalColors.ENDC
		print "One or more items is either not installed or is the incorrect version"
		print "Now exiting"
	else:
		print "Thank you for your patience, now opening program..."

	time.sleep(5)

	return(stop)

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
def runmenu(menu, parent, start):

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
	optioncount = len(menu['options'])
	exitmenu = False
	start = 0
	while not exitmenu: #Loop until the user exits the menu
		getin = runmenu(menu, parent, start)
		if getin == -1 or getin == optioncount:
			exitmenu = True
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

	#Connect to a postgresql database
	db = psycopg2.connect("dbname='postgres' user='root'")
	#Must create cursor object to allow queries from postgresql db
	cur = db.cursor()

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
	postgresSQL_DB_Orchestrator = DatabaseOrchestrator("", "root", "", "postgres", "PostgresSQL")
	rows, columns = os.popen('stty size', 'r').read().split()
	rows = int(rows)
	columns = int(columns)
	processmenu(main_menu)


curses.endwin() #Terminating ncurses application
