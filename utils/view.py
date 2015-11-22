class Dictionary:
	MENU = "menu"
	COMMAND = "command"
	EXITMENU = "exitmenu"
	FORM = "form"
	TEXT = "text"
	SELECTION = "selection"
	TRUEFALSE = "true/false"

main_menu = {
	'title': "Main Menu", 'type': Dictionary.MENU, 'subtitle': "Please select an option...", 'location': '/',
	'options':[
  		{ 'title': "Use MySQL databases", 'type': Dictionary.COMMAND, 'command': 'login(0)' },
    	{ 'title': "Use PostgreSQL databases", 'type': Dictionary.COMMAND, 'command': 'login(1)' }
	#{ 'title': "Login Test", 'type': Dictionary.COMMAND, 'command': 'login(ncurses)' },
  ]#end of menu options
}#end of menu data

exit_menu = {
	'title': "Exit program?", 'type': Dictionary.MENU, 'subtitle': "Please select an action...", 'location': '',
	'options':[
  		{ 'title': "Yes", 'type': Dictionary.COMMAND, 'command': 'EXIT' },
  ]#end of exit_menu options
}#end of exit_menu data

help_menu = {
	'title': "HELP MENU", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of exit_menu options
}#end of help_menu data

createDB_menu = {
	'title': "Create New Database", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of createDB_menu_menu options
}#end of createDB_menu data

createTable_menu = {
	'title': "Create New Table", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of createTable_menu options
}#end of createTable_menu data

deleteDB_menu = {
	'title': "Delete Database", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of deleteDB_menu options
}#end of deleteDB_menu

exportDB_menu = {
	'title': "Export Database", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of exportDB_menu options
}#end of exportDB_menu

importDB_menu = {
	'title': "Import Database", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of importDB_menu_menu options
}#end of importDB_menu data

login_form = {
	'title': "Login", 'type': Dictionary.FORM, 'subtitle': "Please login to your db account", 'location': '',
	'fields':[
		{'title': "Username: ", 'type': Dictionary.TEXT},
		{'title': "Password: ", 'type': Dictionary.TEXT}
	],
	'options': [
		{'title': "Back", 'type': Dictionary.COMMAND, 'command': str(main_menu)},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': ''}
	]
}

createDB_form = {
	'title': "Create New Database", 'type': Dictionary.FORM, 'subtitle': "Please enter the name of your new database to create", 'location': '',
	'fields':[
		{'title': "New Database Name: ", 'type': Dictionary.TEXT}
	],
	'options': [
		{'title': "Back"},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': ''}
	]
}

createTable_form = {
	'title': "Create New Table", 'type': Dictionary.FORM, 'subtitle': "Please enter the name of your new table", 'location': '',
	'fields':[
		{'title': "New Table Name: ", 'type': Dictionary.TEXT}
	],
	'options': [
		{'title': "Back"},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': 'createTable('}
	]
}

createEntity_form = {
	'title': "Add field", 'type': Dictionary.FORM, 'subtitle': "Please fill the following attributes", 'location': '',
	'fields':[
		{'title': "name: ", 'type': Dictionary.TEXT},
		{'title': "type: ", 'type': Dictionary.SELECTION, 'choices':["VARCHAR", "TINYINT", "TEXT", "DATE", "SMALLINT", "MEDIUMINT", "INT", "BIGINT", "FLOAT", "DOUBLE", "DECIMAL", "DATETIME", "TIMESTAMP", "TIME", "YEAR", "CHAR", "TINYBLOB", "TINYTEXT", "BLOB", "MEDIUMBLOB", "MEDIUMTEXT", "LONGBLOB", "LONGTEXT", "ENUM", "SET", "BIT", "BOOL", "BINARY", "VARBINARY"]},
		{'title': "length/values: ", 'type': Dictionary.TEXT},
		{'title': "collation: ", 'type': Dictionary.SELECTION, 'choices':["", "armscii8_bin", "armscii8_general_ci", "ascii_bin", "ascii_general_ci", "big5_bin", "big5_chinese_ci", "binary", "cp1250_bin", "cp1250_croatian_ci", "cp1250_czech_cs", "cp1250_general_ci", "cp1250_polish_ci", "cp1251_bin", "ujis_bin", "utf8_bin"]},
		{'title': "attributes: ", 'type': Dictionary.SELECTION, 'choices':["", "BINARY", "UNSIGNED", "UNSIGNED ZEROFILL", "ON UPDATE CURRENT_TIMESTAMP"]},
		{'title': "NULL: ", 'type': Dictionary.TRUEFALSE},
		{'title': "default: ", 'type': Dictionary.TEXT},
		{'title': "auto increment: ", 'type': Dictionary.TRUEFALSE},
		{'title': "special: ", 'type': Dictionary.SELECTION, 'choices':["NONE", "PRIMARY KEY", "INDEX", "UNIQUE", "FULLTEXT"]}
	],
	'options': [
		{'title': "Back"},
		{'title': "Finished", 'type': Dictionary.COMMAND, 'command': 'getEntityStr('},
		{'title': "Add Another Field", 'type': Dictionary.COMMAND, 'command': 'continue'}
	]
}

deleteDB_form = {
	'title': "Delete this database?", 'type': Dictionary.FORM, 'subtitle': "Please type in the name of the database to confirm.", 'location': '',
	'fields':[
		{'title': "Confirm Delete: ", 'type': Dictionary.TEXT},
		{'title': "", 'type': ""}
	],
	'options': [
		{'title': "Back"},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': ''}
	]
}

exportDB_form = {
	'title': "Export this database?", 'type': Dictionary.FORM, 'subtitle': "Are you sure you want to export this database?", 'location': '',
	'fields':[
		{'title': "", 'type': ""}
	],
	'options': [
		{'title': "Back"},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': ''}
	]
}

importDB_form = {
	'title': "Import Database", 'type': Dictionary.FORM, 'subtitle': "Please enter the name of the database file to import", 'location': '',
	'fields':[
		{'title': "File Name: ", 'type': Dictionary.TEXT}
	],
	'options': [
		{'title': "Back"},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': ''}
	]
}
