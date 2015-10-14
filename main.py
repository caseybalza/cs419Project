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
<<<<<<< HEAD
from utils.view import *
from utils.initiateProgram import initiateProgram
from utils.NCursesHandler import NCursesHandler


#Check if everything needed is installed and correct version, continue with program, else halt.
stop = initiateProgram() #create instance of class initiateProgram
stop = stop.versionCheck() #call versionCheck on the instance.
=======
from utils.initiateProgram import versionCheck
from utils.initiateProgram import terminalColors
from utils.NcursesViewHandler import *
from utils.MenuHandler import *



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

h = curses.color_pair(1) #h is the coloring for a highlighted menu option
n = curses.A_NORMAL #n is the coloring for a non highlighted menu option
>>>>>>> origin/menu-test-nj
	
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
<<<<<<< HEAD
# Source to help create menus http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/

=======
# This function calls showmenu and then acts on the selected item
def processmenu(menu, parent=None):
	if menu['type'] == MENU:
		optioncount = len(menu['options'])
		exitmenu = False
		start = 0
		while not exitmenu: #Loop until the user exits the menu
			getin = runmenu(menu, parent, start, stdscr)
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
>>>>>>> origin/menu-test-nj

################### END OF MENU FUNCTIONS 
#######################################################


#Test function
#def testfun():
	#stdscr.clear()
	#stdscr.refresh()
	#stdscr.addstr(2,2, "WORKING", curses.A_STANDOUT)
	#stdscr.getch()
#end testfun()

def show_table_contents(table, databaseType):
        if databaseType == "MySQL":
            tableContents = mySQL_DB_Orchestrator.get_table_for_viewing(table)
        if databaseType == "PostgresSQL":
            tableContents = postgresSQL_DB_Orchestrator.get_table_for_viewing(table)
        #stdscr.clear()
        #stdscr.refresh()
        #schemaRow = curses.newwin(5, columns, 0, 0)
        width = columns // 5
        rowFormat = "%-{}s %-{}s %-{}s %-{}s %-{}s".format(width, width, width, width, width)
        #schemaRow.addstr(1, 1, rowFormat % (tableContents[0][0][0], tableContents[0][1][0], tableContents[0][2][0], tableContents[0][3][0], tableContents[0][4][0]))
        #schemaRow.refresh()

        #for x in range(1, 20):
            #itemRow = curses.newwin(3, columns, 5 + ((x - 1) * 2), 0)
            #itemRow.addstr(1, 1, rowFormat % (tableContents[1][x][0], tableContents[1][x][1], tableContents[1][x][2], tableContents[1][x][3], tableContents[1][x][4]))
            #itemRow.refresh()

        #Put column names in first column
        #stdscr.getch()

def show_tables(dbs, databaseType):
        if databaseType == "MySQL":
            mySQL_DB_Orchestrator.select_database(dbs)
        if databaseType == "PostgresSQL":
            postgresSQL_DB_Orchestrator.select_database(dbs)

        dbs_menu = {
                'title': dbs + " tables", 'type': Dictionary.MENU, 'subtitle': "Please select a table or action...",
                'options':[]#end of menu options
        }#end of menu data

        if databaseType == "MySQL":
            tables = mySQL_DB_Orchestrator.show_tables()
        if databaseType == "PostgresSQL":
            tables = postgresSQL_DB_Orchestrator.show_tables()

        dbs_menu['options'].append({'title': "CUSTOM QUERY", 'type': Dictionary.COMMAND, 'command': 'testfun()' })
        for table in tables:
                action = os.path.join('show_table_contents(\"{}\", \"{}\")'.format(table, databaseType))
                dbs_menu['options'].append({'title': table, 'type': Dictionary.COMMAND, 'command': action })
        return dbs_menu
#end show_tables(dbs)

#Displays information from MySQL server
def use_mysql():
	mysql_menu = {
		'title': "MySql databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
		'options':[]#end of menu options
	}#end of menu data

        databases = mySQL_DB_Orchestrator.show_databases()
        for database in databases:
            action = os.path.join('show_tables(\"{}\", \"{}\")'.format(database, "MySQL"))
            mysql_menu['options'].append({'title': database, 'type': Dictionary.COMMAND, 'command': action })
        return mysql_menu
#end use_mysql()

def use_psql():
        postgressql_menu = {
                'title': "PostgresSQL databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
                'options':[]#end of menu options
        }#end of menu data

        databases = postgresSQL_DB_Orchestrator.show_databases()
        for database in databases:
            action = os.path.join('show_tables(\"{}\", \"{}\")'.format(database, "PostgresSQL"))
            postgressql_menu['options'].append({'title': database, 'type': Dictionary.COMMAND, 'command': action})
        return postgressql_menu
#end use_psql()

def goBack(input):
	return input

def end_program(handler):
	handler.exit_program()
	sys.exit()

def login(handler):
	return login_form

#MAIN PROGRAM
if stop == 0:

	mySQL_DB_Orchestrator = DatabaseOrchestrator("localhost", "root", "password", "", "MySQL")
	postgresSQL_DB_Orchestrator = DatabaseOrchestrator("", "ubuntu", "", "postgres", "PostgresSQL")
	#rows, columns = os.popen('stty size', 'r').read().split()
	#rows = int(rows)
	#columns = int(columns)
	#processmenu(main_menu)
	ncurses = NCursesHandler()
	results=ncurses.startmenu()
	nextMenu = eval(results)
	ncurses.resetscreen()
	results = ncurses.processmenu(nextMenu)
	storeold = None
	while 1:
		oldMenu = nextMenu
		nextMenu = eval(results)
		if nextMenu == storeold:
			oldMenu = -1
		ncurses.resetscreen()
		results = ncurses.processmenu(nextMenu, oldMenu)
		storeold = oldMenu
	


#curses.endwin() #Terminating ncurses application
