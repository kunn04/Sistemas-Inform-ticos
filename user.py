from quart import Quart, jsonify, request
import os, uuid, hashlib

SECRET_UUID = "00010203-0405-0607-0809-0a0b0c0d0e0f"

app = Quart(__name__)

def generar_token(uid):
    hash = uuid.uuid5(SECRET_UUID, str(uid))
    return str(hash)

def user_already_exists(nombre):
    nom = ""
    with open('users.txt', 'r+') as f:
        for line in f:
            if line.split(":")[0] == nombre:
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
        os.mkdir(user)

    return user

@app.route('user/login', methods = ['PUT', 'POST'])
async def login():
    datos = await request.get_json()
    user = datos.get("nombre")
    pwd = datos.get("password")

    with open('users.txt', 'r') as f:
        for line in f:
            if line.split(":")[0] == user and line.split(":")[1] == pwd:
                return generar_token(line.split(":")[2])
    return "ERROR: User not found"

    

if __name__ == "__main__":
    app.run(host='localhost', port=5050, debug=True)
    

