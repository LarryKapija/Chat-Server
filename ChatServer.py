import socket as sk
import logging as log
import stringcase as sc
import Commands as cmd
import sys
import threading




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

console_arguments = sys.argv
port , verbose = args(console_arguments)

print(f'{port} ->{verbose}')

def verbose_function(debug_message,bool_value):
	if bool_value == True:
		print(debug_message)
			
log.basicConfig(filename='server.log',level=log.DEBUG,filemode='a')
my_socket = sk.socket()
my_socket.bind(('localhost',port))
my_socket.listen(16)
	
def switch(argument):
	switcher = { 
		"/ID": cmd.id,
		"/USERLIST": cmd.userlist,
		"/CHAT": cmd.chat,
		"/CLOSE": cmd.close,
		"/CHATLIST": cmd.chatlist,
		"/ROOM": cmd.room,
		"/QUIT": cmd.quit, 
		"/JOIN": cmd.join,
		"/ADD": cmd.add,
		"/REJECT": cmd.reject, 
		"/REQUESTLIST": cmd.requestlist,
		"/ROOMLIST": cmd.roomlist,
		"/INVITELIST": cmd.invitelist,

	}
	func = switcher.get(argument, "Invalid command")
	return func

def main():
	while True:
		try:
			connection, address = my_socket.accept()
			print("New connection stablished!",end=" ")
			print(address)

			log.info(f"New connection stablished! {address}")

			thread = threading.Thread(target=handle, args=(connection,))
			verbose_function(f'\nNew thread stablished args = {connection}\n',verbose)
			thread.start()

		except Exception as e :
			message = f"ERROR {e}"
			print(message)
			connection.send(message.encode("ascii"))
			connection.close()


def handle(connection):
	with connection:
		client_message = ''
  
		while True:
			petition = connection.recv(1024)
			verbose_function(f'\nNew client petition {petition}\n',verbose)
   
			if petition:
				client_message += petition.decode('utf-8')
				client_message = client_message.replace('\r', '')
				verbose_function(f'\nClient message decode {client_message}\n',verbose)
    
				if not client_message.endswith('\n'):
					continue
				else:
					client_message = client_message.replace("\n", "")
					client_message = client_message.split(" ")
					function = switch(client_message[0])
					verbose_function(f'\nFunction that the server will use: {function}\n',verbose)
     
					if isinstance(function, str):
						connection.send(function.encode("ascii"))
						verbose_function(f'\nMessage : {function.encode("ascii")}\n',verbose)
						continue

					server_message = function(client_message[1:],connection)
					if connection._closed:
						break
					
					connection.send(server_message.encode('ascii'))
					verbose_function(f'\nMessage to the client: {server_message}\n',verbose)
	 
					client_message= ''
					server_message= ''
					
if __name__ == "__main__":
	main()