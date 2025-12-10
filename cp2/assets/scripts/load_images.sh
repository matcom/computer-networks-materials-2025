#!/bin/bash

echo "=== CARGANDO IMÁGENES DESDE ARCHIVOS .tar ==="

# Verificar que los archivos existen
if [ ! -f "../images/router-img.tar" ] || [ ! -f "../images/host1-img.tar" ] || [ ! -f "../images/host2-img.tar" ]; then
    echo "Error: No se encontraron los archivos .tar en la carpeta images/"
    echo "Ejecuta primero: ./build_images.sh"
    exit 1
fi

# Cargar imágenes
echo "Cargando imagen del router..."
sudo docker load -i ../images/router-img.tar

echo "Cargando imagen de host1..."
sudo docker load -i ../images/host1-img.tar

echo "Cargando imagen de host2..."
sudo docker load -i ../images/host2-img.tar

# Verificar que las imágenes se cargaron
echo "Imágenes cargadas:"
sudo docker images | grep -E "(router-img|host1-img|host2-img)"

echo "=== IMÁGENES CARGADAS EXITOSAMENTE ==="
echo "Ahora puedes ejecutar: ./setup_network.sh"