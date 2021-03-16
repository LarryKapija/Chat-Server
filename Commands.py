import stringcase as sc
from ChatServer import verbose_function
from ChatServer import verbose

users = {}


def id(username, connection):
	username = str(''.join(username))

	if len(users) == 16:
		verbose_function(f'\n{connection} tried to enter the chat, but it is already full\n',verbose)
		return "Full"

	elif sc.pascalcase(username) != username:
		verbose_function(f'\n{connection} tried to enter the chat, but the username "{username}" is not valid\n',verbose)
		return "NotValid"

	elif username in users:
		verbose_function(f'\n{connection} tried to enter the chat, but the username "{username}" is already taked\n',verbose)
		return "Taken"

	else:
		users[username] = connection
		verbose_function(f'\n{connection} joined the conversation with the username "{username}\n',verbose)
		#broadcast(f"{username} joined the conversation!")
		#connection.send()
		#print(users)
		return "Ok"

def broadcast(message, userslist =''):
	if len(userlist) == 0:
		for value in users:
			if value in userslist:
				users[value].send(message.encode('ascii'))
	else:
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