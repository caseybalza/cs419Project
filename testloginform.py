import curses
import MySQLdb
import psycopg2
import os
import subprocess
import sys
import time
import curses.textpad

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
def testfun():
	stdscr.clear()
	stdscr.refresh()
	stdscr.addstr(2,2, "WORKING", curses.A_STANDOUT)
	stdscr.getch()

rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)
runform(login_form)
curses.endwin() #Terminating ncurses application


