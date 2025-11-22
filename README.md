# Sistema de Mensajes Concurrente

Este proyecto es un ejercicio para practicar sockets TCP, JSON y concurrencia con Python.
Cuenta con un servidor multi-hilo que guarda mensajes en memoria y un cliente interactivo
que permite registrar y listar mensajes desde la terminal.

## Requisitos previos

-   Python 3.13 o superior (ver `pyproject.toml`).
-   [uv](https://github.com/astral-sh/uv) para gestionar dependencias (opcional pero recomendado).

## Instalación y ejecución

1. Clona este repositorio y entra a la carpeta principal.
2. Crea (o activa) un entorno virtual con Python:
    ```bash
    python -m venv .venv
    source .venv/bin/activate        # En Windows: .venv\Scripts\activate
    ```
3. Instala dependencias desde `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
4. Ejecuta el servidor:
    ```bash
    python servidores.py
    ```
5. En otra terminal (con el mismo entorno activo) inicia el cliente:
    ```bash
    python cliente.py
    ```
6. (Opcional) Tambien se puede ejecutar el main para inicializar tanto UN SOLO servidor, como multiples clientes
   (con el mismo entorno activo)
   `bash
python main.py
`

> Si prefieres usar [uv](https://github.com/astral-sh/uv) también funciona: `uv sync`, `uv run python servidores.py`, etc. (ver sección de curiosidades).

## Archivos principales

-   `cliente.py`: interfaz de línea de comandos; muestra el menú, construye solicitudes JSON y presenta las respuestas con colores.
-   `servidores.py`: servidor TCP concurrente que maneja cada cliente en un hilo y almacena los mensajes en memoria protegida por un bloqueo.
-   `config.py`: variables compartidas (host, puerto, límite de caracteres y códigos ANSI).
-   `main.py`: menú simple para seleccionar entre iniciar el servidor o el cliente (opcional).
-   `REPORTE_TECNICO.md`: reporte del taller con evidencias y respuestas a las preguntas de análisis.

## Curiosidad: usando uv

De forma personal empecé a usar **uv** para manejar entornos y dependencias porque es rapidísimo:

```
uv sync               # crea el entorno e instala
uv run python ...     # ejecuta usando ese entorno
uv pip compile ...    # genera requirements.txt
```

No es obligatorio, pero lo dejo como alternativa muy buena por si alguien quiere probarla. Recomiendo ampliamente empezar a utilizarla, como se puede ver solamente con uv sync ya te gestiona muchas cosas de forma automatica, tambien permite crear esqueletos para diversos proyectos entre otras cosas que estoy explorando.

## Notas sobre archivos auxiliares

-   `pyproject.toml`: metadatos del proyecto y tolerancia de versiones de Python/dependencias.
-   `uv.lock`: archivo generado por `uv` con versiones exactas para reproducibilidad (no afecta si sólo usas pip).
-   `requirements.txt`: listado plano exportado desde `pyproject` para instalaciones tradicionales (`pip install -r requirements.txt`).

## Árbol de archivos

```text
.
├── cliente.py
├── config.py
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── REPORTE_TECNICO.md
├── servidores.py
└── uv.lock
```
