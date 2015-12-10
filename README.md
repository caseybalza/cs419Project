#CS-419 Project

######Authors: Casey Balza, Daryl Cooke, Nickolas Jurczak

#VM Link
http://web.engr.oregonstate.edu/~cooked/CS_419/cs419VM_FinalSubmission.ova

#Background
Databases are rather interesting beasts, but the UIs available for them tend to fall into one of 3 camps:

	• web based
	
	• simple command line interface
	
	• custom, heavyweight, arcane GUIs that rarely look native
	
While there are exceptions to the above (such as FileMaker Pro), DB interfaces are lacking one major flavor
of interface: an ncurses based command line tool.

#Project Description

What I am looking for is relatively straightforward to describe: something along the lines of phpMyAdmin,
but CLI/ncurses based. This means a well implemented interface, with proper pagination of results, full
listing of tables, likely multiple screen ports (think frames on a web site), etc.

Unlike phpMyAdmin, this tool should work for either mysql or postgresql (preferred). Ideally, you will
implement both, and more grading consideration will be given if both are provided, but only one is required.

#Database

No DB will be provided for this project, but you will need to create your own test DBs locally on a VM.
VM creation is up to you, and no guidelines will be given.

#Useful information

	• These tools will be entirely written in python. That means the curses based CLI and any testing tools
	  you need to write.
	  
	• postgreSQL and mysql are very similar. But not quite the same.
	
	• While mysql is rarely used in production environments in larger corporations(at least as far as I can
	  find), postgresql is relatively common.
	  
	• You will need to create a VM for this project. Make sure you can recreate said VM, as you will need
	  to document this extensively for the final write-up. Scripting said creation in some fashion will likely
	  make your life much better.

#How to use program

##Libraries needed installed on Virtual Machine

####ncurses - Necessary for visual layout
##### steps to take installing on linux
1). Switch to sudo user (su root)
2). wget http://ftp.gnu.org/gnu/ncurses/ncurses-6.0.tar.gz
3). tar xzf ncurses-6.0.tar.gz
4). cd ncurses-6.0
5). ./configure --prefix=/opt/ncurses
6). make
7). make install
8). ls -la /opt/ncurses

In python import library
For example: import curses


####MySQLdb - Necessary to connect MySQL with Python
##### steps to take installing on linux
1). sudo apt-get install python-mysqldb

In python import library
For example: import MySQLdb

######Connect to MySQL database

db = MySQLdb.connect(host="hostname",
                     user="username",
                     passwd="some password",
                     db="name of database")

####psycopg2 - Necessary to connect to PostgreSQL with python
##### steps to take installing on linux
1). sudo apt-get install python-psycopg2

######Connect to PostgreSQL database

pdb = psycopg2.connect("dbname='Name of db' user='Name of user'")















