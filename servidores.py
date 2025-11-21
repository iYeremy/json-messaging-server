"""
Servidor concurrente para registro de mensajes
Atiende multiples clientes simultaneamente usando hilos y json
"""

import socket
import threading
import json

