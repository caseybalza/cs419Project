class Dictionary:
	MENU = "menu"
	COMMAND = "command"
	EXITMENU = "exitmenu"
	FORM = "form"
	TEXT = "text"

main_menu = {
	'title': "Main Menu", 'type': Dictionary.MENU, 'subtitle': "Please select an option...",
	'options':[
  		{ 'title': "Use MySQL databases", 'type': Dictionary.COMMAND, 'command': 'login(0)' },
    	{ 'title': "Use PostgreSQL databases", 'type': Dictionary.COMMAND, 'command': 'login(1)' }
	#{ 'title': "Login Test", 'type': Dictionary.COMMAND, 'command': 'login(ncurses)' },
  ]#end of menu options
}#end of menu data

exit_menu = {
	'title': "Exit program?", 'type': Dictionary.MENU, 'subtitle': "Please select an action...",
	'options':[
  		{ 'title': "Yes", 'type': Dictionary.COMMAND, 'command': 'EXIT' },
  ]#end of exit_menu options
}#end of exit_menu data

help_menu = {
	'title': "HELP MENU", 'type': Dictionary.MENU, 'subtitle': "",
	'options':[]#end of exit_menu options
}#end of exit_menu data

login_form = {
	'title': "Login", 'type': Dictionary.FORM, 'subtitle': "Please login to your db account",
	'fields':[
		{'title': "Username: ", 'type': Dictionary.TEXT},
		{'title': "Password: ", 'type': Dictionary.TEXT}
	],
	'options': [
		{'title': "Back", 'type': Dictionary.COMMAND, 'command': str(main_menu)},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': 'use_mysql()'}
	]
}
