import socket
import struct
import threading

# Configuración del grupo multicast
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# NODO COORDINADOR CENTRAL

def nodo_coordinador():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    print("[Coordinador] Esperando entrada de mensajes externos...")
    while True:
        msg = input("Mensaje externo >> ")
        # Atomicidad: envío único al grupo
        sock.sendto(msg.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
        print(f"[Coordinador] Mensaje enviado al grupo: {msg}")



# NODO MIEMBRO DEL GRUPO

def nodo_miembro(nombre):
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MCAST_PORT))  # Escuchar en el puerto multicast

    # Suscripción al grupo multicast
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[{nombre}] Unido al grupo {MCAST_GRP}:{MCAST_PORT}")
    while True:
        data, addr = sock.recvfrom(10240)
        print(f"[{nombre}] Mensaje recibido: {data.decode('utf-8')} desde {addr}")


if __name__ == "__main__":
    opcion = input("¿Ejecutar como (c)oordinador o (m)iembro? ")

    if opcion.lower() == "c":
        nodo_coordinador()
    else:
        nombre = input("Nombre del nodo: ")
        nodo_miembro(nombre)
