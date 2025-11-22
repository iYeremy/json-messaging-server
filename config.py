"""
Configuración compartida entre servidor y cliente.
Define parámetros de red y límites del protocolo.
"""

HOST = "127.0.0.1"
PORT = 50000
MAX_MSG_LEN = 280  # máximo de caracteres permitidos por mensaje

# Colores ANSI
VERDE = "\033[32m"
AZUL = "\033[34m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
RESET = "\033[0m"
