from quart import Quart, jsonify, request
import os, uuid, hashlib, shutil
import uuid
from sqlalchemy import *
from sqlalchemy.exc import *
from sqlalchemy.ext.asyncio import *
from sqlalchemy.orm import *
from sqlalchemy.future import *
from modelSQL import *
from datetime import datetime


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
    username = datos.get("username")
    address = datos.get("address")

    if not email or not pwd or not username or not address:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email).first()

        if user:
            return jsonify({'message' : "Email already in use"}), 401
        
        maxid = session.query(func.max(Customer.customerid)).scalar()

        new_user = Customer(customerid = maxid+1, email = email, password = pwd, username = username, address = address)
        session.add(new_user)
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
    exp_date_str = datos.get("exp_date")
    cvv = datos.get("cvv")
    cardholder = datos.get("cardholder")

    try:
        exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    if not email or not pwd or not creditcard or not exp_date or not cvv or not cardholder:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        creditcard_user = session.query(CreditcardCustomer).filter_by(customerid = user.customerid, creditcard=creditcard).first()

        if creditcard_user:
            return jsonify({'message' : "Credit card already registered by the user"}), 401
        
        new_creditcard = CreditcardCustomer(customerid = user.customerid, creditcard = creditcard, exp_date = exp_date, cvv = cvv, cardholder = cardholder)
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
            return jsonify({'message' : "Invalid creditcard"}), 401
        
        session.delete(creditcard_user)
        session.commit()
        
        return jsonify({'message' : "Credit card deleted successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/list_creditcards', methods = ['POST'])
async def list_creditcards():
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
        
        creditcards_user = session.query(CreditcardCustomer.creditcard).filter_by(customerid = user.customerid).all() #Lista de tuplas
        creditcards_list = [creditcard[0] for creditcard in creditcards_user] #Primer elemento de cada tupla

        if not creditcards_user:
            return jsonify({'message' : "No creditcards registered by the user"}), 401
        
        session.commit()
        
        return jsonify({'message' : creditcards_list}), 200

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
    quantity_str = datos.get("quantity")


    try:
        quantity = int(quantity_str)
    except ValueError:
        return jsonify({"error": "Quantity must be a number"}), 400


    if not email or not pwd or not productid or not quantity:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        product = session.query(Product).filter_by(prod_id = productid).first()

        if not product:
            return jsonify({'message' : "Invalid product id"}), 401
        
        inventory = session.query(Inventory).filter_by(prod_id = productid).first()

        if not inventory or inventory.stock < quantity:
            return jsonify({'message' : "Not enough stock for the quantity required"}), 401
        
        order = session.query(Order).filter_by(customerid = user.customerid, status = 'Processed').first()

        if not order:
            maxid = session.query(func.max(Order.orderid)).scalar()
            order = Order(orderid = maxid+1, customerid = user.customerid, orderdate = datetime.now(), tax = 15, status = 'Processed')
            session.add(order)

        orderDetail = session.query(OrderDetail).filter_by(orderid = order.orderid, prod_id = productid).first()

        if not orderDetail:
            newOrderDetail = OrderDetail(orderid = order.orderid, prod_id = productid, quantity = quantity, price = product.price)
            session.add(newOrderDetail)
        else:
            orderDetail.quantity += quantity

        
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
    quantity_str = datos.get("quantity")

    try:
        quantity = int(quantity_str)
    except ValueError:
        return jsonify({"error": "Quantity must be a number"}), 400


    if not email or not pwd or not productid or not quantity:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        order = session.query(Order).filter_by(customerid = user.customerid, status = 'Processed', ).first()

        if not order:
            return jsonify({'message' : "No cart for the user"}), 401

        orderDetail = session.query(OrderDetail).filter_by(orderid = order.orderid, prod_id = productid).first()

        if not orderDetail:
            return jsonify({'message' : "Product not in the cart"}), 401
        else:
            orderDetail.quantity -= quantity
            if orderDetail.quantity == 0:
                session.delete(orderDetail)

        session.commit()

        return jsonify({'message' : "Product deleted from the cart successfully"}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/pay_cart', methods = ['POST'])
async def pay_cart():
    datos = await request.get_json()
    email = datos.get("email")
    pwd = datos.get("password")
    creditcard = datos.get("creditcard")

    if not email or not pwd:
        return jsonify({"error": "Missing some data"}), 401

    session = Session()
    try:
        user = session.query(Customer).filter_by(email = email, password = pwd).first()

        if not user:
            return jsonify({'message' : "Invalid email or password"}), 401
        
        creditcard_user = session.query(CreditcardCustomer).filter_by(customerid = user.customerid, creditcard=creditcard).first()
        if not creditcard_user:
            return jsonify({'message' : "Invalid credit card"}), 401
        
        order = session.query(Order).filter_by(customerid = user.customerid, status = 'Processed').first()
        
        if not order:
            return jsonify({'message' : "No cart for the user"}), 401

        if user.balance < order.totalamount:
            return jsonify({'message' : "Insufficient balance"}), 401

        order.status = 'Paid'
        session.commit()

        return jsonify({'message' : "Cart paid successfully", 'balance' : user.balance}), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=True)
