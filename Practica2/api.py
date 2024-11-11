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

@app.route('/register', methods = ['POST'])
async def register():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    name = datos.get("name")
    address = datos.get("address")
    creditcard = datos.get("creditcard")

    if not email or not pwd or not name or not address or not creditcard:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email).first()

        if user:
            return jsonify({'message' : "Email already in use"}), 401

        new_user = Customer(email = email, password = pwd, name = name, address = address)
        session.add(new_user)
        session.commit()

        new_creditcard = CreditcardCustomer(customerid = new_user.customerid, creditcard = creditcard)
        session.add(new_creditcard)
        session.commit()

        return jsonify({'message' : "User registered successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/add_creditcard', methods = ['POST'])
async def add_creditcard():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    creditcard = datos.get("creditcard")

    if not email or not pwd or not creditcard:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        creditcard_user = session.query(CreditcardCustomer).filter_by(customerid = user.customerid, creditcard=creditcard).first()

        if creditcard_user:
            return jsonify({'message' : "Credit card already in use"}), 401
        
        new_creditcard = CreditcardCustomer(customerid = user.customerid, creditcard = creditcard)
        session.add(new_creditcard)
        session.commit()

        return jsonify({'message' : "Credit card added successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/delete_creditcard', methods = ['POST'])
async def delete_creditcard():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    creditcard = datos.get("creditcard")

    if not email or not pwd or not creditcard:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        creditcard_user = session.query(CreditcardCustomer).filter_by(customerid = user.customerid, creditcard=creditcard).first()

        if not creditcard_user:
            return jsonify({'message' : "Invalid credit card"}), 401
        
        session.delete(creditcard_user)
        session.commit()

        return jsonify({'message' : "Credit card deleted successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/add_to_cart', methods = ['POST'])
async def add_to_cart():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    productid = datos.get("productid")

    if not email or not pwd or not productid:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        product = session.query(Product).filter_by(productid = productid).first()

        if not product:
            return jsonify({'message' : "Invalid product"}), 401
        
        cart = session.query(Cart).filter_by(customerid = user.customerid, productid = productid).first()

        if cart:
            cart.quantity += 1
        else:
            new_cart = Cart(customerid = user.customerid, productid = productid, quantity = 1)
            session.add(new_cart)
        
        session.commit()

        return jsonify({'message' : "Product added to cart successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/delete_from_cart', methods = ['POST'])
async def delete_from_cart():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    productid = datos.get("productid")

    if not email or not pwd or not productid:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        product = session.query(Product).filter_by(productid = productid).first()

        if not product:
            return jsonify({'message' : "Invalid product"}), 401
        
        cart = session.query(Cart).filter_by(customerid = user.customerid, productid = productid).first()

        if cart:
            if cart.quantity > 1:
                cart.quantity -= 1
            else:
                session.delete(cart)
        
        session.commit()

        return jsonify({'message' : "Product deleted from cart successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/pay_cart', methods = ['POST'])
async def pay_cart():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")

    if not email or not pwd:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        cart = session.query(Cart).filter_by(customerid = user.customerid).all()

        total = 0
        for item in cart:
            product = session.query(Product).filter_by(productid = item.productid).first()
            total += product.price * item.quantity
            session.delete(item)
        
        user.balance -= total
        session.commit()

        return jsonify({'message' : "Cart paid successfully", 'balance' : user.balance}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


#FUNCIONES A IMPLEMENTAR (JJ): Login, Register, Añadir/eliminar tarjeta de credito, añadir saldo, añadir articulos al carrito, 
#eliminar articulos del carrito, pagar carrito
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=True)
