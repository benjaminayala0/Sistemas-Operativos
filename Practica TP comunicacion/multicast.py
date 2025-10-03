import socket
import struct
import sys

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

def nodo_miembro(nombre):
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', MCAST_PORT))  # Escucha en el puerto multicast

    # Unirse al grupo multicast
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"[{nombre}] Esperando mensajes en {MCAST_GRP}:{MCAST_PORT}...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[{nombre}] Recibido: {data.decode()} desde {addr}")


def enviar_mensaje(mensaje):
    # Crear socket UDP para enviar
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    sock.sendto(mensaje.encode(), (MCAST_GRP, MCAST_PORT))
    print(f"[ENVIADOR] Mensaje enviado: {mensaje}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python multicast.py (m nombreNodo | e mensaje)")
        sys.exit(1)

    if sys.argv[1] == "m":
        nodo_miembro(sys.argv[2])   # Ej: python multicast.py m Nodo1
    elif sys.argv[1] == "e":
        enviar_mensaje(sys.argv[2]) # Ej: python multicast.py e HolaGrupo
