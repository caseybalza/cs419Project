#!/usr/bin/env python
#Program Filename: main.py
#Authors: Casey Balza, Daryl Cooke, Nickolas Jurczak
#Date: 9/28/2015
#Description: A ncurses based program that mimics the use of phpmyadmin.

import curses
import MySQLdb

#Connect to MySQL database
db = MySQLdb.connect(host="localhost",
                     user="",
                     passwd="",
                     db="classicmodels")

#Must create cursor object to allow queries from db
cur = db.cursor()

stdscr = curses.initscr() #initialize ncurses
curses.start_color() #allow colors

#Create color pairs.
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

#Set background color of main screen.
stdscr.bkgd(' ', curses.color_pair(2))
stdscr.refresh()

#Create top menu bar
stdscr2 = curses.newwin(3, 80, 0, 0)
stdscr2.border(0)
stdscr2.bkgd(' ', curses.color_pair(3))
stdscr2.refresh()

#Create main menu window on starting page.
stdscr3 = curses.newwin(7, 30, 7, 26)
stdscr3.border(0)
stdscr3.bkgd(' ', curses.color_pair(1))
stdscr3.refresh()

#Create window for outputting MySQL databases.
stdscr4 = curses.newwin(13, 25, 15, 3)
stdscr4.border(0)
stdscr4.bkgd(' ', curses.color_pair(4))
stdscr4.refresh()

#Create window for outputting MySQL db classicmodels Tables.
stdscr5 = curses.newwin(13, 24, 15, 29)
stdscr5.border(0)
stdscr5.bkgd(' ', curses.color_pair(5))
stdscr5.refresh()

#Create window for outputting MySQL db classicmodels customerName Table.
stdscr6 = curses.newwin(13, 24, 15, 54)
stdscr6.border(0)
stdscr6.bkgd(' ', curses.color_pair(6))
stdscr6.refresh()

#Output content into windows
stdscr.addstr(29,23, "Created By: Casey Balza, Daryl Cooke, & Nickolas Jurczak", curses.color_pair(2))
stdscr.refresh()

stdscr2.addstr(1,1, '"Program Title"')
stdscr2.addstr(1,19, 'Q', curses.A_UNDERLINE)
stdscr2.addstr(1,20, 'uit')
stdscr2.addstr(1,25, 'H', curses.A_UNDERLINE)
stdscr2.addstr(1,26, 'elp')
stdscr2.refresh()

stdscr3.addstr(1,10, 'Main Menu', curses.A_STANDOUT)
stdscr3.addstr(3,6, 'Load MySQL DB')
stdscr3.addstr(4,6, 'Load PostgreSQL DB')
stdscr3.refresh()

stdscr4.addstr(1,5, 'MySQL databases', curses.A_STANDOUT)
stdscr4.refresh()

cur.execute("SHOW DATABASES;")
i = 3
for row in cur.fetchall():
	stdscr4.addstr(i,3, row[0])
	i += 1
stdscr4.refresh()

stdscr5.addstr(1,1, '"classicmodels" tables', curses.A_STANDOUT)
stdscr5.refresh()

cur.execute("SHOW TABLES;")
i = 3
for row in cur.fetchall():
	stdscr5.addstr(i,3, row[0])
	i += 1
stdscr5.refresh()

stdscr6.addstr(1,1, '"customerName" table', curses.A_STANDOUT)
stdscr6.addstr(2,1, '"from "classicmodels"', curses.A_STANDOUT)
stdscr6.refresh()

cur.execute("SELECT customerName FROM customers ORDER BY customerNumber ASC LIMIT 5")
i = 3
for row in cur.fetchall():
	stdscr6.addstr(i,1, row[0])
	i += 1
stdscr6.refresh()
	
stdscr.getch()

#Terminating ncurses application
curses.endwin()


