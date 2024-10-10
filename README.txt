--------------------PARA INICIAR EL SERVICIO API--------------------
    1 -- Descomprmir carpeta zip

    2 -- Crear entorno virtual con: 

        mkdir -p venv/si1p1
        python3 -m venv venv/si1p1

    3 -- Activar el entorno virtual:

        source ./venv/si1p1/bin/activate

    4 -- Instalar las dependencias:

        pip install -r requirements.txt

    5 -- Activar el Docker:

        sudo docker-compose up

--------------------PARA PRUEBA AUTOMÁTICA--------------------

    1 -- Abrir otra terminal y ejecutar 'client.py':

        python3 client.py

--------------------PARA PRUEBA MANUAL CON INTERFAZ DE TEXTO--------------------

    1 -- Abrir otra terminal y ejecutar 'interfaz.py':

        python3 interfaz.py

    NOTAS: Esta es una interfaz dinámica con las funciones de login y logout para no tener que poner el token y uid contínuamente.

NOTAS EXTRA:
-- Los servicios user.py y file.py están localizados en los puertos 5080 y 5090 de 0.0.0.0 respectivamente


