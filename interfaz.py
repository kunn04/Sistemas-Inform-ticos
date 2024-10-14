import requests, json

GET = 0
PUT = 1
POST = 2
DELETE = 3

port_user = "5080"
port_file = "5090"

users = 0
method = POST #default

com = ""

method = None

url = None
headers = {}
data = {}
content = ""
parts = []

uid = ""
token = ""
user = "" 
pwd = ""

commands = ['LOGIN', 'REGISTER', 'DELETEUSER', 'MODUSER', 'CREATEFILE', 'DELETEFILE', 'MODFILE', 'READFILE', 'LISTFILE', 'HELP', 'LOGOUT', 'EXIT']

user_input = ""

response = None

def fill_data(coms, command):
    global uid, token, port_file, port_user, content, url, headers, data

    if (command == "LOGIN"):    #LOGIN <USER> <PASSWORD>
        url = "http://localhost:" + port_user + "/user/login"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": str(coms[1]),
            "password": str(coms[2])
        }
    elif (command == "REGISTER"):    #REGISTER <USER> <PASSWORD>
        url = "http://localhost:" + port_user + "/user/create"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre": str(coms[1]),
            "password": str(coms[2])
        }
    elif (command == "CREATEFILE"):    #CREATEFILE <FILENAME> <UID> <TOKEN> --text <CONTENT> 
        url = "http://localhost:" + port_file + "/file/create"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token  
        }
        data = {
            "uid": uid,
            "filename": str(coms[1]),
            "content": str(content)
        }
    elif (command == "DELETEFILE"):    #DELETEFILE <FILENAME> <UID> <TOKEN>
        url = "http://localhost:" + port_file + "/file/delete"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
        data = {
            "uid": str(uid), 
            "filename": str(coms[1])
        }
    elif (command == "LISTFILE"):    #LISTFILE <UID> <TOKEN>
        url = "http://localhost:" + port_file + "/file/list"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
        data = {
            "uid": str(uid)
        }
    elif (command == "READFILE"):    #READFILE <FILENAME> <UID> <TOKEN>
        url = "http://localhost:" + port_file + "/file/read"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
        data = {
            "uid": str(uid),
            "filename": str(coms[1]),
        }
    elif (command == "DELETEUSER"):    #DELETEUSER <USER> <PASSWORD>
        url = "http://localhost:" + port_user + "/user/delete"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre" : str(coms[1]),
            "password" : str(coms[2])
        }
    elif (command == "MODUSER"):    #MODUSER <USER> <OLD_PASSWORD> <NEW_PASSWORD>

        url = "http://localhost:" + port_user + "/user/modify"
        headers = {"Content-Type": "application/json"}
        data = {
            "nombre" : str(coms[1]),
            "password_old" : str(coms[2]),
            "password_new" : str(coms[3])
        }
    elif (command == "MODFILE"):    #MODFILE <FILENAME> <UID> <TOKEN> --text <TEXT_TO_ADD>
        url = "http://localhost:" + port_file + "/file/modify"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        }
        data = {
            "uid": str(uid),
            "filename": str(coms[1]),
            "content": " " + content
        }

def execute(method):
    global url, headers, data

    if (method == POST):
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif (method == GET):
        response = requests.get(url, headers=headers, data=json.dumps(data))
    elif (method == DELETE):
        response = requests.delete(url, headers=headers, json=data)

    return response


def verify(string, num, filemode):
    global content

    try:
        string.split(' ')[num]
    except IndexError:
        return False
    else:
        if filemode:
            parts = string.split(' ')
            content = " ".join(parts[2:])            
        return True
    
def printv(string):
    print("\033[92m" + string + "\033[0m")

    
def extract_uid(response):
    global uid, token

    if response.text.split(':')[0] == 'ERROR':
        return False
    else:
        token = response.text.split('\n')[1].split(' ')[1]
        uid = response.text.split('\n')[0].split(' ')[1]
        return True


