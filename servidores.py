"""
Servidor concurrente para registro de mensajes
Atiende multiples clientes simultaneamente usando hilos y json
"""

import socket
import threading
import json
import os # Para el caso en que exista otro server

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
        usuario = peticion.get("usuario")
        texto = peticion.get("mensaje")
        if not usuario or not texto:
            return {"estado":"error", "respuesta":"Solicitud incompleta"}
        nuevo = {"usuario":usuario, "mensaje":texto}
        with lock_mensajes:
            mensajes.append(nuevo)
            total = len(mensajes)
        print(f"[{nombre_hilo}] Mensaje registrado. Total acumulado: {total}")
        return {"estado":"ok", 
                "respuesta":"Mensaje registrado", 
                "total_mensajes": total
                }
    
    elif accion == "listar":
        with lock_mensajes:
            copia = list(mensajes) # copia de la lista global
        print(f"[{nombre_hilo}] Listando {len(copia)} mensajes")
        return {"estado":"ok", 
                "mensajes": copia
                }
    elif accion == "salir":
        print(f"[{nombre_hilo}] Cliente solicitó cerrar la sesión")
        return {"estado": "ok", "respuesta": "Sesión cerrada"}
    
    else:
        print(f"[{nombre_hilo}] Accion no reconocida: {accion}")
        return {"estado": "error", 
                "respuesta": f"Acción desconocida: {accion}"}

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

def inicializar_servidor():
    """
    Inicializa el socket del servidor (pasivo), escucha conexiones
    entrantes y crea un nuevo hilo para cada cliente aceptado
    """
    with socket.socket(IPV4, TCP) as servidor: # creacion de un socket de escucha
        servidor.bind((HOST, PORT)) # vincula a un IP y un PORT
        servidor.listen() # espera conexiones entrantes de clientes
        print(f"[+] Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = servidor.accept() # crea un nuevo canal para un cliente
            hilo = threading.Thread(target=manejar_cliente,
                                    args=(conn, addr),
                                    daemon=True
                                    )
            hilo.start()

def iniciar_servidor_guardado():
    if os.path.exists("server.lock"):
        print("[!] Ya hay un servidor iniciado.")
        return
    with open("server.lock", "w") as f:
        f.write("activo")
    try:
        inicializar_servidor()  # llama a tu funcion real del servidor
    finally:
        os.remove("server.lock")

if __name__ == "__main__":
    iniciar_servidor_guardado()