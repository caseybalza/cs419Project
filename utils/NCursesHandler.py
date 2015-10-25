import curses
import MySQLdb
import psycopg2
import os
import subprocess
import sys
import time
import curses.textpad
import pprint
from utils.view import *
from math import ceil
from utils.constants import *
from Logger import get_logger


class NCursesHandler:

	def __init__(self):


		self.stdscr = curses.initscr() #initialize ncurses
                self.logger = get_logger("NcursesHandler")

		curses.noecho() # Disables automatic echoing of key presses (prevents program from input each key twice)
		curses.cbreak() # Runs each key as it is pressed rather than waiting for the return key to pressed)
		curses.start_color() #allow colors
		self.stdscr.keypad(1) # Capture input from keypad allow to move around on menus
		self.stdscr.bkgd(' ', curses.color_pair(2))

		#window for top menu bar
		self.stdscr2 = curses.newwin(3, 80, 0, 0)

		#window help menu
		self.stdscr3 = curses.newwin(18, 44, 7, 18)

		#Create color pairs.
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
		curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
		curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)
		curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
		curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_RED)
		curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_GREEN)
		curses.init_pair(11, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_CYAN)
		curses.init_pair(13, curses.COLOR_YELLOW, curses.COLOR_BLUE)
		curses.init_pair(14, curses.COLOR_GREEN, curses.COLOR_BLACK)

		self.h = curses.color_pair(14) #h is the coloring for a highlighted menu option
		self.n = curses.A_NORMAL #n is the coloring for a non highlighted menu option

	#Clears screen and outputs exit menu
	def exit_window(self, new_menu, location, old_menu):
		self.stdscr.clear
		self.processmenu(new_menu, location, old_menu)
	#end exit_window

	#closes program
	def exit_program(self):
		curses.endwin() #Terminating ncurses application
		sys.exit()
	#end exit_program

	#Top Menu Bar
	def top_bar_menu(self, location):
                self.stdscr2.clear()
		self.stdscr2.border(124, 124, 61, 61, 35, 35, 35, 35)
		self.stdscr2.bkgd(' ', curses.color_pair(1))
		self.stdscr2.addstr(1,2, 'Location:')
		self.stdscr2.addstr(1,11, location)
		self.stdscr2.addstr(1,67, 'H', curses.A_UNDERLINE)
		self.stdscr2.addstr(1,68, 'elp')
		self.stdscr2.addstr(1,73, 'E', curses.A_UNDERLINE)
		self.stdscr2.addstr(1,74, 'xit')
		self.stdscr2.refresh()
	#end top_menu_bar

	def help_window(self, new_menu, location, old_menu):
		
		self.stdscr3.border(0)
		self.stdscr3.bkgd(' ', curses.color_pair(8))
		self.stdscr3.addstr(3,2, 'The "Location" in the top menu bar tells')
		self.stdscr3.addstr(4,2, 'you where you currently are in a SQL')
		self.stdscr3.addstr(5,2, 'server.')
		self.stdscr3.addstr(7,2, '"Shift + E" to exit program')
		self.stdscr3.addstr(8,2, '"Shift + H" to to bring up help menu')
		self.stdscr.refresh()
		self.stdscr2.refresh()
		self.stdscr3.refresh()
		self.processmenu(new_menu, location, old_menu)
	#end help_window

	def createDB_window(self, new_menu, location, old_menu, results):
		self.stdscr.clear
		self.stdscr2.clear
		self.stdscr3.clear
		self.stdscr3.border(0)
		self.stdscr3.bkgd(' ', curses.color_pair(8))
		self.stdscr3.addstr(3,2, 'Redirecting you back to Main Menu')
		
		if results[0] == CREATE_DB_ERROR:
			self.stdscr3.addstr(10,2, results[0]) #Just output error message
		else:
			self.stdscr3.addstr(9,2, "Success! " + results[0] + " database created." ) #output success message + db name

		self.stdscr.refresh()
		self.stdscr2.refresh()
		self.stdscr3.refresh()
		self.stdscr.clear
		self.processmenu(new_menu, location, old_menu)
	#end createDB_window

	def deleteDB_window(self, new_menu, location, old_menu, results):
		self.stdscr.clear
		self.stdscr2.clear
		self.stdscr3.clear
		self.stdscr3.border(0)
		self.stdscr3.bkgd(' ', curses.color_pair(8))
		self.stdscr3.addstr(3,2, 'Redirecting you back to Main Menu')
		
		if results[0] == DELETE_DB_ERROR:
			self.stdscr3.addstr(10,2, results[0]) #Just output error message
		elif results[0] == DELETE_WRONG_DB_ERROR:
			self.stdscr3.addstr(10,2, results[0]) #Just output error message
		else:
			self.stdscr3.addstr(9,2, "Success! " + results[0] + " database deleted." ) #output success message + db name

		self.stdscr.refresh()
		self.stdscr2.refresh()
		self.stdscr3.refresh()
		self.stdscr.clear
		self.processmenu(new_menu, location, old_menu)
	#end deleteDB_window

	#properly loads form, ,returns values entered
	def runform(self, form, location, parent):

		fieldcount = len(form['fields'])# how many fields there are in the form
		optioncount = len(form['options'])# how many options there are

		pos=0
		oldpos=None
		x = None
		optionselect = 0
		results = []
		wins = []
		boxs = []
		returnvalue = {'fields':None, 'option':None}
		# Display all fields

		for index in range(fieldcount):
		
			if index < fieldcount:
				self.stdscr.addstr(5+index,20, "%s" % (form['fields'][index]['title']), self.n)
				index += 1

		self.stdscr.border(0)
		self.stdscr.addstr(2,35, form['title'], curses.A_STANDOUT) # Title for this menu
		self.stdscr.addstr(4,16, form['subtitle'], curses.A_BOLD) # Subtitle for this menu
		self.stdscr.addstr(28,23, "Created By: Casey Balza, Daryle Cooke, & Nick Jurczak", curses.color_pair(13))
		self.stdscr.refresh()

		#top menu bar
		self.top_bar_menu(location)

		#display options			

		for index in range(optioncount):
			textstyle = self.n
	
			if pos==fieldcount:
				if optionselect==index:
					textstyle = self.h
			self.stdscr.addstr(5+5*fieldcount,20+(index*20), "%s" % (form['options'][index]['title']), textstyle)
		self.stdscr.refresh()

		for index in range(fieldcount):
			if form['fields'][index]['type'] == Dictionary.TEXT:
				next = index
				if len(boxs) <= index:
					wins.append(curses.newwin(1,30,5+index,20+len(form['fields'][index]['title'])))
					boxs.append(curses.textpad.Textbox(wins[index]))
				text = None
				def check(input):
					if input == 14:
						boxs[index].gather()
					if input == curses.KEY_DOWN:
						boxs[index].gather()
					if input == curses.KEY_UP:
						next -= 2
						boxs[index].gather()
				#boxs[index].do_command(check)
				text = boxs[index].edit()
				if len(results)>index:
					results[index] = text.strip()
				else:
					results.append(text.strip())
				index = next
			else:
				boxs.append(None)
				results.append(form['fields'][index]['type']) #Used for deleting a database
		sys.stdout.flush()
		while x !=ord('\n'):
			if pos != oldpos:
				oldpos = pos
				for index in range(optioncount):
					textstyle = self.n

					if pos==index:
						textstyle = self.h
					self.stdscr.addstr(5+5*fieldcount,20+(index*20), "%s" % (form['options'][index]['title']), textstyle)
				self.stdscr.refresh()

			x = self.stdscr.getch()
			if x == curses.KEY_RIGHT:
				pos += 1
				pos %= optioncount
			elif x == curses.KEY_LEFT:
				if pos > 0:
					pos -= 1
				else:
					pos = optioncount -1
			elif x == 69:
				return 'exit'
			elif x == 72:
				return 'help'
		if pos is 0:
			return str(parent)
		else:
			#returnvalue['fields'] = results
			#returnvalue['option'] = form['options'][pos]
			return form['options'][pos]['command']+str(results)+')'



	# This function displays the appropriate menu and returns the option selected
	def runmenu(self, menu, parent, start, location):

		# work out what text to display as the last menu option
		if parent is None:
			lastoption = 0 #display no lastoption
		elif parent == "No":
			lastoption = "No"
		elif parent == "Close":
			lastoption = "Close"
		else:
			lastoption = "Return to %s" % parent['title']

		optioncount = len(menu['options']) # how many options in this menu

		pos=0 #pos is the zero-based index of the hightlighted menu option. Every time runmenu is called,
			  # position returns to 0, when runmenu ends the position is returned and tells the program what opt$
		oldpos=None # used to prevent the screen being redrawn every time
		x = None #control for while loop, let's you scroll through options until return key is pressed then returns pos to program
		         # Loop until return key is pressed
		back = False # used for BACK menu option
		while x !=ord('\n'):
			if pos != oldpos:
				oldpos = pos
				#self.stdscr.border(0)
				self.stdscr.addstr(5,35, menu['title'], curses.A_STANDOUT) # Title for this menu
				self.stdscr.addstr(7,16, menu['subtitle'], curses.A_BOLD) #Subtitle for this menu
				self.stdscr.addstr(28,23, "Created By: Casey Balza, Daryl Cooke, & Nickolas Jurczak", curses.color_pair(13))
				self.stdscr.refresh()
				
				#top menu bar
				self.top_bar_menu(location)

				# Display all the menu items, showing the 'pos' item highlighted
				count = 0
				for index in range(optioncount):
					index += start
					textstyle = self.n

					if pos==count:
						textstyle = self.h

					if count < 7 and index < optioncount:
						self.stdscr.addstr(8+count,20, "%d - %s" % (count+1, menu['options'][index]['title']), textstyle)
						count += 1

					elif count == 7:
						self.stdscr.addstr(8+count,20, "%d - %s" % (count+1, "MORE"), textstyle)
						count += 1
					
				if start >= 7:
					self.stdscr.addstr(8+count,20, "%d - %s" % (count+1, "BACK"), textstyle)
					count += 1
					back = True
			
				# Now display Exit/Return at bottom of menu
				if lastoption != 0 and lastoption != "Close":
					textstyle = self.n

					if pos==count:
						textstyle = self.h
					self.stdscr.addstr(8+count,20, "%d - %s" % (count+1, lastoption), textstyle)
					self.stdscr.refresh()
					# finished updating screen

				if lastoption == "Close":
					if pos==count:
						textstyle = self.h
					self.stdscr.addstr(23, 37,  "%s" % (lastoption), textstyle)
					self.stdscr3.refresh()

			x = self.stdscr.getch() # Gets user input

			# What is user input?
			max = 0
			if optioncount <= 8:
				max = ord(str(optioncount+1))
			else:
				max = ord('9')
			if x >= ord('1') and x <= max:
				pos = x - ord('0') - 1 # convert keypress back to a number, then subtract 1 to get index
			elif x == 258: # down arrow
				if(lastoption == 0):
					if pos < count - 1:
						pos += 1
					else: pos = pos
				else:
					if pos < count:
						pos += 1
					else: pos = pos
			elif x == 259: # up arrow
				if pos > 0:
					pos += -1
				else: pos = 0
			elif x == 69: # if user entered 'E' (shift + e) from the .getch()
				pos = 'exit'
				return pos
			elif x == 72: # if user entered 'H' (shift + h) from the .getch()
				pos = 'help'
				return pos
		# return index of the selected item
		if pos == 9 or pos == optioncount or pos == count:
			return -1
		elif pos == 7:
			return -2
		elif pos == 8 and back == True or pos == count - 1 and back == True:
			return -3
		else:
			pos += start

			return pos
	#end runmenu()


	# This function calls showmenu and then acts on the selected item
	def processmenu(self, menu, location, parent=None ):
		optioncount = len(menu['options'])
		start = 0
		if menu['type'] == Dictionary.MENU:
			while (1): #Loop until the user exits the menu
				getin = self.runmenu(menu, parent, start, location)
				if getin == -1 or getin == optioncount:
					return str(parent)
				elif getin == 'exit': #if user input 'E' (shift + e) bring up exit menu
					self.stdscr.clear()
					saying = "No"
					self.exit_window(exit_menu, "", saying) #open exit window
					self.stdscr.clear()#Clear screen of exit menu if user did not exit
				elif getin == 'help': #if user input 'E' (shift + e) bring up exit menu
					self.stdscr.clear()
					saying = "Close"
					self.help_window(help_menu, "", saying) #open exit window
					self.stdscr.clear()#Clear screen of exit menu if user did not exit
				elif getin == -2:
					start += 7
					self.stdscr.clear()
				elif getin == -3:
					start -= 7
					self.stdscr.clear()
				elif menu['options'][getin]['type'] == Dictionary.COMMAND:
					curses.def_prog_mode()    # save curent curses environment
					self.stdscr.clear() #clears previous screen
					result = (menu['options'][getin]['command']) # Get command into variable
					if(result == 'EXIT'):
						self.exit_program()
					return result#Call the command
					#stdscr.clear() #clears previous screen on key press and updates display based on pos
					#curses.reset_prog_mode()   # reset to 'current' curses environment
					#curses.curs_set(1)         # reset doesn't do this right
					#curses.curs_set(0)
				elif menu['options'][getin]['type'] == Dictionary.MENU:
					self.stdscr.clear() #clears previous screen on key press and updates display based on pos
					self.processmenu(menu['options'][getin], menu) # display the submenu
					self.stdscr.clear() #clears previous screen on key press and updates display based on pos

		else:
			if parent is None:
				parent = main_menu
			while (1):
				getin = self.runform(menu, location, parent)
				if getin == 'help':
					self.stdscr.clear()
					saying = "Close"
					self.help_window(help_menu, "", saying)
					self.stdscr.clear()
				elif getin == 'exit':
					self.stdscr.clear()
					saying = "No"
					self.exit_window(exit_menu, "", saying)
					self.stdscr.clear()
				else:
					return getin
			#return result['option']['command']
			#return result['option']['command']+str(result['fields'])+')'
	#end processmenu()
	
        def draw_table_help_box(self):
                box = curses.newwin(10, 40, 3, 20)
                box.box()
                box.border('|','|','-','-','+','+','+','+')
                box.addstr(1, 2, "{:^36}".format("Table View Help Menu"), curses.A_UNDERLINE)
                box.addstr(3, 2, "{:<36}".format("Left arrow: scrolls columns left"))
                box.addstr(4, 2, "{:<36}".format("Right arrow: scrolls columns right"))
                box.addstr(5, 2, "{:<36}".format("Down arrow: scroll entries down"))
                box.addstr(6, 2, "{:<36}".format("Up arrow: scroll entries up"))
                box.addstr(8, 2, "{:^36}".format("Close"), curses.color_pair(3))
                box.refresh()
                x = box.getch()
                while x != ord('\n'):
                    x = box.getch()
                box.clear()

        def draw_table_bottom_bar(self):
                box = curses.newwin(1, 80, 22, 0)
                box.box()
                box.bkgd(' ', curses.color_pair(1))
                #box.border('|','|','-','-','+','+','+','+')
                try:
                    box.addstr(0, 0, "{:2}".format(""))
                except:
                    pass

                box.addstr(0, 2, "{:<1}".format("D"), curses.A_UNDERLINE)
                box.addstr(0, 3, "{:<9}".format("elete"))

                box.addstr(0, 12, "{:<1}".format("U"), curses.A_UNDERLINE)
                box.addstr(0, 13, "{:<9}".format("pdate"))

                box.addstr(0, 22, "{:<1}".format("I"), curses.A_UNDERLINE)
                box.addstr(0, 23, "{:<9}".format("nsert"))

                try:
                    box.addstr(0, 30, "{:50}".format(""))
                except:
                    pass

                box.refresh()

        def draw_table(self, tableName, contents, location):
                self.draw_table_bottom_bar()
                curses.curs_set(0)
                highlightText = curses.color_pair(3)
                normalText = curses.A_NORMAL
                schema = contents[0]
                records = contents[1]
                numCols = len(schema)
                numRows = len(records)
                maxEntitiesOnPage = 15

                box = curses.newwin(maxEntitiesOnPage + 4, 80, 3, 0)
                box.box()
                box.border('|','|','-','-','+','+','+','+')
                box.addstr(1, 2, "{} table".format(tableName), curses.A_UNDERLINE)
                box.addstr(2, 2, "{:>4.4}".format(""), curses.A_UNDERLINE)
                box.addstr(2, 6, "{:>24.20}".format(schema[0][0] if numCols > 0 else ""), curses.A_UNDERLINE)
                box.addstr(2, 30, "{:>24.20}".format(schema[1][0] if numCols > 1 else ""), curses.A_UNDERLINE)
                box.addstr(2, 54, "{:>24.20}".format(schema[2][0] if numCols > 2 else ""), curses.A_UNDERLINE)
                box.keypad(1)

                pages =  int(ceil(numRows / maxEntitiesOnPage))
                rowPosition = 1
                columnPosition = 0
                page = 1
                for i in range(1, maxEntitiesOnPage + 1):
                    if i == rowPosition:
                        textType = highlightText
                    else:
                        textType = normalText

                    box.addstr(i + 2, 2, str(i) + " - ", textType)

                    for j in range(0, 3):
                        box.addstr(i + 2 - (maxEntitiesOnPage * (page - 1)), 6 + (24 * j), "{:>24.20}".format(
                            str(records[i - 1][j + columnPosition]) if numCols > j + columnPosition else ""), normalText)

                    if i == numRows:
                        break
                
                sys.stdout.flush()
                self.top_bar_menu(location)
                box.refresh()
                x = box.getch()
                while x != 69:
                    if x == curses.KEY_DOWN:
                        if page == 1:
                            if rowPosition < i:
                                rowPosition += 1
                            else:
                                if pages > 1:
                                    page += 1
                                    rowPosition = 1 + (maxEntitiesOnPage * (page - 1))
                        elif page == pages + 1:
                            if rowPosition < numRows:
                                rowPosition += 1
                        else:
                            if rowPosition < maxEntitiesOnPage + (maxEntitiesOnPage * (page - 1)):
                                rowPosition += 1
                            else:
                                page += 1
                                rowPosition = 1 + (maxEntitiesOnPage * (page - 1))
                    if x == curses.KEY_UP:
                        if page == 1:
                            if rowPosition > 1:
                                rowPosition -= 1
                        else:
                            if rowPosition> (1 + (maxEntitiesOnPage * (page - 1))):
                                rowPosition -= 1
                            else:
                                page -= 1
                                rowPosition = maxEntitiesOnPage + (maxEntitiesOnPage * (page - 1))
                    if x == curses.KEY_LEFT:
                        if columnPosition > 0:
                            columnPosition -= 1
                    if x == curses.KEY_RIGHT:
                        if columnPosition < numCols - 3:
                            columnPosition += 1
                    #Help
                    if x == 72:
                        self.draw_table_help_box()
                    #Delete
                    if x == 68:
                        self.logger.info("Delete row {}".format(rowPosition))
                    #Update
                    if x == 85:
                        self.logger.info("Update row {}".format(rowPosition))
                    #Insert
                    if x == 73:
                        self.logger.info("Insert into table {}".format(tableName))
                    if x == ord("\n") and numRows != 0:
                        self.logger.info("Row {} selected".format(rowPosition))
                        #Item selected, does nothing currently

                    box.erase()
                    box.border('|','|','-','-','+','+','+','+')

                    box.addstr(1, 2, "{} table".format(tableName), curses.A_UNDERLINE)
                    box.addstr(2, 2, "{:>4.4}".format(""), curses.A_UNDERLINE)
                    for i in range(0, 3):
                        box.addstr(2, 6 + (24 * i), "{:>24.20}".format(schema[i + columnPosition][0] if numCols > i + columnPosition else ""), curses.A_UNDERLINE)

                    for i in range(1 + (maxEntitiesOnPage * (page - 1)), maxEntitiesOnPage + 1 + (maxEntitiesOnPage * (page - 1))):
                        if (i + (maxEntitiesOnPage * (page - 1)) == rowPosition + (maxEntitiesOnPage * (page - 1))):
                            textType = highlightText
                        else:
                            textType = normalText

                        box.addstr(i + 2 - (maxEntitiesOnPage * (page - 1)), 2, str(i) + " - ", textType)

                        
                        for j in range(0, 3):
                            box.addstr(i + 2 - (maxEntitiesOnPage * (page - 1)), 6 + (24 * j), "{:>24.20}".format(
                                str(records[i - 1][j + columnPosition]) if numCols > j + columnPosition else ""), normalText)

                        if i == numRows:
                            break

                    box.refresh()
                    x = box.getch()

                curses.endwin()
                
	def setuplogin(self, type):
		form = login_form
		function = None
		if type == 0:
			function = 'use_mysql('
		elif type == 1:
			function = 'use_psql('
		form['options'][1]['command'] = function
		return form
	
	# Starts program with main menu
	def startmenu(self):
		return self.processmenu(main_menu, "", None)

	def testfun(self):
		self.stdscr.clear()
		self.stdscr.refresh()
		self.stdscr.addstr(2,2, "WORKING", curses.A_STANDOUT)
		self.stdscr.getch()
	#end testfun()

	def resetscreen(self):
		self.stdscr.clear()
		self.stdscr2.clear()
		self.stdscr.refresh()
		self.stdscr2.refresh()
	#end resetscreen()

