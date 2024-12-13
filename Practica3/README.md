# Práctica 3: Sistemas Informáticos

## Descripción

Esta práctica consiste en la creación y gestión de una base de datos utilizando **PostgreSQL** y **MongoDB**, así como en la implementación de una **API REST** con **Flask** para interactuar con la base de datos. Se incluyen scripts automatizados para la creación y borrado del entorno virtual y de la base de datos, además de instrucciones para ejecutar la API y el cliente para probar todo el sistema.

## Requisitos

- **Docker** y **Docker Compose**
- **Python 3**
- **PostgreSQL**
- **MongoDB**
- **Flask**
- **pip**

## Instalación y Configuración

### 1. Crear el Entorno Virtual y Configurar Docker

Ejecutar el script `setup_venv.sh` para crear el entorno virtual, instalar las dependencias y configurar Docker:

Este script realiza las siguientes acciones:

- Crea un entorno virtual si no existe.
- Activa el entorno virtual.
- Instala las dependencias listadas en `requirements.txt`.
- Detiene cualquier instancia de PostgreSQL en ejecución.
- Construye y levanta los contenedores de Docker definidos en `compose.yml`.

### 2. Poblar la Base de Datos MongoDB desde PostgreSQL

Ejecutar el script `create_mongodb_from_postgresqldb.py` para poblar la base de datos **MongoDB** con datos extraídos de **PostgreSQL**:

Parámetros:

- `--city`: Nombre de la ciudad.
- `--commit`: (Opcional) Realiza un commit intermedio.
- `--incorrectOrder`: (Opcional) Borra en orden incorrecto.


### 3. Poblar la Base de Datos Neojdb desde PostgreSQL

Ejecutar el script `create_neo4jdb_from_postgresqldb.py` para poblar la base de datos **Neojdb** con datos extraídos de **PostgreSQL**:

Para acceder a ella, poner simplemente en el buscador: http://localhost:7474/browser/, que será en el puerto en el que se encuentre la conexión a la base de datos.

Para ejecutar las consultas de cypher, simplemente se pueden poner en la propia página.



### 4. Ejecutar la API

Ejecutar el script `api.py` para iniciar la **API REST** con **Flask**:

La API estará disponible en `http://127.0.0.1:5000`.

### 5. Probar la API con el Cliente

Ejecutar el script `client.py` para probar la API:

### 6. Borrar el Entorno Virtual y Detener Docker

Ejecutar el script `venv_down.sh` para borrar el entorno virtual y detener los contenedores de Docker:

Este script realiza las siguientes acciones:

- Detiene los contenedores de Docker.
- Borra el entorno virtual.

## Estructura del Proyecto

- `setup_venv.sh`: Script para configurar el entorno virtual y Docker.
- `venv_down.sh`: Script para borrar el entorno virtual y detener Docker.
- `requirements.txt`: Lista de dependencias de Python.
- `compose.yml`: Configuración de Docker Compose.
- `app/`: Directorio que contiene los scripts de la aplicación.
  - `create_mongodb_from_postgresqldb.py`: Script para poblar MongoDB desde PostgreSQL.
  - `mongodb_queries.py`: Script con consultas a MongoDB.
  - `api.py`: Implementación de la API REST con Flask.
  - `client.py`: Cliente para probar la API.
- `actualiza.sql`: Script SQL para actualizar restricciones en PostgreSQL.

## Notas

- Asegúrese de tener **Docker** y **Docker Compose** instalados y en ejecución.
- Verifique que los puertos definidos en `compose.yml` no estén en uso por otros servicios.
- Para detener la API, presione `Ctrl+C` en la terminal donde está ejecutando `api.py`.
