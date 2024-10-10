from quart import Quart, jsonify, request
import os, uuid, hashlib, shutil

SECRET_UUID = uuid.UUID("00010203-0405-0607-0809-0a0b0c0d0e0f")

app = Quart(__name__)

def generar_token(uid):
    hash = uuid.uuid5(SECRET_UUID, str(uid))
    return str(hash)

def user_already_exists(nombre):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'users.txt')

    if not os.path.exists(file_path):
        with open('users.txt', 'w') as f:
            f.write('')
        

    with open('users.txt', 'r+') as f:
        for line in f:
            if line.split(":")[0] == nombre:
                return True
    return False

def uid_already_exists(uid):
    with open('users.txt', 'r+') as f:
        for line in f:
            if line.split(":")[2] == uid:
                return True
    return False


@app.route('/home')
async def index():
    return 'Hello World'


@app.route('/user/create', methods = ['PUT', 'POST'])
async def register():
    datos = await request.get_json()
    user = datos.get("nombre")
    pwd = datos.get("password")

    if user_already_exists(user):
        return "ERROR: Username already exists"

    uid = str(uuid.uuid4())

    with open('users.txt', 'a') as f:
        f.write('\n' + user + ':' + pwd + ':' + uid)
        os.mkdir(uid)

    return "usuario " + user + " creado con éxito"

@app.route('/user/login', methods = ['PUT', 'POST'])
async def login():
    datos = await request.get_json()
    user = datos.get("nombre")
    pwd = datos.get("password")

    with open('users.txt', 'r') as f:
        for line in f:
            if line.split(":")[0] == user and line.split(":")[1] == pwd:
                return "uid: " + line.split(':')[2] + "\ntoken: " + generar_token(line.split(":")[2])
    return "ERROR: User not found or incorrect password"

@app.route('/user/delete', methods = ['DELETE'])
async def delete_user():
    datos = await request.get_json()
    delete = False
    data = ""
    uid = ""
    
    user = datos.get("nombre")
    pwd = datos.get("password")

    if (user_already_exists(user) == False):
        return "ERROR: user is not in the system, please register"

    with open('users.txt', 'r') as f:
        for line in f:
            if line.split(":")[0] == user and line.split(":")[1] == pwd:
                delete = True
                uid = line.split(":")[2]
            else:
                data += line
    if delete:
        with open('users.txt', 'w') as f:
            f.write(data)
        
        if os.path.exists(uid):
            shutil.rmtree(uid)
        
        return "Usuario borrado con éxito"
    return "ERROR: User not found or incorrect password"

@app.route('/user/modify', methods = ['POST'])
async def modify():
    datos = await request.get_json()
    user = datos.get("nombre")
    pwd1 = datos.get("password_old")
    pwd2 = datos.get("password_new")
    data = ''
    found = False

    with open('users.txt', 'r') as f:
        for line in f:
            if line.split(":")[0] == user and line.split(":")[1] == pwd1:
                data += line.split(':')[0] + ":" + pwd2 + ":" + line.split(':')[2]
                found = True
            else:
                data += line
        if (found):
            with open('users.txt', 'w') as f:
                f.write(data)
            return "Contraseña modificada con éxito"
        else:
            return "ERROR: User not found or incorrect password"
    


    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=True)
    

