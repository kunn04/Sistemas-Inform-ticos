# Definimos la imagen base de python
FROM python:3.10

# Establecemos el directorio de trabajo del contenedor
WORKDIR /app

# Copia el archivo de dependencias para instalar las librerías necesarias de python
COPY requirements.txt ./

# Instala las dependencias de Python
RUN pip install --upgrade --no-cache-dir -r requirements.txt 

# Copia el código de la API dentro del contenedor
COPY . .

# Abre los puertos de escucha del contenedor
EXPOSE 5080

# Abre los puertos de escucha del contenedor
EXPOSE 5090

