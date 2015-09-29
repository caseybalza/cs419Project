#!/usr/bin/env python
#Program Filename: main.py
#Authors: Casey Balza, Daryl Cooke, Nickolas Jurczak
#Date: 9/28/2015
#Description: A ncurses based program that mimics the use of phpmyadmin.

import curses
stdscr = curses.initscr() #initialize ncurses
curses.start_color() #allow colors

#Create color pairs.
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_CYAN)

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

stdscr.addstr(23,23, "Created By: Casey Balza, Daryl Cooke, & Nickolas Jurczak", curses.color_pair(2))
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

stdscr.getch()

#Terminating ncurses application
curses.endwin()
