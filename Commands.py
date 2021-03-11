import stringcase as sc
import logging as log

log.basicConfig(filename='server.log', level=log.DEBUG, filemode="a")
users = {}

def id(username, connection):
    username = str(''.join(username))
    
    #check full
    if len(users) == 16:
        return 'Full'
    #check pascalcase
    elif sc.pascalcase(username) != username:
        return 'NotValid'
    #check if taken
    elif username in users:
        return 'Taken'
    #check in?
    else:
        users[username]=connection
        return 'Ok'

def userlist(a=None, b=None):
    mylist=[]
    if len(users)== 0:
        return "Empty"
    else:
        for key in users.keys():
            mylist.append(key)
        return str(mylist)

def chat(args, connection):
    username = args[1]
    key_list = list(users.keys())
    values_list = list(users.values())
    try:
        if username in users:
            position = values_list.index(connection)
            message = str(' '.join(args)).replace(username, key_list[position])
            message = '/CHAT ' + message
            users[username].send(message.encode('ascii'))
            return "Ok"
        else:
            return "NotFound"
    except Exception as e:
        print(e)
        log.error(e)
        return 'Error'

def close(client, connection):
    try:
        for key in users.keys():
            if users[key] == connection:
                users.pop(key)
                connection.send('Ok'.encode('ascii'))
                connection.close()
                break
    except Exception as e:
        log.error(e)
        return f'Error{e}'

def chatlist():
    return 'HI'