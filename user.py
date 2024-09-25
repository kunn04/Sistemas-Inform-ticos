from quart import Quart, jsonify, request
import os, uuid, hashlib

SECRET_UUID = uuid.UUID("00010203-0405-0607-0809-0a0b0c0d0e0f")

app = Quart(__name__)

def generar_token(uid):
    print(uid)
    hash = uuid.uuid5(SECRET_UUID, str(uid))
    return str(hash)

def user_already_exists(nombre):
    nom = ""
    with open('users.txt', 'r+') as f:
        for line in f:
            if line.split(":")[0] == nombre:
                return True
    return False

def uid_already_exists(uid):
    nom = ""
    with open('users.txt', 'r+') as f:
        for line in f:
            if line.split(":")[2] == uid:
                return True
    return False


@app.route('/home')
async def index():
    return 'Hello World'


@app.route('/user/create_user', methods = ['PUT', 'POST'])
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

    return user

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

@app.route('/user/create_file', methods = ['POST'])
async def create_file():
    datos = await request.get_json()
   
    
    print(datos)
    uid = datos.get('uid')
    filename = datos.get('filename')
    content = datos.get('content')
    auth = request.headers.get('Authorization')
    token = auth.split(" ")[1]

    if (uid_already_exists(uid) == False):
        return "ERROR: uid is not in the system, please register"

    if (generar_token(uid) != token):
        return "ERROR: auth failed"
    
    if os.path.exists(uid):
        path = os.path.join(uid + filename)
        with open(path, 'w') as f:
            f.write(content)
            return 'Fichero creado on exito'
    

    

if __name__ == "__main__":
    app.run(host='localhost', port=5050, debug=True)
    

