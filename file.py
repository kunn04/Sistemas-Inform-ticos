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
            if (line == "\n"):
                pass
            elif line.split(":")[2] == uid:
                return True
    return False


@app.route('/file/create_file', methods = ['POST'])
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
        path = os.path.join(uid + "/" + filename)
        with open(path, 'w') as f:
            f.write(content)
            return 'Fichero creado on exito'
        
@app.route('/file/delete_file', methods = ['POST'])
async def delete_file():
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
        path = os.path.join(uid + "/" + filename)
        if os.path.exists(path):
            os.remove(path)
            return "Archivo con nombre " + filename + " borrado con éxito"
        else:
            return "Archivo con nombre " + filename + " no existe"
        
@app.route('/file/list_file', methods = ['GET'])
async def list_file():
    datos = await request.get_json()
   
    
    print(datos)
    uid = datos.get('uid')
    auth = request.headers.get('Authorization')
    token = auth.split(" ")[1]

    if (uid_already_exists(uid) == False):
        return "ERROR: uid is not in the system, please register"

    if (generar_token(uid) != token):
        return "ERROR: auth failed"
    
    if os.path.exists(uid):
        return os.listdir(uid)
    

    

if __name__ == "__main__":
    app.run(host='localhost', port=5090, debug=True)