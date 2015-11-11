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
from utils.constants import *

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
        location = "{}/{}/{}".format(DB_Orchestrator.databaseType, DB_Orchestrator.database, table)
	logger.info("Displaying the {} table".format(table))
	return ncurses.draw_table(table, tableContents, location, False)

def show_tables(dbs):
	logger.info("Inside show_tables")
	DB_Orchestrator.select_database(dbs)

	dbs_menu = {
	'title': dbs + " tables", 'type': Dictionary.MENU, 'subtitle': "Please select a table or action...",
	'location': "", 'options':[]#end of DB_options_menu#end of menu options
	}#end of menu data

	tables = DB_Orchestrator.show_tables()

	dbs_menu['options'].append({'title': "CUSTOM QUERY", 'type': Dictionary.COMMAND, 'command': 'custom_query()' })
	for table in tables:
		action = os.path.join('show_table_contents(\"{}\")'.format(table))
		dbs_menu['options'].append({'title': table, 'type': Dictionary.COMMAND, 'command': action, 'location': table })
	return dbs_menu
#end show_tables(dbs)

def custom_query():
        query = ncurses.custom_query()
        location = "{}/{}/CustomQuery".format(DB_Orchestrator.databaseType, DB_Orchestrator.database)
        if query != "":
            try:
                queryResult = DB_Orchestrator.custom_query(query)
            except:
                logger.info("Woops, error in custom query, should probably show these to the user")
                return None
            return ncurses.draw_table("CustomQuery", queryResult, location, True)
        return None

def show_db_options(dbs):
	logger.info("Inside show_db_options")
	viewtables = os.path.join('show_tables(\"{}\")'.format(dbs))
	deleteDB = os.path.join('loadDB_deleteform(\"{}\")'.format(dbs))
	exportDB = os.path.join('loadDB_exportform(\"{}\")'.format(dbs))
	db_options_menu = {
	'title': dbs + " Database Options", 'type': Dictionary.MENU, 'subtitle': "Please select an action...",
	'location': dbs ,'options':[
				{ 'title': "View Tables", 'type': Dictionary.COMMAND, 'command': viewtables },
				{ 'title': "Delete database", 'type': Dictionary.COMMAND, 'command': deleteDB },
				{ 'title': "Export database", 'type': Dictionary.COMMAND, 'command': exportDB },
				{ 'title': "Create Table", 'type': Dictionary.COMMAND, 'command': str(createEntity_form)}
			]#end of DB_options_menu
	}#DB_options_menu
	
	return db_options_menu
#end show_db_options(dbs)

#Displays information from MySQL server
def use_mysql(results):
	logger.info("Inside use_mysql")
	#logininfo = eval(results)
	logininfo = results
	try:
		DB_Orchestrator.load("localhost", logininfo[0], logininfo[1], "", "MySQL")
	except:
		ncurses.loginfail()
		return login(0)
		
	mysql_menu = {
		'title': "MySql databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
		'location': 'MySQL/', 'options':[]#end of menu options
	}#end of menu data
	
	#Add Create Database option to top of menu
	mysql_menu['options'].append({ 'title': "Create Database", 'type': Dictionary.COMMAND, 'command': 'loadDB_createform()', 'location': "createDB" })

	#Add Import Database option to top of menu
	mysql_menu['options'].append({ 'title': "Import Database", 'type': Dictionary.COMMAND, 'command': 'loadDB_importform()', 'location': "importDB" })

	databases = DB_Orchestrator.show_databases()
	for database in databases:
		action = os.path.join('show_db_options(\"{}\")'.format(database))
		mysql_menu['options'].append({'title': database, 'type': Dictionary.COMMAND, 'command': action, 'location': database})
	
	return mysql_menu
#end use_mysql()

