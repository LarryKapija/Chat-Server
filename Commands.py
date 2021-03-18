import stringcase as sc
#from ChatServer import verbose_function
#from ChatServer import verbose
#from Verbose import verbose_function
#from Verbose import verbose
import Models

users = {}
groups = {}
invitations = {}

def id(username, connection):
	username = str(''.join(username))

	if len(users) == 16:
		#verbose_function(f'\n{connection} tried to enter the chat, but it is already full\n',verbose)
		return "Full"

	elif sc.pascalcase(username) != username:
		#verbose_function(f'\n{connection} tried to enter the chat, but the username "{username}" is not valid\n',verbose)
		return "NotValid"

	elif username in users:
		#verbose_function(f'\n{connection} tried to enter the chat, but the username "{username}" is already taked\n',verbose)
		return "Taken"

	else:
		users[username] = connection
		#verbose_function(f'\n{connection} joined the conversation with the username "{username}\n',verbose)
		invitations[username] = []
		#broadcast(f"{username} joined the conversation!")
		#connection.send()
		#print(users)
		return "Ok"

def broadcast(message, userslist =''):
	if userslist != '':
		for value in users:
			if value in userslist:
				users[value].send(f'{message}\n'.encode('ascii'))
	else:
		for value in users:
			users[value].send(f'{message}\n'.encode("ascii"))

def userlist(a=None, b=None):
	mylist = []
	if len(users) == 0:
		return "Empty"
	else:
		for key in users.keys():
			mylist.append(key)
		return str(mylist)


def chat(args, connection):

	#username = args[1]
	key_list = list(users.keys())
	value_list = list(users.values())
	
	try:
		if args[0] == '-u' :
			username = args[1]
	
			if username in users:
				position = value_list.index(connection)
				message = str(' '.join(args)).replace(username, key_list[position]).replace("-u ", "").replace("-m ", "")
				message = f'/MESSAGE {message}'
				users[username].send(f'{message}\n'.encode("ascii"))
				return "Ok"
			else:
				return "NotFound"
		
		elif args[0] == '-g':
			roomname = args[1]

			if roomname in groups.keys():
				room = groups[roomname]
				position = value_list.index(connection)
				message = str(' '.join(args)).replace("-g ", "").replace("-m ", "")
				message = "/MESSAGE " + message.replace(roomname, f"{roomname}_{key_list[position]}")
	
				broadcast(message,list(room.members))
				return "Ok"
			else:
				return 'NotFound'
		else:
			position = value_list.index(connection)
			message = "/MESSAGE " + f'{key_list[position]} ' + ' '.join(args).replace("-m ", "")
			broadcast(message,'')
			return 'Ok'
			

	except Exception as e :
		print(e)
		return "Error" 


def close(client,connection):
	try:
		for userkey in users.keys():
			if users[userkey] == connection:
				
				for room in groups.values():
					if userkey in room.members:
						quit(room.room_name,connection)

				invitations.pop(userkey)
				users.pop(userkey)

				connection.send('Ok\n'.encode('ascii'))
				connection.close()
				break
			
	except Exception as e:
		return f"Error{e}"
	
def chatlist():
	return "CHATLIST"

def join(args, connection):
	try:
		roomname = args[0]
		position = list(users.values()).index(connection)
		username = list(users.keys())[position]

		if not roomname in groups.keys():
			return "NotFound"
		
		elif username in groups[roomname].members:
			return "Already"

		elif roomname in invitations[username]:
      
			for member in groups[roomname].members:
				message = "/ROOMJOIN " + username + " joined " + roomname
				users[member].send(f'{message}\n'.encode("ascii"))
    
			groups[roomname].members.append(username)
			# groups[roomname].invitations.remove(username)
			invitations[username].remove(roomname)
		else:
			if not username in groups[roomname].requests:
				groups[roomname].requests.append(username)
				owner = groups[roomname].owner
				message = "/ROOMJOIN " + username + " request-to-join " + roomname
				users[owner].send(f'{message}\n'.encode("ascii"))

			return "Ok"

	except Exception as e:
		print(e)
		return "Error"

