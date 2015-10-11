class Dictionary:
	MENU = "menu"
	COMMAND = "command"
	EXITMENU = "exitmenu"


main_menu = {
	'title': "Main Menu", 'type': Dictionary.MENU, 'subtitle': "Please select an option...",
	'options':[
  		{ 'title': "Use MySQL databases", 'type': Dictionary.COMMAND, 'command': 'use_mysql()' },
    	{ 'title': "Use PostgreSQL databases", 'type': Dictionary.COMMAND, 'command': 'use_psql()' },
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
  		{ 'title': "Yes", 'type': Dictionary.COMMAND, 'command': 'exit_program()' },
  ]#end of exit_menu options
}#end of exit_menu data

