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