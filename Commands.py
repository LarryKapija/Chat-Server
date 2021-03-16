import stringcase as sc
import Models

users = {}
groups = {}
invitations = {}

def id(username, connection):
	username = str(''.join(username))

	if len(users) == 16:
		return "Full"

	elif sc.pascalcase(username) != username:
		return "NotValid"

	elif username in users:
		return "Taken"

	else:
		users[username] = connection
		invitations[username] = []
		#broadcast(f"{username} joined the conversation!")
		#connection.send()
		#print(users)
		return "Ok"
def broadcast(message):
	for value in users:
		users[value].send(message.encode("ascii"))

def userlist(a=None, b=None):
	mylist = []
	if len(users) == 0:
		return "Empty"
	else:
		for key in users.keys():
			mylist.append(key)
		return str(mylist)


def chat(args, connection):

	username = args[1]
	key_list = list(users.keys())
	value_list = list(users.values())
	try:
		if username in users:
			position = value_list.index(connection)
			message = str(' '.join(args)).replace(username, key_list[position])
			message = "/CHAT " + message
			users[username].send(message.encode("ascii"))
			return "Ok"
		else:
			return "NotFound"

	except Exception as e :
		print(e)
		return "Error"



def close(client,connection):
	try:
		for key in users.keys():
			if users[key] == connection:
				users.pop(key)
				connection.send('Ok'.encode('ascii'))
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
    if username in groups[roomname].members:
      return "Already"
    if username in invitations:
      if roomname in invitations[username]:
        for member in groups[roomname].members:
          message = "/ROOMJOIN" + username + " joined " + roomname
          users[member].send(message.encode("ascii"))
        groups[roomname].members.append(username)
        groups[roomname].invitations.remove(username)
        invitations[username].remove(roomname)
    else:
      if not username in groups[roomname].requests:
        groups[roomname].requests.append(username)
      owner = groups[roomname].owner
      message = "/ROOMJOIN" + username + " request-to-join " + roomname
      users[owner].send(message.encode("ascii"))

    
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
    if username != groups[roomname].owner:
      return "NoOwner"
    
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
  return "Ok"

def getUser(connection):
	for key in users.keys():
		if users[key] == connection:
			return key

def room(args,connection):
	try:
		roomname = args[0]
		if roomname in groups:
			return "Taken"
		
		owner =  getUser(connection)
		groups[roomname] = Models.Groups(roomname,owner)
		return 'Ok'

	except Exception as e:
		return f"Error{e}"

# def RoomExist(room_name):


def IsOwner(room_name, connection):
	user = getUser(connection)
	room = groups[room_name]
	if (user == room.owner):
		return True
	else:
		return False

def add(args, connection):
	try:	
		user = getUser(connection)
		
		if (args[0] == '-f'):
			roomname = args[1]
			newmemebers = args[2:]

			#TODO check grupo existe 
			#

			room = groups[roomname]
			if (IsOwner(roomname, connection)):
				for member in newmemebers:
					#TODO check existe usuario

					#TODO eliminar requests
					for req in room.requests:
						if member == req:
							room.requests.remove(member)

					#TODO eliminar invitaciones
					for group in invitations[member]:
						if roomname == group :
							invitations[member].remove(roomname)

					#TODO add memeber 
					groups[roomname].members.append(member)
					return "Ok"

		else:
			roomname = args[0]
			newmemebers = args[1:]
			#TODO check grupo existe 
			#
			if (IsOwner(roomname, connection)):
				for member in newmemebers:
					#TODO check existe ususario

					#TODO eliminar request si hay y agregar al grupo
					if member in groups[roomname].requests:
						groups[roomname].requests.remove(member)
						groups[roomname].members.append(member)
						return "Ok"

					#TODO enviar invitacion si no tiene
					if roomname not in invitations[member]:
						invitations[member].append(roomname)
						return "Ok"

	except Exception as e:
		return f"Error{e}"



def quit():
	return "null"
def reject():
	return "null"

def invitelist():
	return "null"
