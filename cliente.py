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