import requests
import json

BASE_URL = 'http://localhost:5080'  # Cambia esto a la URL de tu API

def register(email, password, username, address):
    url = f"{BASE_URL}/register"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "username": username,
        "address": address
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def login(email, password):
    url = f"{BASE_URL}/login"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def delete_creditcard(email, password, creditcard):
    url = f"{BASE_URL}/delete_creditcard"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "creditcard": creditcard
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def list_creditcards(email, password):
    url = f"{BASE_URL}/list_creditcards"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()



def add_to_cart(email, password, productid, quantity):
    url = f"{BASE_URL}/add_to_cart"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "productid": productid,
        "quantity": quantity
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def delete_from_cart(email, password, productid, quantity):
    url = f"{BASE_URL}/delete_from_cart"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "productid": productid,
        "quantity": quantity
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def add_creditcard(email, password, creditcard, expiration_date, cvv, cardholder):
    url = f"{BASE_URL}/add_creditcard"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "creditcard": creditcard,
        "exp_date": expiration_date,
        "cvv": cvv,
        "cardholder": cardholder
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def pay_cart(email, password, creditcard):
    url = f"{BASE_URL}/pay_cart"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "creditcard": creditcard
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def add_balance(email, password, balance, creditcard):
    url = f"{BASE_URL}/add_balance"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password,
        "balance": balance,
        "creditcard": creditcard
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def main():
    email = "example999@domain.com"
    password = "securepassword"
    creditcard = "1234567890123456"
    cvv = "123"
    cardholder = "John Doe"
    expiration_date = "2025-12-31"
    address = "Calle Falsa 123, Springfield"
    username = "John Doe"
    product_ids = [1, 2, 3]  # IDs de los productos a añadir al carrito
    product_id_delete = 3
    quantity = 1

    # REGISTRO
    result = register(email, password, username, address)
    print("Registro:", result)
    print()

    # LOGIN
    result = login(email, password)
    print("Login:", result)
    print()

    # AÑADIR TARJETA DE CRÉDITO
    result = add_creditcard(email, password, creditcard, expiration_date, cvv, cardholder)
    print("Añadir tarjeta de crédito:", result)
    print()

    # LISTAR TARJETAS DE CRÉDITO
    result = list_creditcards(email, password)
    print("Listar tarjetas de crédito:", result)
    print()

    # AÑADIR PRODUCTOS AL CARRITO
    for product_id in product_ids:
        result = add_to_cart(email, password, product_id, quantity)
        print(f"Añadir producto {product_id} al carrito:", result)
        print()

    # ELIMINAR PRODUCTOS DEL CARRITO
    result = delete_from_cart(email, password, product_id_delete, quantity)
    print(f"Eliminar producto {product_id_delete} del carrito:", result)
    print()
    
    # AÑADIR SALDO
    result = add_balance(email, password, 100, creditcard)
    print("Añadir saldo:", result)
    print()

    # PAGAR
    result = pay_cart(email, password, creditcard)
    print("Pagar carrito:", result)
    print()

    # ELIMINAR TARJETA DE CRÉDITO
    result = delete_creditcard(email, password, creditcard)
    print("Eliminar tarjeta de crédito:", result)
    print()

    # LISTAR TARJETAS DE CRÉDITO
    result = list_creditcards(email, password)
    print("Listar tarjetas de crédito:", result)
    print()

if __name__ == "__main__":
    main()