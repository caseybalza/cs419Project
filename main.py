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
from utils.view import *
from utils.initiateProgram import initiateProgram
from utils.NCursesHandler import NCursesHandler
from utils.Logger import get_logger

#Check if everything needed is installed and correct version, continue with program, else halt.

#stop = initiateProgram() #create instance of class initiateProgram
#stop = stop.versionCheck() #call versionCheck on the instance.
stop = 0

DB_Orchestrator = DatabaseOrchestrator()
ncurses = NCursesHandler()
logger = get_logger("Main")

def show_table_contents(table):
	logger.info("Inside show_table_contents")
	logger.info("Database selected is: {}".format(DB_Orchestrator.database))
	tableContents = DB_Orchestrator.get_table_for_viewing(table)
	logger.info("Displaying the {} table".format(table))
	ncurses.draw_table(table, tableContents)

	return None

def show_tables(dbs):
	logger.info("Inside show_tables")
	DB_Orchestrator.select_database(dbs)

	dbs_menu = {
	'title': dbs + " tables", 'type': Dictionary.MENU, 'subtitle': "Please select a table or action...",
	'location': dbs,'options':[]#end of menu options
	}#end of menu data

	tables = DB_Orchestrator.show_tables()

	dbs_menu['options'].append({'title': "CUSTOM QUERY", 'type': Dictionary.COMMAND, 'command': 'testfun()' })
	for table in tables:
		action = os.path.join('show_table_contents(\"{}\")'.format(table))
		dbs_menu['options'].append({'title': table, 'type': Dictionary.COMMAND, 'command': action, 'location': table })
	return dbs_menu
#end show_tables(dbs)

#Displays information from MySQL server
def use_mysql(results):
	logger.info("Inside use_mysql")
	#logininfo = eval(results)
	logininfo = results
	DB_Orchestrator.load("localhost", logininfo[0], logininfo[1], "", "MySQL")
	mysql_menu = {
		'title': "MySql databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
		'location': 'MySQL/', 'options':[]#end of menu options
	}#end of menu data
	
	#Add Create Database option to top of menu
	mysql_menu['options'].append({ 'title': "Create Database", 'type': Dictionary.COMMAND, 'command': 'loadDB_createform()', 'location': "createDB" })

	#Add Import Database option to top of menu
	mysql_menu['options'].append({ 'title': "Import Database", 'type': Dictionary.COMMAND, 'command': 'importMySQLdb', 'location': "importDB" })

	databases = DB_Orchestrator.show_databases()
	for database in databases:
		action = os.path.join('show_tables(\"{}\")'.format(database))
		mysql_menu['options'].append({'title': database, 'type': Dictionary.COMMAND, 'command': action, 'location': database})
	
	return mysql_menu
#end use_mysql()

def use_psql(results):
	logger.info("Inside use_psql")
	DB_Orchestrator.load("", results[0], results[1], "postgres", "PostgresSQL")
	postgressql_menu = {
		'title': "PostgresSQL databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
		'location': 'PSQL/', 'options':[]#end of menu options
}#end of menu data

	#Add Create Database option to top of menu
	postgressql_menu['options'].append({ 'title': "Create Database", 'type': Dictionary.COMMAND, 'command': 'loadDB_createform()', 'location': "createDB" })

	#Add Import Database option to top of menu
	postgressql_menu['options'].append({ 'title': "Import Database", 'type': Dictionary.COMMAND, 'command': 'importPSQLdb', 'location': "importDB" })

	databases = DB_Orchestrator.show_databases()
	for database in databases:
		action = os.path.join('show_tables(\"{}\")'.format(database))
		postgressql_menu['options'].append({'title': database, 'type': Dictionary.COMMAND, 'command': action, 'location': database})
	return postgressql_menu
#end use_psql()

def goBack(input):
	return input

def end_program(handler):
	handler.exit_program()
	sys.exit()

def login(type):
	return ncurses.setuplogin(type)
	#return login_form

def createDB(results):
	ncurses.stdscr.clear()
	results[0] = DB_Orchestrator.create_database(results[0]) #results is a list so pass in first index which is the new databases name.
	ncurses.createDB_window(createDB_menu, "", "Close", results) #open exit window
	ncurses.stdscr.clear()#Clear screen of exit menu if user did not exit

#Used to load form to get name of new database to create and calls createMySQLdb()
def loadDB_createform():
	form = createDB_form
	function = 'createDB('
	form['options'][1]['command'] = function
	return form

def mainFunction(screen): 
	#MAIN PROGRAM
	if stop == 0:
		while 1:
			#processmenu(main_menu)
			results=ncurses.startmenu()
			back_list_stack = [] #Create a stack to hold path
			location = [] #Holds path user has taken inside sql servers
			#back_list_stack.append(results) #Add main menu to path
			nextMenu = eval(results)
			back_list_stack.append(nextMenu)
			ncurses.resetscreen()
			results = ncurses.processmenu(nextMenu, 'Login')
			#back_list_stack.append(results)#Add option selected from Main menu to path
			location.append(nextMenu.get('location')) #Add part of path to location
			storeold = None;
			while 1:
				logger.info(results)
				size = len(back_list_stack)
				oldMenu = nextMenu
				nextMenu = eval(results)

				if nextMenu is None:
					nextMenu = oldMenu
				logger.info(nextMenu)

				location.append(nextMenu.get('location'))  #Add part of path to location
				if nextMenu == storeold:
					back_list_stack.pop()
					if size >= 2:
						back_list_stack.pop()
						location.pop()
					if size > 2:
						oldMenu = back_list_stack[-1]
					else:
						oldMenu = None
					location.pop()
					size = len(back_list_stack)
				ncurses.resetscreen()
				
				#Return back to main menu and login if new database has been created
				if oldMenu == loadDB_createform():
					break
		
				str_location = ''.join(location) #convert list to string.

				results = ncurses.processmenu(nextMenu, str_location, oldMenu)
				storeold = oldMenu
				back_list_stack.append(nextMenu)



curses.wrapper(mainFunction)

#curses.endwin() #Terminating ncurses application