def requestlist(args, connection):
	try:
		roomname = args[0]
		position = list(users.values()).index(connection)
		username = list(users.keys())[position]

		if not roomname in groups.keys():
			return "NotFound"

		elif username != groups[roomname].owner:
			return "NoOwner"
		
		else:
			return str(groups[roomname].requests)

	except Exception as e:
		print(e)
		return "Error"

def roomlist(client, connection):
	try:
		return str(list(groups.keys()))

	except Exception as e:
		print(e)
		return "Error"
	#return "Ok"

def getUser(connection):
	for key in users.keys():
		if users[key] == connection:
			return key

def room(args,connection):
	try:
		roomname = args[0]
		if roomname in groups:
			return "Taken"
		
		owner =	getUser(connection)
		groups[roomname] = Models.Groups(roomname,owner)
		return 'Ok'

	except Exception as e:
		print(e)
		return "Error"

# def RoomExist(room_name):


def IsNotOwner(room_name, connection):
	user = getUser(connection)
	room = groups[room_name]
 
	if (user == room.owner):
		return False
	else:
		return True

def add(args, connection):
	try:	
		if (args[0] == '-f'):
			roomname = args[1]
			newmembers = args[2:]

			#TODO check grupo existe
			if(roomname not in groups):
				return "RoomNotFound"

			room = groups[roomname]
			if (IsNotOwner(roomname, connection)):
				return "Error"

			for member in newmembers:
				#TODO check existe usuario
				if member not in users:
					return "UserNotFound"

				#TODO eliminar requests
				for req in room.requests:
					if member == req:
						room.requests.remove(member)

				#TODO eliminar invitaciones
				for group in invitations[member]:
					if roomname == group :
						invitations[member].remove(roomname)

				#TODO add memeber
				msg = '/ADDED ' + roomname
				users[member].send(msg.encode('ascii'))
				groups[roomname].members.append(member)
				return "Ok"


		else:
			roomname = args[0]
			newmembers = args[1:]
			#TODO check grupo existe 
			if roomname not in groups :
				return "RoomNotFound"

			#TODO check es owner
			if IsNotOwner(roomname, connection):
				return "Error"

			for member in newmembers:

				#TODO check existe ususario
				if(member not in users):
					return "UserNotFound"

				#TODO eliminar request si hay y agregar al grupo
				if member in groups[roomname].requests:
					groups[roomname].requests.remove(member)
					groups[roomname].members.append(member)
					return "Ok"

				#TODO enviar invitacion si no tiene
				if roomname not in invitations[member]:
					mdg = '/INVITED ' + roomname
					users[member].send(msg.encode('ascii'))
					invitations[member].append(roomname)
					return "Ok"


	except Exception as e:
		return f"Error{e}"



def quit(args, connection):
	try:
		roomname = args[0]
		room = groups[roomname]
		
		user = getUser(connection)
		if user not in room.members:
			return "NotInRoom"

		if room.owner == user:
			message = f"/ROOMQUIT {user} deleted {roomname}"
			broadcast(message, room.members)

			for user_invitations in invitations:
				if roomname in user_invitations:
					user_invitations.remove(roomname)
	 
			for member in room.members:
				users[member].send(message)
	
			groups.pop(roomname)
			return "Ok"

		elif room.owner != user:
			message = f"/ROOMQUIT {user} left {roomname}"

			index = room.members.index(user)
			room.members.pop(index)
   
			broadcast(message,room.members)
	except :
		return "Error"


def reject(args, connection):
	try:
		user = getUser(connection)
		roomname = args[0]
		room = groups[roomname]
		invitations[user].remove(roomname)
		room.invitations.remove(user)
		owner = room.owner
		message = f"/ROOMREJECT {user} reject"
		users[owner].send(message.encode("ascii"))
		return "Ok"
	except :
		return "Error"

def invitelist(args,connection):
	try:
		user = getUser(connection)
		user_invitations = invitations[user]
		#print(user_invitations)
		return str(user_invitations)
	except Exception as e :
		print(e)
		return "Error"
