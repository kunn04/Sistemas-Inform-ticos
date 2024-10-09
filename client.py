import requests, json

GET = 0
PUT = 1
POST = 2
DEL = 3

port_user = "5080"
port_file = "5090"

users = 0
method = POST #default

while True:
    command = str(input())

    print(command.split(' ')[0])

    if (command.split(' ')[0].upper() == "LOGIN"):
        url = "http://localhost:" + port_user + "/user/login"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": "usuario" + str(command.split(' ')[1]),
            "password": "1234"
        }
        method = POST
    elif (command.split(' ')[0].upper() == "CREATE"):
        url = "http://localhost:" + port_user + "/user/create"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": "usuario" + str(command.split(' ')[1]),
            "password": "1234"
        }
        method = POST
    elif (command.split(' ')[0].upper() == "CREATEFILE"):
        url = "http://localhost:" + port_file + "/file/create"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[2])  
        }
        data = {
            "uid": str(command.split(' ')[3]),
            "filename": "nombre_archivo" + str(command.split(' ')[1]) + ".txt",
            "content": "Este es el contenido del archivo."
        }
        method = POST
    elif (command.split(' ')[0].upper() == "DELETEFILE"):
        url = "http://localhost:" + port_file + "/file/delete"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[2])
        }
        data = {
            "uid": str(command.split(' ')[3]), 
            "filename": "nombre_archivo" + str(command.split(' ')[1]) + ".txt",
            "content": "Este campo se puede ignorar para la eliminación."
        }
        method = DEL
    elif (command.split(' ')[0].upper() == "LISTFILE"):
        url = "http://localhost:" + port_file + "/file/list"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[1])
        }
        data = {
            "uid": str(command.split(' ')[2])
        }
        method = GET
    elif (command.split(' ')[0].upper() == "READFILE"):
        url = "http://localhost:" + port_file + "/file/read"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[2])
        }
        data = {
            "uid": str(command.split(' ')[3]),
            "filename": "nombre_archivo" + str(command.split(' ')[1]) + ".txt",
        }
        method = GET
    elif (command.split(' ')[0].upper() == "DELETEUSER"):
        url = "http://localhost:" + port_user + "/user/delete"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre" : "usuario" + str(command.split(' ')[1]),
            "password" : "1234"
        }
        method = DEL
    elif (command.split(' ')[0].upper() == "MODUSER"):
        url = "http://localhost:" + port_user + "/user/modify"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre" : "usuario" + str(command.split(' ')[1]),
            "password_old" : "1234",
            "password_new" : "4321"
        }
        method = POST
    elif (command.split(' ')[0].upper() == "MODFILE"):
        url = "http://localhost:" + port_file + "/file/modify"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[2])
        }
        data = {
            "uid": str(command.split(' ')[3]),
            "filename": "nombre_archivo" + str(command.split(' ')[1]) + ".txt",
            "content": "Este es el nuevo contenido añadido del fichero."
        }
        method = POST
    else:
        url = None
        print('No se ha especificado ningun comando')
    
    if (url is not None):
        if (method == POST):
            response = requests.post(url, headers=headers, data=json.dumps(data))
        elif (method == GET):
            response = requests.get(url, headers=headers, data=json.dumps(data))
        elif (method == DEL):
            response = requests.delete(url, headers=headers, json=data)

        print(response.text + " --- " + str(response.status_code))
        print()
