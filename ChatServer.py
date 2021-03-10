import socket as sk
import logging as log
import stringcase as sc
import Commands as cmd
import threading

log.basicConfig(filename='server.log',level=log.DEBUG,filemode='a')
my_socket = sk.socket()
my_socket.bind(('localhost',6000))
my_socket.listen(16)


def switch(argument):
	switcher = {
		"/ID": cmd.id,
		"/USERLIST": cmd.userlist,
		"/CHAT": cmd.chat,
		"/CLOSE": cmd.close,
		"/CHATLIST": cmd.chatlist
	}
	func = switcher.get(argument, "Invalid command")
	return func

def main():
	while True:
		try:
			connection, address = my_socket.accept()
			print("New connection established!",end=" ")
			print(address)

			log.info(f"New connection established!{address}")

			thread = threading.Thread(target=handle, args=(connection,))
			thread.start()

		except Exception as e:
			message = f"Hubo un error {e}"
			print(message)
			connection.send(message.encode("ascii"))
			connection.close()
   

def handle(connection):
	while True:
		try:
			petition = connection.recv(4096)
			petition = str(petition, encoding = "ascii")
			petition = petition.split(" ")

			function = switch(petition[0])
			message = function(petition[1:], connection)
			connection.send(message.encode("ascii"))
		except:
			connection.close()
	
if __name__ == "__main__":
    main()