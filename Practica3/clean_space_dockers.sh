#!/bin/bash

# Confirmación antes de proceder
read -p "Este script eliminará todos los contenedores detenidos, imágenes no utilizadas, volúmenes huérfanos y redes no usadas. ¿Deseas continuar? (s/n): " confirm

if [[ "$confirm" != "s" ]]; then
  echo "Operación cancelada."
  exit 0
fi

# Detener Docker si está en ejecución
echo "Deteniendo Docker..."
sudo systemctl stop docker

# Limpiar contenedores detenidos
echo "Eliminando contenedores detenidos..."
sudo docker container prune -f

# Limpiar imágenes no utilizadas
echo "Eliminando imágenes no utilizadas..."
sudo docker image prune -a -f

# Limpiar volúmenes no utilizados
echo "Eliminando volúmenes no utilizados..."
sudo docker volume prune -f

# Limpiar redes no utilizadas
echo "Eliminando redes no utilizadas..."
sudo docker network prune -f

# Limpiar sistema completo de Docker
echo "Limpiando todo lo no utilizado en Docker..."
sudo docker system prune -a -f

# Reiniciar Docker
echo "Reiniciando Docker..."
sudo systemctl start docker

echo "¡Limpieza completada con éxito!"
