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

4. **Conectar a la base de datos PostgreSQL:**

   Utiliza el siguiente comando para conectarte a la base de datos:

   ```bash
   psql -h localhost -p 5432 -U alumnodb -d si1
   ```

5. **Ejecutar el scripts de actualización:**

   Ejecuta los scripts de actualización de la BBDD dentro de la base de datos:

   ```bash
   \i actualiza.sql

   \i actualizaCarrito.sql

   \i actualizaPrecios.sql

   \i actualizaTablas.sql

   \i pagado.sql
   ```

6. **Ejecutar la api:**

   Finalmente, ejecuta la api para poder enviar curls:

   ```bash
   python3 api.py
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
