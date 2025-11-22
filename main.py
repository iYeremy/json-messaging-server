from servidores import iniciar_servidor_guardado
from cliente import iniciar_cliente

def main():
    print("=== Sistema de Mensajes ===")
    print("1) Iniciar servidor")
    print("2) Iniciar cliente")
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        iniciar_servidor_guardado()
    elif opcion == "2":
        iniciar_cliente()
    else:
        print("opcion invalida :(")

if __name__ == "__main__":
    main()
