import sys
def args(console_arguments):
	x=0
	port=5000
	verbose = False
	
	for argument in console_arguments:
		try:
			if argument == '-p' or argument == '--port':
				port = int(console_arguments[x+1])
	
			elif argument == '-v' or argument == '--verbose' :
				verbose = True
		except:
				port=5000
				verbose = False
		x+=1
  
	if port < 0 or port > 65535 :
		port = 5000
  
	return port,verbose

def verbose_function(debug_message,bool_value):
	if bool_value == True:
		print(debug_message)

console_arguments = sys.argv
port, verbose = args(console_arguments)