import socket as sk

mi_socket = sk.socket()
mi_socket.bind(('localhost',5000))
mi_socket.listen(5)

while True:
	try:
		conexion, direccion = mi_socket.accept()
		print("Nueva conexion establecida!",end=" ")
		print(direccion)

		peticion = conexion.recv(1024)
		peticion = str(peticion)
		
		if "hola" in peticion.lower() :
			mensaje = "Hi"
		elif "Como estas" in peticion:
			mensaje = "Bien y tu?"
		else:
			mensaje = "Pase buenas noches joven"

		conexion.send(mensaje.encode("ascii"))
		conexion.close()

	except Exception as e:
		mensaje = f"Hubo un error {e}"
		conexion.send(mensaje.encode("ascii"))
		conexion.close()