import stringcase as sc

users = {}


def Id(username, connection):
    username = str(''.join(username))

    if len(users) == 16:
        return "FULL"

    elif sc.pascalcase(username) != username:
        return "INVALID NAME"

    elif username in users:
        return "TAKEN"

    else:
        users[username] = connection
        print(users)
        return "OK"


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
            return "OK"
        else:
            return "NOTFOUND"
            
    except Exception :
        return "ERROR"


def close():
    return "CLOSE"


def chatlist():
    return "CHATLIST"
