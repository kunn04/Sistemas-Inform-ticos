# Instrucciones de Ejecución

Este proyecto utiliza PostgreSQL con Docker y requiere ejecutar algunos comandos para poner en marcha el sistema. A continuación se detallan los pasos necesarios:

## Pasos para ejecutar:

1. **Detener el servicio de PostgreSQL en el sistema:**

   ```bash
   sudo systemctl stop postgresql
   ```

2. **Apagar los contenedores de Docker (si están en ejecución):**

   ```bash
   sudo docker-compose down
   ```

3. **Levantar los contenedores de Docker:**

   ```bash
   sudo docker-compose up
   ```

4. **Conectar a la base de datos PostgreSQL (si1):**

   Utiliza el siguiente comando para conectarte a la base de datos:

   ```bash
   psql -h localhost -p 5432 -U alumnodb -d si1
   ```

5. **Ejecutar los scripts de actualización:**

   Ejecuta los scripts de actualización de la BBDD dentro de la base de datos:

   ```bash
   \i actualiza.sql

   \i actualizaPrecios.sql

   \i actualizaTablas.sql

   \i actualizaCarrito.sql

   \i pagado.sql
   ```

6. **Ejecutar la api:**

   Finalmente, ejecuta la api para poder enviar curls:

   ```bash
   python3 api.py
   ```

# OPTIMIZACIÓN:

1. **Conectar a la base de datos PostgreSQL (si2):**

   Utiliza el siguiente comando para conectarse a la base de datos:

   ```bash
   psql -h localhost -p 5433 -U alumnodb -d si2
   ```

2. **Ejecutar el script:**

   Ejecuta los scripts de actualización de la BBDD dentro de la base de datos:

   ```bash
   \i estadosDistintos.sql
   ```

## CURLS DE PRUEBA:

- **REGISTER:**

```bash
curl -X POST http://localhost:5080/register \
      -H "Content-Type: application/json" \
      -d '{
           "email": "example999@domain.com",
           "password": "securepassword",
           "username": "ExampleName",
           "address": "123 Main St"
         }'
```

- **LOGIN:**

```bash
curl -X POST http://localhost:5080/login \
   -H "Content-Type: application/json" \
   -d '{
         "email": "example999@domain.com",
         "password": "securepassword"
      }'
```

- **ADD CREDITCARD:**

```bash
curl -X POST http://localhost:5080/add_creditcard \
      -H "Content-Type: application/json" \
      -d '{
            "email": "example999@domain.com",
            "password": "securepassword",
            "creditcard": "1234567890123456",
            "exp_date": "2025-12-31",
            "cvv": "123",
            "cardholder": "Example Name"
         }'
```

- **LIST CREDITCARDS:**

```bash
curl -X POST http://localhost:5080/list_creditcards \
      -H "Content-Type: application/json" \
      -d '{
          "email": "example999@domain.com",
          "password": "securepassword"
         }'

```

- **ADD BALANCE:**

```bash
curl -X POST http://localhost:5080/add_balance \
      -H "Content-Type: application/json" \
      -d '{
            "email": "example999@domain.com",
            "password": "securepassword",
            "balance": "100",
            "creditcard": "1234567890123456"
         }'
```

- **ADD TO CART:**

```bash
curl -X POST http://localhost:5080/add_to_cart \
      -H "Content-Type: application/json" \
      -d '{
            "email": "example999@domain.com",
            "password": "securepassword",
            "productid": "1",
            "quantity": "6"
         }'
```

- **DELETE FROM CART:**

```bash
curl -X POST http://localhost:5080/delete_from_cart \
      -H "Content-Type: application/json" \
      -d '{
            "email": "example999@domain.com",
            "password": "securepassword",
            "productid": "1",
            "quantity": "3"
         }'
```

- **PAY CART:**

```bash
curl -X POST http://localhost:5080/pay_cart \
      -H "Content-Type: application/json" \
      -d '{
         "email": "example999@domain.com",
         "password": "securepassword",
         "creditcard": "1234567890123456"
      }'
```

- **DELETE CREDITCARD:**

```bash
curl -X POST http://localhost:5080/delete_creditcard \
      -H "Content-Type: application/json" \
      -d '{
         "email": "example999@domain.com",
         "password": "securepassword",
         "creditcard": "1234567890123456"
      }'
```

## Notas:

- Asegúrate de tener Docker y Docker Compose instalados y configurados correctamente en tu sistema.
- Este proyecto usa PostgreSQL en un contenedor Docker.
- El script `actualiza.sql` contiene las instrucciones necesarias para actualizar la base de datos después de levantar los contenedores.

```

```
