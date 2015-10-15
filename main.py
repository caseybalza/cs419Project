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


#Check if everything needed is installed and correct version, continue with program, else halt.
#stop = initiateProgram() #create instance of class initiateProgram
#stop = stop.versionCheck() #call versionCheck on the instance.
	
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
        DB_Orchestrator.select_database(dbs)
        #if databaseType == "PostgresSQL":
        #    postgresSQL_DB_Orchestrator.select_database(dbs)

        dbs_menu = {
                'title': dbs + " tables", 'type': Dictionary.MENU, 'subtitle': "Please select a table or action...",
                'options':[]#end of menu options
        }#end of menu data

        tables = DB_Orchestrator.show_tables()
        #tables = postgresSQL_DB_Orchestrator.show_tables()

        dbs_menu['options'].append({'title': "CUSTOM QUERY", 'type': Dictionary.COMMAND, 'command': 'testfun()' })
        for table in tables:
                action = os.path.join('show_table_contents(\"{}\", \"{}\")'.format(table, databaseType))
                dbs_menu['options'].append({'title': table, 'type': Dictionary.COMMAND, 'command': action })
        return dbs_menu
#end show_tables(dbs)

#Displays information from MySQL server
def use_mysql(DB_Orchestrator, results):
	#logininfo = eval(results)
	logininfo = results
	DB_Orchestrator.load("localhost", logininfo[0], logininfo[1], "", "MySQL")
	mysql_menu = {
		'title': "MySql databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
		'options':[]#end of menu options
	}#end of menu data

        databases = DB_Orchestrator.show_databases()
        for database in databases:
            action = os.path.join('show_tables(\"{}\", \"{}\")'.format(database, "MySQL"))
            mysql_menu['options'].append({'title': database, 'type': Dictionary.COMMAND, 'command': action })
        return mysql_menu
#end use_mysql()

def use_psql(DB_Orchestrator, results):
	DB_Orchestrator.load("", results[0], results[1], "postgres", "PostgresSQL")
        postgressql_menu = {
                'title': "PostgresSQL databases", 'type': Dictionary.MENU, 'subtitle': "Please select a database to use...",
                'options':[]#end of menu options
        }#end of menu data

        databases = DB_Orchestrator.show_databases()
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

def login(type):
	return ncurses.setuplogin(type)
	#return login_form

#MAIN PROGRAM
stop = 0;
if stop == 0:

	#mySQL_DB_Orchestrator = DatabaseOrchestrator("localhost", "root", "password", "", "MySQL")
	#postgresSQL_DB_Orchestrator = DatabaseOrchestrator("", "ubuntu", "", "postgres", "PostgresSQL")
	DB_Orchestrator = DatabaseOrchestrator()
	#rows, columns = os.popen('stty size', 'r').read().split()
	#rows = int(rows)
	#columns = int(columns)
	#processmenu(main_menu)
	ncurses = NCursesHandler()
	results=ncurses.startmenu()
	back_list_stack = [] #Create a stack to hold path
	back_list_stack.append(results) #Add main menu to path
	nextMenu = eval(results)
	ncurses.resetscreen()
	results = ncurses.processmenu(nextMenu)
	back_list_stack.append(results)#Add option selected from Main menu to path
	storeold = results;
	while 1:

		size = len(back_list_stack)
		oldMenu = nextMenu
		nextMenu = eval(results)
		if nextMenu == storeold:
			back_list_stack.pop()
			back_list_stack.pop()
			size = len(back_list_stack)
		ncurses.resetscreen()
		results = ncurses.processmenu(nextMenu, eval(back_list_stack[(size - 2)]))
		storeold = oldMenu
		back_list_stack.append(results)
		
		



#curses.endwin() #Terminating ncurses application





