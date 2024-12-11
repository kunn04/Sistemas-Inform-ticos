#!/bin/bash

#Nombre del entorno virtual
ENV_DIR="si1p3"

#Docker compose down
sudo docker compose down

#borrar el entorno virtual
sudo rm -rf $ENV_DIR

echo "Entorno virtual y Docker borrados"
