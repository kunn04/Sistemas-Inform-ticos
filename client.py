import requests, json

GET = 0
POST = 1
DELETE = 2

url = ""
headers = {}
data = {}

port_user = '5080'
port_file = '5090'
uid = ''
token = ''

def execute(method):
    global url, headers, data, uid, token

    if (method == POST):
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif (method == GET):
        response = requests.get(url, headers=headers, data=json.dumps(data))
    elif (method == DELETE):
        response = requests.delete(url, headers=headers, json=data)

    print("Respuesta:\n" + "\033[92m" + response.text + "\033[0m" + "\n--- Codigo de salida: " + str(response.status_code), end='\n\n')

    if token == '' and response.text.split(':')[0] == "uid":
        token = response.text.split('\n')[1].split(' ')[1]
        uid = response.text.split('\n')[0].split(' ')[1]

    return

#Creación de un usuario ejemplo
url = "http://localhost:" + port_user + "/user/create"
headers = {"Content-Type": "application/json"}
data = {
    "nombre": "usuario_ejemplo",
    "password": "1234"
}

print("Creación de un usuario ejemplo (user:'usuario_ejemplo', password:'1234'):")
execute(POST)



#Login de usuario
url = "http://localhost:" + port_user + "/user/login"
headers = {"Content-Type": "application/json"}
data = {
    "nombre": "usuario_ejemplo",
    "password": "1234"
}

print("Login del usuario ejemplo (user:'usuario_ejemplo', password:'1234'):")
execute(POST)

#Cambio de contraseña de un usuario
url = "http://localhost:" + port_user + "/user/modify"
headers = {"Content-Type": "application/json"}
data = {
    "nombre" : "usuario_ejemplo",
    "password_old" : "1234",
    "password_new" : "4321"
}

print("Cambio de contraseña de 'usuario_ejemplo' de '1234' a '4321':")
execute(POST)


#Login de usuario
url = "http://localhost:" + port_user + "/user/login"
headers = {"Content-Type": "application/json"}
data = {
    "nombre": "usuario_ejemplo",
    "password": "4321"
}

print("Login del usuario ejemplo con la nueva contraseña (user:'usuario_ejemplo', password:'4321'):")
execute(POST)


#Listado de ficheros del usuario
url = "http://localhost:" + port_file + "/file/list"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid
}

print("Listado de ficheros existentes del usuario (comprueba que no había nada previamente):")
execute(GET)

#Creacion de un fichero
url = "http://localhost:" + port_file + "/file/create"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token  
}
data = {
    "uid": uid,
    "filename": "ejemplo.txt",
    "content": "Hola Mundo!"
}

print("Creación del fichero 'ejemplo.txt':")
execute(POST)


#Listado de ficheros del usuario
url = "http://localhost:" + port_file + "/file/list"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid
}

print("Listado de ficheros del usuario (comprobamos que se ha creado correctamente):")
execute(GET)

#Lectura del fichero
url = "http://localhost:" + port_file + "/file/read"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid,
    "filename": "ejemplo.txt",
}

print("Lectura del contenido de 'ejemplo.txt':")
execute(GET)

#Modificacion del fichero
url = "http://localhost:" + port_file + "/file/modify"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid,
    "filename": "ejemplo.txt",
    "content": "\nAdios Mundo!"
}

print("Modificación del fichero 'ejemplo.txt' añadiendo texto extra la final de fichero:")
execute(POST)

#Lectura del fichero
url = "http://localhost:" + port_file + "/file/read"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid,
    "filename": "ejemplo.txt",
}

print("Lectura del contenido de 'ejemplo.txt' (comprobamos que se ha modificado el fichero):")
execute(GET)

#Eliminación del fichero
url = "http://localhost:" + port_file + "/file/delete"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid, 
    "filename": "ejemplo.txt"
}

print("Eliminación del fichero 'ejemplo.txt':")
execute(DELETE)

#Listado de ficheros del usuario
url = "http://localhost:" + port_file + "/file/list"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
}
data = {
    "uid": uid
}

print("Listado de ficheros del usuario (comprobamos que se ha eliminado correctamente):")
execute(GET)

#Eliminación de usaurio
url = "http://localhost:" + port_user + "/user/delete"
headers = {"Content-Type": "application/json"}
data = {
    "nombre" : "usuario_ejemplo",
    "password" : "4321"
}

print("Eliminación del usuario:")
execute(DELETE)

#Login de usuario
url = "http://localhost:" + port_user + "/user/login"
headers = {"Content-Type": "application/json"}
data = {
    "nombre": "usuario_ejemplo",
    "password": "1234"
}

print("Login del usuario ejemplo (comprobamos que no existe con user:'usuario_ejemplo', password:'4321'):")
execute(POST)

print("FIN DE PRUEBAS")




    