while True:
    if user != '':
        print("\033[94m" + user + ': ' + "\033[0m", end='')
    user_input = str(input("Introduzca un comando o help para ayuda: "))
    parts = user_input.split(' ')
    com = parts[0].upper()

    if com not in commands:
        print('COMANDOS DISPONIBLES:')
        print('LOGIN <USER> <PASSWORD> -- inicia sesión con una cuenta ya creada')
        print('REGISTER <USER> <PASSWORD> -- registra una nueva cuenta')
        print('MODUSER <USER> <PASSWORD_OLD> <PASSWORD_NEW> -- modifica la contraseña de un usuario')
        print('DELETEUSER <USER> <PASSWORD> -- borra un usuario')
        print('CREATEFILE <FILENAME> <CONTENT> -- crea un nuevo fichero')
        print('MODFILE <FILENAME> <ADDED_CONTENT> -- añade contenido a un fichero')
        print('DELETEFILE <FILENAME> -- borra un fichero')
        print('READFILE <FILENAME> -- lee el contenido de un fichero')
        print('LISTFILE -- lista los archivos de un usuario')
        print('LOGOUT -- cierra sesión de la cuenta actual')
        continue

    if com == 'LOGIN':
        if verify(user_input, 2, False) and user == '':
            user = parts[1]
            pwd = parts[2]

            fill_data(parts, com)
            response = execute(POST)

            if not extract_uid(response):
                printv('El usuario o contraseña no son correctos')
                user = ''
                pwd = ''
                continue
            else:
                printv('Bienvenido ' + user)
        elif user != '':
            printv("Cierre sesión antes de iniciar sesión con otra cuenta")
        else:
            printv("ERROR: \nUse: LOGIN <USER> <PASSWORD>")
            continue

    elif com == 'REGISTER':
        if verify(user_input, 2, False):
            fill_data(parts, com)
            response = execute(POST)
            printv(response.text)
        else:
            printv("ERROR: \nUse: REGISTER <USER> <PASSWORD>")
            continue
    elif com == 'MODUSER':
        if verify(user_input, 3, False):
            fill_data(parts, com)
            response = execute(POST)
            printv(response.text)
        else:
            printv("ERROR: \nUse: MODUSER <USER> <PASSWORD_OLD> <PASSWORD_NEW>")
            continue
    elif com == 'DELETEUSER':
        if verify(user_input, 2, False):
            fill_data(parts, com)
            response = execute(DELETE)
            printv(response.text)
        else:
            printv("ERROR: \nUse: DELETEUSER <USER> <PASSWORD>")
            continue
    elif com == 'CREATEFILE':
        if verify(user_input, 1, True) and user != '':
            fill_data(parts, com)
            response = execute(POST)
            print("\033[94m" + user + ': ' + "\033[0m", end='')
            printv(response.text)
            content = ''
        elif user == '':
            printv('Debes iniciar sesión primero')
        else:
            printv("ERROR: \nUse: CREATEFILE <FILENAME> <CONTENT>")
            continue
    elif com == 'MODFILE':
        if verify(user_input, 1, True) and user != '':
            fill_data(parts, com)
            response = execute(POST)
            print("\033[94m" + user + ': ' + "\033[0m", end='')
            printv(response.text)
            content = ''
        elif user == '':
            printv('Debes iniciar sesión primero')
        else:
            printv("ERROR: \nUse: MODFILE <FILENAME> <ADDED_CONTENT>")
            continue
    elif com == 'DELETEFILE':
        if verify(user_input, 1, True) and user != '':
            fill_data(parts, com)
            response = execute(DELETE)
            print("\033[94m" + user + ': ' + "\033[0m", end='')
            printv(response.text)
            content = ''
        elif user == '':
            printv('Debes iniciar sesión primero')
        else:
            printv("ERROR: \nUse: DELETEFILE <FILENAME>")
            continue
    elif com == 'READFILE':
        if verify(user_input, 1, True) and user != '':
            fill_data(parts, com)
            response = execute(GET)
            print("\033[94m" + user + ': ' + "\033[0m", end='')
            printv(response.text)
            content = ''
        elif user == '':
            printv('Debes iniciar sesión primero')
        else:
            printv("ERROR: \nUse: READFILE <FILENAME>")
            continue
    elif com == 'LISTFILE':
        if verify(user_input, 0, True) and user != '':
            fill_data(parts, com)
            response = execute(GET)
            print("\033[94m" + user + ': ' + "\033[0m", end='')
            printv(response.text)
            content = ''
        elif user == '':
            printv('Debes iniciar sesión primero')
        else:
            printv("ERROR: \nUse: LISTFILE")
            continue
    elif com == 'LOGOUT':
        if user == '':
            printv('No ha iniciado sesión con ninguna cuenta')
        else:
            user = ''
            pwd = ''
            uid = ''
            token = ''
            printv('Ha cerrado la sesión correctamente')
    elif com == 'HELP':
        print('COMANDOS DISPONIBLES:')
        print('LOGIN <USER> <PASSWORD> -- inicia sesión con una cuenta ya creada')
        print('REGISTER <USER> <PASSWORD> -- registra una nueva cuenta')
        print('MODUSER <USER> <PASSWORD_OLD> <PASSWORD_NEW> -- modifica la contraseña de un usuario')
        print('DELETEUSER <USER> <PASSWORD> -- borra un usuario')
        print('CREATEFILE <FILENAME> <CONTENT> -- crea un nuevo fichero')
        print('MODFILE <FILENAME> <ADDED_CONTENT> -- añade contenido a un fichero')
        print('DELETEFILE <FILENAME> -- borra un fichero')
        print('READFILE <FILENAME> -- lee el contenido de un fichero')
        print('LISTFILE -- lista los archivos de un usuario')
        print('LOGOUT -- cierra sesión de la cuenta actual')
    elif com == 'EXIT':
        exit()

        