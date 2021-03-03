import stringcase as sc

users = {'miguelc':('localhost',500)}

def Id(username,address):
    username = str(''.join(username))
    
    if len(users) == 16:
        return "FULL"
    
    elif sc.pascalcase(username) != username:
        return "INVALID NAME"
    
    elif username in users:
        return "TAKEN"
    
    else :
        users[username]=address
        print(users)
        return "OK"
    
def userlist(a,k):
	mylist =[]
	if len(users) == 0:
            return "Empty"
	else:
		for key in users.keys():
			mylist.append(key)
		return str(mylist)

def chat():
	return "CHAT"

def close():
	return "CLOSE"
def chatlist():
	return "CHATLIST"
