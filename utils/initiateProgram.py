import curses
import MySQLdb
import psycopg2
import os
import subprocess
import sys
import time

<<<<<<< HEAD
=======

>>>>>>> origin/menu-test-nj
#ANSI escape sequence colors for changing text color without using curses
#source: stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
class terminalColors:
	SUCCESS = '\33[1m\33[32m'
	FAIL = '\33[1m\33[31m'
	ENDC = '\33[0m'

<<<<<<< HEAD
class initiateProgram(object):

	#Checks if applications are/or installed and are of correct version.
	#Sources used:
	#stackoverflow.com/questions/5847934/how-to-check-if-python-module-exists-and-can-be-imported
	#stackoverflow.com/questions/710609/checking-a-python-module-version-at-runtime
	#stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7
	def versionCheck(self):
		stop = 0 #Used to determine if there was a failure, if so halt program.
		#Check to see if required programs are and installed and have correct version.
		check_these_programs = [["python", "mysql", "psql"], ["2.7", "14", "9"]]
	
		for i in range(0, len(check_these_programs[0])):
			j = 1 #used for indexing in 2-D array
		
			#Used to redirect output from subprocess to devnull (don't want it printed to screen), closes after subprocess finishes.
			fnull = open(os.devnull, 'w')
			try:
				subprocess.call([check_these_programs[0][i], "--version"], stdout = fnull, 
																		   stderr=subprocess.STDOUT,
																		   close_fds=True)
			except:#Means program is not installed
				stop = 1 #Failure do not continue with program
				result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
				print check_these_programs[0][i] + " version " + check_these_programs[j][i] + " - " + result
				continue #Skip to next iteration
			else:#Program is installed now need to check versions
				if check_these_programs[0][i] == "python":
					major = sys.version_info.major
					minor = sys.version_info.minor
					if major == 2 and minor == 7:
						result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
					else:
						result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
						stop = 1 #Failure do not continue with program
			
				elif check_these_programs[0][i] == "psql":
					proc = subprocess.Popen(["psql", "--version"], stdout=subprocess.PIPE)
					ver = proc.communicate()[0]
				
					#parse output of psql --version to get major version number
					ver = ver.split(" ",4)
					ver = ver[2].split(".", 1)
					ver = ver[0]
				
					if ver == check_these_programs[1][2]:
						result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
					else:
						result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
						stop = 1 #Failure do not continue with program

				elif check_these_programs[0][i] == "mysql":
					proc = subprocess.Popen(["mysql", "--version"], stdout=subprocess.PIPE)
					ver = proc.communicate()[0]
				
					#parse output of psql --version to get major version number
					ver = ver.split(" ",3)
					ver = ver[3].split(".", 1)
					ver = ver[0]
				
					if ver == check_these_programs[1][1]:
						result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
					else:
						result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
						stop = 1 #Failure do not continue with program


			print check_these_programs[0][i] + " version " + check_these_programs[j][i] + ".* - " + result
			time.sleep(0.5)

		#Check python modules
		check_these_modules = [["curses", "MySQLdb", "psycopg2"],["2.2", "1.2.3", "2.5.3 (dt dec mx pq3 ext)"]]
		for i in range(0, len(check_these_modules[0])):
			j = 1 #used for indexing in 2-D array

			try:
				__import__(check_these_modules[0][i]) #Checking modules are installed.
			except ImportError:
				stop = 1 #Failure do not continue with program
				result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
				print check_these_modules[0][i] + " version " + check_these_modules[j][i] + " - " + result
				continue #Skip to next iteration
			else:#Is installed, but need to check for correct version.
				if check_these_modules[0][i] == "curses":#curses uses different syntax to check for version
					ver = curses.version
				else:
					ver = eval(check_these_modules[0][i] + '.__version__')

				if check_these_modules[j][i] == ver:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program

				print check_these_modules[0][i] + " version " + check_these_modules[j][i] + " - " + result
				time.sleep(0.5)
		
			j += 1

	
		if stop == 1:
			print terminalColors.FAIL + "ALERT" + terminalColors.ENDC
			print "One or more items is either not installed or is the incorrect version"
			print "Now exiting"
		else:
			print "Thank you for your patience, now opening program..."

		time.sleep(5)

		return(stop)
	#end versionCheck()