def use_psql(results):
	logger.info("Inside use_psql")
	try:
		DB_Orchestrator.load("", results[0], results[1], "postgres", "PostgresSQL")
	except:
		ncurses.loginfail()
		return login(1)
	postgressql_menu = {
		'title': "PostgresSQL databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
		'location': 'PSQL/', 'options':[]#end of menu options
}#end of menu data

	#Add Create Database option to top of menu
	postgressql_menu['options'].append({ 'title': "Create Database", 'type': Dictionary.COMMAND, 'command': 'loadDB_createform()', 'location': "createDB" })

	#Add Import Database option to top of menu
	postgressql_menu['options'].append({ 'title': "Import Database", 'type': Dictionary.COMMAND, 'command': 'loadDB_importform()', 'location': "importDB" })

	databases = DB_Orchestrator.show_databases()
	for database in databases:
		action = os.path.join('show_db_options(\"{}\")'.format(database))
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

def importDB(results):
	logger.info("Inside importDB")
	ncurses.stdscr.clear()
	ncurses.stdscr2.clear()
	ncurses.stdscr3.clear()
	try:
		DB_Orchestrator.import_database(results[0])
	except:
		results[0] = IMPORT_DB_ERROR
	ncurses.importDB_window(importDB_menu, "", "Close", results) #open importDB_window
	return 'IMPORTED'

def exportDB(results):
	logger.info("Inside exportDB")
	ncurses.stdscr.clear()
	ncurses.stdscr2.clear()
	ncurses.stdscr3.clear()
	
	try:
		DB_Orchestrator.export_database(results[0])
	except:
		results[0] = EXPORT_DB_ERROR
	
	ncurses.exportDB_window(exportDB_menu, "", "Close", results) #open exportDB_window
	return 'EXPORTED'

def deleteDB(results):
	logger.info("Inside deleteDB")
	ncurses.stdscr.clear()
	ncurses.stdscr2.clear()
	ncurses.stdscr3.clear()
	if results[0] == results[1]:
		try:
			DB_Orchestrator.delete_database(results[0]) #results is a list so pass in first index which is the new databases name.
		except:
			results[0] = DELETE_DB_ERROR
	else:
		results[0] = DELETE_WRONG_DB_ERROR
	ncurses.deleteDB_window(deleteDB_menu, "", "Close", results) #open deleteDB_window
	return 'DELETED'

def createDB(results):
	logger.info("Inside createDB")
	ncurses.stdscr.clear()
	ncurses.stdscr2.clear()
	ncurses.stdscr3.clear()
	try:
		DB_Orchestrator.create_database(results[0]) #results is a list so pass in first index which is the new databases name.
	except:
		results[0] = CREATE_DB_ERROR
	ncurses.createDB_window(createDB_menu, "", "Close", results) #open createDB_window

#Used to load form to get name of new database to create and calls createDB()
def loadDB_createform():
	form = createDB_form
	function = 'createDB('
	form['options'][1]['command'] = function
	return form

#Used to load form to get name of database to delete and calls deleteDB()
def loadDB_deleteform(dbs):
	form = deleteDB_form
	function = 'deleteDB('
	form['options'][1]['command'] = function
	form['fields'][1]['type'] = dbs
	return form

#Used to load form to get name of database to export and calls exportDB()
def loadDB_exportform(dbs):
	form = exportDB_form
	function = 'exportDB('
	form['options'][1]['command'] = function
	form['fields'][0]['type'] = dbs
	return form

#Used to load form to get name of database to import and calls importDB()
def loadDB_importform():
	form = importDB_form
	function = 'importDB('
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
                                if nextMenu is not None and 'commands' in nextMenu:
                                    logger.info("Operations from table view {}".format(nextMenu))
                                    DB_Orchestrator.perform_bulk_operations(eval(nextMenu)['commands'])
                                    nextMenu = None

				if nextMenu is None:
					nextMenu = oldMenu
				logger.info(nextMenu)

				#Return back to main menu and login if database has been deleted
				if nextMenu == 'DELETED' or nextMenu == 'IMPORTED':
					ncurses.resetscreen()
					break

				if nextMenu == main_menu:
					ncurses.resetscreen()
					break

				#After user exports database change value of nextMenu to view database options menu.
				if nextMenu == 'EXPORTED':
					ncurses.resetscreen()
					nextMenu = storeold
					

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





