class Dictionary:
	MENU = "menu"
	COMMAND = "command"
	EXITMENU = "exitmenu"
	FORM = "form"
	TEXT = "text"

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

deleteDB_menu = {
	'title': "Delete Database", 'type': Dictionary.MENU, 'subtitle': "", 'location': '',
	'options':[]#end of deleteDB_menu options
}#end of deleteDB_menu

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
