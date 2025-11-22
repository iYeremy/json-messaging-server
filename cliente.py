"""
Cliente interactivo para registro concurrente de mensajes
Se conecta a un servidor en HOST:PORT y utiliza json para 
enviar solicitudes de registro y consulta de mensajes, 
manejando respuestas y errores 
"""

import socket
import json
from config import HOST, PORT, MAX_MSG_LEN, VERDE, AZUL, ROJO, AMARILLO, RESET

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
        print(f"{ROJO}[CLIENTE] Error de comunicacion{RESET}")
        return None
    if not datos:
        print(f"{ROJO}[CLIENTE] El servidor cerro la conexion{RESET}")
        return None
    try:
        return json.loads(datos.decode("utf-8").strip())
    except Exception:
        print(f"{ROJO}[CLIENTE] La respuesta del servidor no es valida{RESET}")
        return None


def registrar_mensaje(conexion_cliente):
    """
    Solicita al usuario su nombre y mensaje, y los envia al servidor

    Args: conexion_cliente (socket): canal TCP conectado al servidor
    Retorna un bool donde indica si la operacion se ejecuto correctamente o no
    """
    print(f"{AZUL}Vas a registrar un mensaje, rellena los requisitos:{RESET}\n")
    usuario = input(f"{AZUL}Ingrese su nombre de usuario: {RESET}").strip()
    mensaje = input(f"{AZUL}Ingrese el mensaje a registrar (max {MAX_MSG_LEN} caracteres): {RESET}")
    if not usuario or not mensaje:
        print(f"{ROJO}[!] Nombre de usuario y mensaje obligatorios{RESET}")
        return True
    if len(mensaje) > MAX_MSG_LEN:
        print(f"{ROJO}[!] El mensaje excede el máximo permitido de {MAX_MSG_LEN} caracteres{RESET}")
        return True
    solicitud = {"accion":"registrar", "usuario":usuario, "mensaje": mensaje}
    respuesta = enviar(conexion_cliente, solicitud)
    if respuesta is None:
        return False

    if respuesta.get("estado") == "ok":
        print(f"{VERDE}[+] {respuesta.get('respuesta')}{RESET}")
        print(f"{VERDE}[#] Total mensajes: {respuesta.get('total_mensajes')}{RESET}")
    else:
        print(f"{ROJO}[!] Error: {respuesta.get('respuesta')}{RESET}")
    return True
    
def listar_mensajes(conexion_cliente):
    """
    Solicita al servidor la lista completa de mensajes almacenados

    Args: conexion_cliente (socket): conexion activa con el servidor
    Retorna un bool donde indica si se pudo listar o no
    """
    solicitud = {"accion":"listar"}
    respuesta = enviar(conexion_cliente, solicitud)
    if respuesta is None:
        return False
    if respuesta.get("estado") == "ok":
        mensajes = respuesta.get("mensajes", [])
        print(f"{AMARILLO}[/] Mensajes registrados: {RESET}")
        for msg in mensajes:
            usuario = msg.get("usuario", "anonimo")
            texto = msg.get("mensaje", "")
            print(f"{AMARILLO}- {usuario}: {texto}{RESET}")

    else:
        print(f"{ROJO}[!] Error: {respuesta.get('respuesta')}{RESET}")
    return True

def cerrar_conexion(conexion_cliente):
    """
    Intenta notificar al servidor el cierre de sesion y cerrar el socket

    Args: conexion_cliente(socket): conexion a cerrar
    """
    try:
        fin = {"accion":"salir"}
        conexion_cliente.sendall(json.dumps(fin).encode("utf-8"))
    except:
        pass

def mostrar_menu():
    """
    Despliegue del menu de opciones

    Retorna un (str) que sera la opcion seleccionada por el usuario
    """
    print(f"\n{AZUL}=== Menu Cliente ==={RESET}")
    print(f"{AZUL}1) Registrar mensaje{RESET}")
    print(f"{AZUL}2) Listar mensajes{RESET}")
    print(f"{AZUL}3) Salir{RESET}")
    return input(f"{AZUL}Seleccione una opcion: {RESET}").strip()

def iniciar_cliente():
    """
    Establece la conexion, muestra el menu y gestiona operaciones
    """
    print(f"{AMARILLO}[CLIENTE] Intentando conectar a {HOST}:{PORT}...{RESET}")
    try:
        conexion_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conexion_cliente.connect((HOST, PORT))
        print(f"{VERDE}[CLIENTE] Conexion establecida con el servidor.{RESET}")
    except Exception as e:
        print(f"{ROJO}[CLIENTE] No se pudo conectar: {e}{RESET}")
        return

    while True:
        opcion = mostrar_menu()
        if opcion == "1":
            if not registrar_mensaje(conexion_cliente):
                break
        elif opcion == "2":
            if not listar_mensajes(conexion_cliente):
                break
        elif opcion == "3":
            cerrar_conexion(conexion_cliente)
            break
        else:
            print(f"{ROJO}[!] Opcion invalida. Intente de nuevo :({RESET}")

    try:
        conexion_cliente.close()
    except Exception:
        pass
    print(f"{AMARILLO}[CLIENTE] Conexion finalizada.{RESET}")

if __name__ == "__main__":
    iniciar_cliente()
