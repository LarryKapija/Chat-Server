import stringcase as sc

users = {}


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
        # broadcast(f"{username} joined!")
        #connection.send()
        #print(users)
		return "Ok"


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
			return "OK"
		else:
			return "NOTFOUND"

	except Exception as e :
		print(e)
		return "ERROR"

def broadcast(message):
	for key,value in users:
		value.send(message.encode("ascii"))

def close(client,connection):
	try:
		for key in users.keys():
			if users[key] == connection:
				users.pop(key)

		connection.close()
		return "Ok"
	except Exception :
		return "Error"
    
def chatlist():
	return "CHATLIST"