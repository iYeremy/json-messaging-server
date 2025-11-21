"""
Servidor concurrente para registro de mensajes
Atiende multiples clientes simultaneamente usando hilos y json
"""

import socket
import threading
import json

HOST = "127.0.0.1" 
PORT = 50000