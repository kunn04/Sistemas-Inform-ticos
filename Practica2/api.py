from quart import Quart, jsonify, request
import os, uuid, hashlib, shutil
import uuid
from sqlalchemy import *
from sqlalchemy.exc import *
from sqlalchemy.ext.asyncio import *
from sqlalchemy.orm import *
from sqlalchemy.future import *
from modelSQL import *


username = 'alumnodb'
password = '1234'
host = 'localhost'
port = '5432'
database = 'si1'

DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}'

app = Quart(__name__)

Session = sessionmaker(bind=engine)


@app.route('/login', methods = ['POST'])
async def login():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")

    if not email or not pwd:
        return jsonify({"error": "Missing email or password"}), 400

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if user:
            return jsonify({'message' : "Login Successful", 'customerid' : user.customerid}), 200
        else:
            return jsonify({'message' : "Invalid username or password"}), 401
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/add_balance', methods = ['POST'])
async def add_balance():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    balance = datos.get("balance")
    creditcard = datos.get("creditcard")

    try:
        intBalance = int(balance)
    except ValueError:
        return jsonify({"error": "Balance must be a number"}), 400

    if intBalance < 0:
        return jsonify({"error": "Balance can't be negative"}), 400

    if not email or not pwd or not balance or not creditcard:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        creditcard_user = session.query(CreditcardCustomer).filter_by(customerid = user.customerid, creditcard=creditcard).first()

        if not creditcard_user:
            return jsonify({'message' : "Invalid credit card"}), 401
        
        user.balance += intBalance
        session.commit()

        return {'message' : "Balance added successfully", 'balance' : user.balance}, 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


#FUNCIONES A IMPLEMENTAR (JJ): Login, Register, Añadir/eliminar tarjeta de credito, añadir saldo, añadir articulos al carrito, 
#eliminar articulos del carrito, pagar carrito
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=True)