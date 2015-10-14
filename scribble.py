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
#end show_tables(dbs)

#Displays information from postgresql server
def use_psql():

	#Connect to a postgresql database
	db = psycopg2.connect("dbname='postgres' user='ubuntu'")
	#Must create cursor object to allow queries from postgresql db
	cur = db.cursor()

	postgresql_menu = {
		'title': "PostGreSql databases", 'type': MENU, 'subtitle': "Please select an option...",
		'options':[
   	 ]#end of menu options
	}#end of menu data
	
	cur.execute("SELECT * FROM pg_database")
	for row in cur.fetchall():
		postgresql_menu['options'].append({'title': row[0],'type': COMMAND, 'command': 'show_tables(row[0])' })

	processmenu(postgresql_menu, main_menu)

#end use_mysql()

#Show tables from selected database
def show_tables(dbs):

	#Connect to a postgresql database
	db = psycopg2.connect("dbname="+dbs+" user='ubuntu'")
	#Must create cursor object to allow queries from postgresql db
	cur = db.cursor()

	postgresql_dbs_menu = {
		'title': dbs+" tables", 'type': MENU, 'subtitle': "Please select a table or action...",
		'options':[
   	 ]#end of menu options
	}#end of menu data

	cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
	for row in cur.fecthall():
		postgresql_dbs_menu['options'].append({'title': dbs,'type': COMMAND, 'command': 'testfun()' })
	postgresql_dbs_menu['options'].append({'title': "custom query",'type': COMMAND, 'command': 'testfun()' })
	processmenu(postgresql_dbs_menu, mysql_menu)
#end show_tables(dbs)
