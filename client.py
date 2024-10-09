import requests, json

GET = 0
PUT = 1
POST = 2

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
        url = "http://localhost:" + port_user + "/user/create_user"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": "usuario" + str(command.split(' ')[1]),
            "password": "1234"
        }
        method = POST
    elif (command.split(' ')[0].upper() == "CREATEFILE"):
        url = "http://localhost:" + port_file + "/file/create_file"
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
        url = "http://localhost:" + port_file + "/file/delete_file"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[2])
        }
        data = {
            "uid": str(command.split(' ')[3]), 
            "filename": "nombre_archivo" + str(command.split(' ')[1]) + ".txt",
            "content": "Este campo se puede ignorar para la eliminación."
        }
        method = POST
    elif (command.split(' ')[0].upper() == "LISTFILE"):
        url = "http://localhost:5000/file/list_file"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + str(command.split(' ')[2])
        }
        data = {
            "uid": str(command.split(' ')[3])
        }
        method = GET
    
    if (method == POST):
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif (method == GET):
        response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text + " --- " + str(response.status_code))
    print()
