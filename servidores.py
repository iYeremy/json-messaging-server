"""
Servidor concurrente para registro de mensajes
Atiende multiples clientes simultaneamente usando hilos y json
"""

import socket
import threading
import json

HOST = "127.0.0.1" 
PORT = 50000

# estructura compartida para almacenar mensajes registrados
mensajes = [] # lista global, cada mensaje es un diccionario
lock_mensajes = threading.Lock() # asegura exclusion mutua al acceder a mensajes

def manejar_cliente(conexion, direccion):
    """
    Gestiona la comunicacion con un cliente: recibe solicitudes json,
    las procesa (insert/list) y envia respuestas json
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
                enviar_respuesta()
                continue
            respuesta = procesar_peticion(peticion, nombre_hilo)
            enviar_respuesta()
            pass 
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

def enviar_respuesta():
    pass

def iniciar_servidor():
    pass
