import socket as sk 
import threading 

mi_socket = sk.socket()
mi_socket.connect(('localhost', 6000))

def receive():
	while True:
		try:
			
			respuesta = mi_socket.recv(1024).decode("ascii")
			if len(respuesta)!=0:   
				if '/CHAT' in respuesta:
					respuesta = respuesta.split(" ")
					message = " ".join(respuesta[4:])
					print(f"{respuesta[2]} : {message}")
				else:
					print(f"\nServer response: {respuesta}")   

			else:
				continue
			
		except Exception as e :
				print(f"{e}")
				mi_socket.close()
				break
def write():
	while True:
		mensaje = str(input(': '))
		mi_socket.send(mensaje.encode("ascii"))  
		break

def main():
	receive_thread = threading.Thread(target=receive)
	receive_thread.start()
	
	write_thread = threading.Thread(target=write)
	write_thread.start()

if __name__=="__main__":
	main()