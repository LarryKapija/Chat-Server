import socket as sk
import logging as log
import Commands as cmd

log.basicConfig(filename='server.log',level=log.DEBUG,filemode='a')
my_socket = sk.socket()
my_socket.bind(('localhost',5000))
my_socket.listen(16)


# users["username"] = address 

def switch(argument):
	switcher = {
		"/ID": cmd.Id,
		"/USERLIST": cmd.userlist,
		"/CHAT": cmd.chat,
		"/CLOSE": cmd.close,
		"/CHATLIST": cmd.chatlist
	}
	func = switcher.get(argument, "Invalid command")
	return func

while True:
	try:
		connection, address = my_socket.accept()
		print("New connection established!",end=" ")
		print(address)

		log.info(f"New connection established!{address}")
		petition = connection.recv(4096)
		petition = str(petition, encoding = "ascii")
		petition = petition.split(" ")

		function = switch(petition[0])
		message = function(petition[1:], address)
		
		connection.send(message.encode("ascii"))
		connection.close()

	except Exception as e:
		message = f"Hubo un error {e}"
		print(message)
		connection.send(message.encode("ascii"))
		connection.close()

