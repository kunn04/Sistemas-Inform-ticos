import requests

BASE_URL = 'http://localhost:5000'  # Cambia esto a la URL de tu API

def add_to_cart(email, password, productid):
    url = f"{BASE_URL}/add_to_cart"
    data = {
        "email": email,
        "password": password,
        "productid": productid
    }
    response = requests.post(url, json=data)
    return response.json()

def delete_from_cart(email, password, productid):
    url = f"{BASE_URL}/delete_from_cart"
    data = {
        "email": email,
        "password": password,
        "productid": productid
    }
    response = requests.post(url, json=data)
    return response.json()

def add_creditcard(email, password, creditcard):
    url = f"{BASE_URL}/add_creditcard"
    data = {
        "email": email,
        "password": password,
        "creditcard": creditcard
    }
    response = requests.post(url, json=data)
    return response.json()

def main():
    email = "user@example.com"
    password = "securepassword"
    creditcard = "1234567890123456"
    product_ids = [1, 2, 3]  # IDs de los productos a añadir al carrito

    # Añadir tarjeta de crédito
    result = add_creditcard(email, password, creditcard)
    print(f"Adding credit card: {result}")

    # Añadir productos al carrito
    for productid in product_ids:
        result = add_to_cart(email, password, productid)
        print(f"Adding product {productid} to cart: {result}")

    # Eliminar productos del carrito (opcional)
    for productid in product_ids:
        result = delete_from_cart(email, password, productid)
        print(f"Deleting product {productid} from cart: {result}")

if __name__ == "__main__":
    main()