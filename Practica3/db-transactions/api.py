from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configuracion de la base de datos
DATABASE_URI = 'postgresql://alumnodb:1234@localhost:5432/si1'
engine = create_engine(DATABASE_URI, execution_options={"autocommit": False})
Session = sessionmaker(bind=engine)


@app.route('/borraCiudad', methods=['POST'])
def borra_ciudad_correcto():
    city = request.json.get('city')
    ordenincorrecto = request.json.get('ordenincorrecto')
    commitintermedio = request.json.get('commitintermedio')

    session = Session()
    try:
        # Verificar si hay clientes en la ciudad
        result = session.execute(
            text("SELECT COUNT(*) FROM customers WHERE city = :city"),
            {'city': city}
        ).scalar()

        if result == 0:
            return jsonify({"message": "No se encontraron clientes en la ciudad especificada."})

        if not ordenincorrecto:
            # Borrar en el orden correcto
            print("Deleting order details...")
            session.execute(text("DELETE FROM orderdetail WHERE orderid IN (SELECT orderid FROM orders WHERE customerid IN (SELECT customerid FROM customers WHERE city = :city))"), {'city': city})
            print("Deleted order details")
            print("Deleting orders...")
            session.execute(text("DELETE FROM orders WHERE customerid IN (SELECT customerid FROM customers WHERE city = :city)"), {'city': city})
            print("Deleted orders")
            print("Deleting customers...")
            session.execute(text("DELETE FROM customers WHERE city = :city"), {'city': city})
            print("Deleted customers")
        else:
            print("Deleting order details...")
            session.execute(text("DELETE FROM orderdetail WHERE orderid IN (SELECT orderid FROM orders WHERE customerid IN (SELECT customerid FROM customers WHERE city = :city))"), {'city': city})
            print("Deleted order details")
            
            if commitintermedio:
                session.commit()
                print("Intermediate commit")
                session.begin()
            
            print("Deleting customers...")
            session.execute(text("DELETE FROM customers WHERE city = :city"), {'city': city})
            print("Deleted customers")
            print("Deleting orders...")
            session.execute(text("DELETE FROM orders WHERE customerid IN (SELECT customerid FROM customers WHERE city = :city)"), {'city': city})
            print("Deleted orders")

        session.commit()
        print("Transaction committed")
        return jsonify({"message": "Clientes y su informacion asociada borrados correctamente."})

    except Exception as e:
        session.rollback()
        print("Transaction rolledback")
        return jsonify({"error": str(e)})

    finally:
        session.close()
        print("Session closed")


if __name__ == '__main__':
    app.run(debug=True)