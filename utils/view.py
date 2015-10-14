class Dictionary:
	MENU = "menu"
	COMMAND = "command"
	EXITMENU = "exitmenu"
	FORM = "form"
	TEXT = "text"

login_form = {
	'title': "Login", 'type': Dictionary.FORM, 'subtitle': "Please login to your db account",
	'fields':[
		{'title': "Username: ", 'type': Dictionary.TEXT},
		{'title': "Password: ", 'type': Dictionary.TEXT}
	],
	'options': [
		{'title': "Back", 'type': Dictionary.COMMAND, 'command': 'processMenu(main_menu)'},
		{'title': "Continue", 'type': Dictionary.COMMAND, 'command': 'testfun()'}
	]
}


main_menu = {
	'title': "Main Menu", 'type': Dictionary.MENU, 'subtitle': "Please select an option...",
	'options':[
  		{ 'title': "Use MySQL databases", 'type': Dictionary.COMMAND, 'command': 'use_mysql()' },
    	{ 'title': "Use PostgreSQL databases", 'type': Dictionary.COMMAND, 'command': 'use_psql()' },
	{ 'title': "Login Test", 'type': Dictionary.COMMAND, 'command': 'login(ncurses)' },
		#Menu with a submenu
        { 'title': "Sebmenu preview", 'type': Dictionary.MENU, 'subtitle': "Please select an option...",
        	'options': [
        		{ 'title': "Option1", 'type': Dictionary.COMMAND, 'command': 'testfun()' },
          		{ 'title': "Option2", 'type': Dictionary.COMMAND, 'command': 'testfun()' },
          		{ 'title': "Option3", 'type': Dictionary.COMMAND, 'command': 'testfun()' },
			]#end submenu
        }
  ]#end of menu options
}#end of menu data

exit_menu = {
	'title': "Exit program?", 'type': Dictionary.MENU, 'subtitle': "Please select an action...",
	'options':[
  		{ 'title': "Yes", 'type': Dictionary.COMMAND, 'command': 'exit_program(ncurses)' },
  ]#end of exit_menu options
}#end of exit_menu data
