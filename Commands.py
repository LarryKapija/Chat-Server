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
    message = str(''.join(args[2:]))
    try:
        if username in users:
            users[username].send(message)
            return "Ok"
        else:
            return "NotFound"
            
    except Exception :
        return "Error"

def broadcast(message):
    for key,value in users:
        value.send(message.encode("ascii"))
        
def close(client):
    username =""
    users.pop(username)
    return "Ok"


def chatlist():
    return "CHATLIST"