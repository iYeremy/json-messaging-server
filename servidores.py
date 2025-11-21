"""
Servidor concurrente para registro de mensajes
Atiende multiples clientes simultaneamente usando hilos y json
"""

import socket
import threading
import json

# PARAMETROS DE RED
HOST = "127.0.0.1" 
PORT = 50000

# ALIAS DE PROTOCOLOS
IPV4 = socket.AF_INET
TCP = socket.SOCK_STREAM

# BUFFER DE MENSAJES
mensajes = [] # lista global, cada mensaje es un diccionario

# CONTROL DE CONCURRENCIA
lock_mensajes = threading.Lock() # asegura exclusion mutua al acceder a mensajes

def manejar_cliente(conexion, direccion):
    """
    Gestiona la comunicacion con un cliente: recibe solicitudes json,
    las procesa (insert/list) y envia respuestas json
    Args: conexion(socket): socket conectado con el cliente
          direccion(tuple): direccion IP y puerto del cliente
    """
    nombre_hilo = threading.current_thread().name
    print(f"[{nombre_hilo}] Sesion iniciada con {direccion}")
    try:
        while True:
            data = conexion.recv(1024) # recibe y lee hasta 1024 bits en su flujo
            if not data: 
                break
            try:
                peticion = json.loads(data.decode("utf-8"))
                accion = peticion.get("accion","<sin accion>")
                print(f"[{nombre_hilo}] Accion recibida: {accion}")
            except json.JSONDecodeError:
                print(f"[{nombre_hilo}] Error: JSON invalido")
                enviar_respuesta(conexion, estado = "error", mensaje="Formato JSON invalido")
                continue
            respuesta = procesar_peticion(peticion, nombre_hilo)
            enviar_respuesta(conexion, **respuesta)
    except Exception as e:
        print(f"[{nombre_hilo}] Error inesperado: {e}")
    finally:
        conexion.close()
        print(f"[{nombre_hilo}] Conexion cerrada con {direccion}")

def procesar_peticion(peticion, nombre_hilo):
    """
    Procesa una peticion del cliente, ya validada como json
    Args: peticion (dict): diccionario con la accion solicitada y datos
          nombre_hilo (str): nombre del hilo que atiende al cliente

    Retorna un (dict) con una respuesta que contiene estado, mensaje y/o datos
    """

    accion = peticion.get("accion")

    if accion == "registrar":
        mensaje = peticion.get("mensaje")
        if not mensaje:
            return {"estado":"error", "mensaje":"Campo 'mensaje' requerido"}
        with lock_mensajes:
            mensajes.append(mensaje)
            total = len(mensajes)
        print(f"[{nombre_hilo}] Mensaje registrado. Total acumulado: {total}")
        return {"estado":"ok", "mensaje":"Mensaje registrado", "total": total}
    
    elif accion == "listar":
        with lock_mensajes:
            lista = mensajes.copy() # copia de la lista global
        print(f"[{nombre_hilo}] Listando {len(lista)} mensajes")
        return {"estado":"ok", "mensaje": lista}

    else:
        print(f"[{nombre_hilo}] Accion no reconocida: {accion}")
        return {"estado": "error", "mensaje": f"Acción desconocida: {accion}"}

def enviar_respuesta(conexion, **datos):
    """
    Envia una respuesta al cliente en forato json codificado en UTF-8
    Args: conexion (socket): socket activo con el cliente
          datos (dict): contenido de la respuesta a enviar
    """
    try:
        respuesta = json.dumps(datos).encode("utf-8")
        conexion.sendall(respuesta)

    except Exception as e: 
        print(f"[!] Error al enviar respuesta: {e}")

def iniciar_servidor(self):
    """
    Inicializa el socket del servidor (pasivo), escucha conexiones
    entrantes y crea un nuevo hilo para cada cliente aceptado
    """
    with socket.socket(IPV4, TCP) as servidor: # creacion de un socket de escucha
        servidor.bind((self.HOST, self.PORT)) # vincula a un IP y un PORT
        servidor.listen() # espera conexiones entrantes de clientes
        print(f"[+] Servidor escuchando en {self.HOST}:{self.PORT}")

        while True:
            conn, addr = servidor.accept() # crea un nuevo canal para un cliente
            hilo = threading.Thread(target=manejar_cliente,
                                    args={conn, addr}
                                    )
            hilo.start()
