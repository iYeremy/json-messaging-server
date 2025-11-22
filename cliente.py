"""
Cliente interactivo para registro concurrente de mensajes
Se conecta a un servidor en HOST:PORT y utiliza json para 
enviar solicitudes de registro y consulta de mensajes, 
manejando respuestas y errores 
"""

import socket
import json

# PARAMETROS DE RED
HOST = "127.0.0.1" 
PORT = 50000

def enviar(conexion_cliente, paquete):
    """
    Serializa un objeto python a json y lo envia a traves del socket
    Luego recibe la respuesta del servidor, intenta descodificarla desde json
    y la retorna como diccionario de python

    Args: conexion_cliente (socket): conexion activa con el servidor
          paquete (dict): solicitud a enviar al servidor

    Retorna un (dict) con la respuesta decodificada o None si hay error
    """
    try:
        texto = json.dumps(paquete) + "\n"
        conexion_cliente.sendall(texto.encode("utf-8"))
        datos = conexion_cliente.recv(1024) # flujo de bits que se van a enviar
    except Exception as e:
        print("[CLIENTE] Error de comunicacion")
        return None
    if not datos:
        print("[CLIENTE] EL servidor cerro la conexion")
        return None
    try:
        return json.loads(datos.decode("utf-8").strip())
    except Exception:
        print("[CLIENTE] La respuesta del servidor no es valida")
        return None


def registrar_mensaje(conexion_cliente):
    """
    Solicita al usuario su nombre y mensaje, y los envia al servidor

    Args: conexion_cliente (socket): canal TCP conectado al servidor
    Retorna un bool donde indica si la operacion se ejecuto correctamente o no
    """
    print("Vas a registrar un mensaje, rellena los requisitos:" + "\n")
    usuario = input("Ingrese su nombre de usuario: ").strip()
    mensaje = input("Ingrese el mensaje a registrar")
    if not usuario or not mensaje:
        print("[!] Nombre de usuario y mensaje obligatorios")
        return True
    solicitud = {"accion":"registrar", "usuario":usuario, "mensaje": mensaje}
    respuesta = enviar(conexion_cliente, solicitud)
    if respuesta is None:
        return False
    if respuesta.get("estado" == "ok"):
        print(f"[+] {respuesta.get('respuesta')}")
        print(f"[#] Total mensajes: {respuesta.get('total_mensajes')}")
    else:
        print(f"[X] Error: {respuesta.get('respuesta')}")
        return True
    
def listar_mensajes(conexion_cliente):
    """
    Solicita al servidor la lista completa de mensajes almacenados

    Args: conexion_cliente (socket): conexion activa con el servidor
    Retorna un bool donde indica si se pudo listar o no
    """
    solicitud = {"accion":"listar"}
    respuesta = enviar(conexion_cliente, solicitud)
    

def cerrar_conexion(conexion_cliente):
    pass

def iniciar_cliente():
    pass
