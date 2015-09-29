#!/usr/bin/env python

import curses
stdscr = curses.initscr() #initialize ncurses
curses.start_color() #allow colors

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

#Output strings
stdscr.addstr(0,0, "TESTING NCURSES", curses.color_pair(1))
stdscr.refresh()
stdscr.getch()

stdscr.addstr(5,35, 'Hello World!')
stdscr.refresh()
stdscr.getch()

#Terminating ncurses application
curses.endwin()