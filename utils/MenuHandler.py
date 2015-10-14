import curses
import curses.textpad
from NcursesViewHandler import *

# Source to help create menus http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menu/


def runform(form, stdscr):

	h = curses.color_pair(1) #h is the coloring for a highlighted menu option
	n = curses.A_NORMAL #n is the coloring for a non highlighted menu option


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
def runmenu(menu, parent, start, stdscr):

	h = curses.color_pair(1) #h is the coloring for a highlighted menu option
	n = curses.A_NORMAL #n is the coloring for a non highlighted menu option


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

