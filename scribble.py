#Displays information from MySQL server
def use_mysql():

	#Connect to MySQL database
	db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="password",
                     db="")

	#Must create cursor object to allow queries from mysql db
	cur = db.cursor()

	mysql_menu = {
		'title': "MySql databases", 'type': MENU, 'subtitle': "Please select an option...",
		'options':[
   	 ]#end of menu options
	}#end of menu data
	
	cur.execute("SHOW DATABASES;")
	for row in cur.fetchall():
		mysql_menu['options'].append({'title': row[0],'type': COMMAND, 'command': 'show_tables(row[0])' })

	processmenu(mysql_menu, main_menu)

#end use_mysql()

#Show tables from selected database
def show_tables(dbs):

	#Connect to MySQL database
	db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="password",
                     db="")

	#Must create cursor object to allow queries from mysql db
	cur = db.cursor()

	mysql_dbs_menu = {
		'title': dbs+" tables", 'type': MENU, 'subtitle': "Please select a table or action...",
		'options':[
   	 ]#end of menu options
	}#end of menu data

	cur.execute("USE "+dbs+";")
	cur.execute("SHOW TABLES;")
	for row in cur.fecthall():
		mysql_dbs_menu['options'].append({'title': dbs,'type': COMMAND, 'command': 'testfun()' })
	mysql_dbs_menu['options'].append({'title': "custom query",'type': COMMAND, 'command': 'testfun()' })
	processmenu(mysql_dbs_menu, mysql_menu)