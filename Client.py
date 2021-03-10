import socket as sk 

mi_socket = sk.socket()
mi_socket.connect(('localhost', 6000))

while True:
    try:
        mensaje = str(input('Inserte un su mensaje: '))

        mi_socket.send(mensaje.encode("ascii"))
        respuesta = mi_socket.recv(4096) 

        print("\nUsted tiene un mensaje del servidor:",end=" ")

        respuesta = str(respuesta,encoding="ascii")
        print(respuesta)
        continue
        
    except Exception:
        mi_socket.close()