=======
#Checks if applications are/or installed and are of correct version.
#Sources used:
#stackoverflow.com/questions/5847934/how-to-check-if-python-module-exists-and-can-be-imported
#stackoverflow.com/questions/710609/checking-a-python-module-version-at-runtime
#stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7
def versionCheck():
	stop = 0 #Used to determine if there was a failure, if so halt program.

	#Check to see if required programs are and installed and have correct version.
	check_these_programs = [["python", "mysql", "psql"], ["2.7", "14", "9"]]
	
	for i in range(0, len(check_these_programs[0])):
		j = 1 #used for indexing in 2-D array
		
		#Used to redirect output from subprocess to devnull (don't want it printed to screen), closes after subprocess 			 finishes.
		fnull = open(os.devnull, 'w')
		try:
			subprocess.call([check_these_programs[0][i], "--version"], stdout = fnull, 
																	   stderr=subprocess.STDOUT,
																	   close_fds=True)
		except:#Means program is not installed
			stop = 1 #Failure do not continue with program
			result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
			print check_these_programs[0][i] + " version " + check_these_programs[j][i] + " - " + result
			continue #Skip to next iteration
		else:#Program is installed now need to check versions
			if check_these_programs[0][i] == "python":
				major = sys.version_info.major
				minor = sys.version_info.minor
				if major == 2 and minor == 7:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program
			
			elif check_these_programs[0][i] == "psql":
				proc = subprocess.Popen(["psql", "--version"], stdout=subprocess.PIPE)
				ver = proc.communicate()[0]
				
				#parse output of psql --version to get major version number
				ver = ver.split(" ",4)
				ver = ver[2].split(".", 1)
				ver = ver[0]
				
				if ver == check_these_programs[1][2]:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program

			elif check_these_programs[0][i] == "mysql":
				proc = subprocess.Popen(["mysql", "--version"], stdout=subprocess.PIPE)
				ver = proc.communicate()[0]
				
				#parse output of psql --version to get major version number
				ver = ver.split(" ",3)
				ver = ver[3].split(".", 1)
				ver = ver[0]
				
				if ver == check_these_programs[1][1]:
					result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
				else:
					result = terminalColors.FAIL + "FAILED wrong version" + terminalColors.ENDC
					stop = 1 #Failure do not continue with program


		print check_these_programs[0][i] + " version " + check_these_programs[j][i] + ".* - " + result
		time.sleep(0.5)

	#Check python modules
	check_these_modules = [["curses", "MySQLdb", "psycopg2"],["2.2", "1.2.3", "2.5.3 (dt dec mx pq3 ext)"]]
	for i in range(0, len(check_these_modules[0])):
		j = 1 #used for indexing in 2-D array

		try:
			__import__(check_these_modules[0][i]) #Checking modules are installed.
		except ImportError:
			stop = 1 #Failure do not continue with program
			result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
			print check_these_modules[0][i] + " version " + check_these_modules[j][i] + " - " + result
			continue #Skip to next iteration
		else:#Is installed, but need to check for correct version.
			if check_these_modules[0][i] == "curses":#curses uses different syntax to check for version
				ver = curses.version
			else:
				ver = eval(check_these_modules[0][i] + '.__version__')

			if check_these_modules[j][i] == ver:
				result = terminalColors.SUCCESS + "SUCCESS" + terminalColors.ENDC
			else:
				result = terminalColors.FAIL + "FAILED" + terminalColors.ENDC
				stop = 1 #Failure do not continue with program

			print check_these_modules[0][i] + " version " + check_these_modules[j][i] + " - " + result
			time.sleep(0.5)
		
		j += 1

	
	if stop == 1:
		print terminalColors.FAIL + "ALERT" + terminalColors.ENDC
		print "One or more items is either not installed or is the incorrect version"
		print "Now exiting"
	else:
		print "Thank you for your patience, now opening program..."

	time.sleep(5)

	return(stop)
#end versionCheck()
>>>>>>> origin/menu-test-nj
