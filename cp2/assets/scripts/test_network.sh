#!/bin/bash

echo "=== PRUEBAS DE CONECTIVIDAD DE RED ==="

# Verificar que los contenedores están corriendo
if ! sudo docker ps | grep -q "router"; then
    echo "Error: Los contenedores no están corriendo. Ejecuta: ./setup_network.sh"
    exit 1
fi

# Pequeña pausa para asegurar que todo esté listo
sleep 2

# Prueba 1: Ping desde host1 a router
echo "1. Ping desde host1 al router (192.168.1.2):"
if sudo docker exec host1 ping -c 3 192.168.1.2; then
    echo "✓ OK"
else
    echo "✗ FAIL"
fi

# Prueba 2: Ping desde host2 a router
echo -e "\n2. Ping desde host2 al router (192.168.2.2):"
if sudo docker exec host2 ping -c 3 192.168.2.2; then
    echo "✓ OK"
else
    echo "✗ FAIL"
fi

# Prueba 3: Ping entre hosts (debería funcionar a través del router)
echo -e "\n3. Ping desde host1 a host2 (192.168.2.3):"
if sudo docker exec host1 ping -c 3 192.168.2.3; then
    echo "✓ OK"
else
    echo "✗ FAIL"
fi

# Prueba 4: Ping desde host2 a host1
echo -e "\n4. Ping desde host2 a host1 (192.168.1.3):"
if sudo docker exec host2 ping -c 3 192.168.1.3; then
    echo "✓ OK"
else
    echo "✗ FAIL"
fi

# Prueba 5: Verificar tablas de ruteo
echo -e "\n5. Tabla de rutas del router:"
sudo docker exec router ip route show

echo -e "\n6. Tabla de rutas de host1:"
sudo docker exec host1 ip route show

echo -e "\n7. Tabla de rutas de host2:"
sudo docker exec host2 ip route show

# Prueba 6: Verificar IP forwarding en router
echo -e "\n8. IP Forwarding en router:"
sudo docker exec router cat /proc/sys/net/ipv4/ip_forward

echo -e "\n=== PRUEBAS COMPLETADAS ==="