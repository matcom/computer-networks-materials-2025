#!/bin/bash

# Variables
NETWORK_1="network1"
NETWORK_2="network2"
ROUTER_CONTAINER="router"
HOST1_IMAGE="host1-img"
HOST2_IMAGE="host2-img"
ROUTER_IMAGE="router-img"

# Paso 1: Verificar y crear las redes Docker
echo "Verificando y creando redes Docker..."
if ! sudo docker network inspect $NETWORK_1 &>/dev/null; then
  sudo docker network create $NETWORK_1 --subnet=192.168.1.0/24
else
  echo "La red $NETWORK_1 ya existe."
fi

if ! sudo docker network inspect $NETWORK_2 &>/dev/null; then
  sudo docker network create $NETWORK_2 --subnet=192.168.2.0/24
else
  echo "La red $NETWORK_2 ya existe."
fi

# Paso 2: Verificar y construir las imágenes
echo "Verificando y construyendo imágenes..."
if ! sudo docker images --format "{{.Repository}}" | grep -q $HOST1_IMAGE; then
  echo "Construyendo imagen del host1..."
  sudo docker build -t $HOST1_IMAGE ./dockerfiles/host1
else
  echo "La imagen $HOST1_IMAGE ya existe."
fi

if ! sudo docker images --format "{{.Repository}}" | grep -q $HOST2_IMAGE; then
  echo "Construyendo imagen del host2..."
  sudo docker build -t $HOST2_IMAGE ./dockerfiles/host2
else
  echo "La imagen $HOST2_IMAGE ya existe."
fi

if ! sudo docker images --format "{{.Repository}}" | grep -q $ROUTER_IMAGE; then
  echo "Construyendo imagen del router..."
  sudo docker build -t $ROUTER_IMAGE ./router
else
  echo "La imagen $ROUTER_IMAGE ya existe."
fi

# Paso 3: Detener y eliminar contenedores existentes
sudo docker rm -f router host1 host2

# Paso 4: Iniciar el router
echo "Iniciando el router..."
sudo docker run -d --name $ROUTER_CONTAINER \
  --privileged \
  --network $NETWORK_1 \
  --ip 192.168.1.2 \
  $ROUTER_IMAGE

# Conectar el router a la red de clientes
sudo docker network connect $NETWORK_2 $ROUTER_CONTAINER --ip 192.168.2.2

# Paso 5: Iniciar los hosts
echo "Iniciando host1..."
HOST1_CONTAINER="host1"
sudo docker run -d --name $HOST1_CONTAINER \
    --privileged \
    --cap-add=NET_ADMIN \
    --network $NETWORK_1 \
    --ip 192.168.1.3 \
    $HOST1_IMAGE

echo "Iniciando host2..."
HOST2_CONTAINER="host2"
sudo docker run -d --name $HOST2_CONTAINER \
    --privileged \
    --cap-add=NET_ADMIN \
    --network $NETWORK_2 \
    --ip 192.168.2.3 \
    $HOST2_IMAGE


# Paso 8: Configurar enrutamiento
echo "Configurando enrutamiento para los hosts..."
sudo docker exec $HOST2_CONTAINER sh -c "ip route add 192.168.1.0/24 via 192.168.2.2"
sudo docker exec $HOST1_CONTAINER sh -c "ip route add 192.168.2.0/24 via 192.168.1.2"


echo "Configuración completada."