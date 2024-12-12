#!/bin/bash

# Nombre del entorno virtual
ENV_DIR="si1p3"

# Crear el entorno virtual si no existe
if [ ! -d "$ENV_DIR" ]; then
  echo "Creando entorno virtual..."
  python3 -m venv $ENV_DIR
else
  echo "El entorno virtual ya existe."
fi

# Activar el entorno virtual
source $ENV_DIR/bin/activate

# Instalar dependencias automáticamente
if [ -f "requirements.txt" ]; then
  echo "Instalando dependencias desde requirements.txt..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "Archivo requirements.txt no encontrado."
fi

#Ejecutar docker compose
sudo systemctl stop postgresql

sudo docker compose up --build

