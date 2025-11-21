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

def manejar_cliente(direccion):
    """
    Gestiona la comunicacion con un cliente: recibe solicitudes json,
    las procesa (insert/list) y envia respuestas json
    """
    nombre_hilo = threading.current_thread().name
    print(f"[{nombre_hilo}] Sesion iniciada con {direccion}")