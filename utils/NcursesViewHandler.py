import curses

MENU = "menu"
COMMAND = "command"
EXITMENU = "exitmenu"
FORM = "form"
TEXT = "text"


login_form = {
	'title': "Login", 'type': FORM, 'subtitle': "Please login to your db account",
	'fields':[
		{'title': "Username: ", 'type': TEXT},
		{'title': "Password: ", 'type': TEXT}
	],
	'options': [
		{'title': "Back", 'type': COMMAND, 'command': 'processMenu(main_menu)'},
		{'title': "Continue", 'type': COMMAND, 'command': 'testfun()'}
	]
}

main_menu = {
	'title': "Main Menu", 'type': MENU, 'subtitle': "Please select an option...",
	'options':[
  		{ 'title': "Use MySQL databases", 'type': COMMAND, 'command': 'use_mysql()' },
    	{ 'title': "Use PostgreSQL databases", 'type': COMMAND, 'command': 'use_psql()' },
		#Menu with a submenu
        { 'title': "Sebmenu preview", 'type': MENU, 'subtitle': "Please select an option...",
        	'options': [
        		{ 'title': "Option1", 'type': COMMAND, 'command': 'testfun()' },
          		{ 'title': "Option2", 'type': COMMAND, 'command': 'testfun()' },
          		{ 'title': "Option3", 'type': COMMAND, 'command': 'testfun()' },
			]#end submenu
        }
  ]#end of menu options
}#end of menu data

exit_menu = {
	'title': "Exit program?", 'type': MENU, 'subtitle': "Please select an action...",
	'options':[
  		{ 'title': "Yes", 'type': COMMAND, 'command': 'exit_program()' },
  ]#end of exit_menu options
}#end of exit_menu data
