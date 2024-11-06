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

5. **Ejecutar el script de actualización:**

   Finalmente, ejecuta el script `actualiza.sql` dentro de la base de datos:

   ```bash
   \i actualiza.sql
   ```

## Notas:

- Asegúrate de tener Docker y Docker Compose instalados y configurados correctamente en tu sistema.
- Este proyecto usa PostgreSQL en un contenedor Docker.
- El script `actualiza.sql` contiene las instrucciones necesarias para actualizar la base de datos después de levantar los contenedores.

