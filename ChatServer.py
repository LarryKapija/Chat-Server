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
			message = f"ERROR {e}"
			print(message)
			connection.send(message.encode("ascii"))
			connection.close()


def handle(connection):

	with connection:
		client_message = ''
		while True:
			petition = connection.recv(1024)
			if petition:
				client_message += petition.decode('utf-8')
				if petition.decode('utf-8') == '\r\n' or petition.decode('utf-8').endswith('\r\n'):
					continue
				else:
					client_message = client_message.split(" ")
					function = switch(client_message[0])
     
					server_message = function(client_message[1:],connection)
					connection.send(server_message.encode('ascii'))
     
					client_message= ''
					server_message= ''

if __name__ == "__main__":
	main()