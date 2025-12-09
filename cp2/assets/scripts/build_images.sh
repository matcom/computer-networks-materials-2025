#!/bin/bash

echo "=== CONSTRUYENDO Y GUARDANDO IMÁGENES DOCKER ==="

# Crear directorio de imágenes si no existe
mkdir -p ../images

# Construir imágenes
echo "Construyendo imagen del router..."
sudo docker build -t router-img -f dockerfiles/router/Dockerfile .

echo "Construyendo imagen de host1..."
sudo docker build -t host1-img -f dockerfiles/host1/Dockerfile .

echo "Construyendo imagen de host2..."
sudo docker build -t host2-img -f dockerfiles/host2/Dockerfile .

# Guardar imágenes como archivos .tar
echo "Guardando imágenes como archivos .tar..."
sudo docker save -o ./images/router-img.tar router-img
sudo docker save -o ./images/host1-img.tar host1-img
sudo docker save -o ./images/host2-img.tar host2-img

# Verificar que los archivos se crearon
echo "Verificando creación de archivos:"
ls -la ../images/

echo "=== IMÁGENES GUARDADAS EN LA CARPETA 'images/' ==="
echo "Puedes copiar esta carpeta y usar load_images.sh para cargarlas"