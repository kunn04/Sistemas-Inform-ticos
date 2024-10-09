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

6 -- Abrir otra terminal y ejecutar el client.py:

    python3 client.py

NOTAS EXTRA:
-- Los servicios user.py y file.py están localizados en los puertos 5080 y 5090 de localhost respectivamente


