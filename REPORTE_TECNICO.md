# Reporte Técnico

## Integrantes
- Yeremy (código estudiantil no proporcionado)
- Asistente remoto de apoyo (sin código)

> Nota: en el informe final debemos actualizar los códigos exactos si la escuela los solicita.

## Propósito general
Construir un sistema sencillo de mensajería local para practicar sockets, JSON y concurrencia. La idea es que varias personas puedan mandar mensajes cortos a un servidor y luego consultarlos usando un cliente interactivo.

## Descripción del servidor
- El servidor (`servidores.py`) abre un socket TCP en `HOST` y `PORT` definidos en `config.py`.
- Cada nueva conexión se atiende en un hilo separado. Así, un cliente que se queda pensando no bloquea a los demás.
- Se guarda cada mensaje como un diccionario `{usuario, mensaje}` dentro de una lista en memoria protegida por un `Lock` para evitar condiciones de carrera.
- Las peticiones válidas son `registrar`, `listar` y `salir`. Las respuestas se envían siempre como JSON con un campo `estado`.
- Se agregó un límite global `MAX_MSG_LEN` para controlar el tamaño de los textos y mantener el servidor estable.
- Los colores ANSI declarados en `config.py` ayudan a leer los logs en tiempo real (azul informativo, verde exitoso, amarillo avisos y rojo errores/cierres).

## Descripción del cliente
- El cliente (`cliente.py`) también usa `config.py`, así que ambos comparten host, puerto y longitud máxima.
- Provee un menú simple con tres opciones: registrar, listar o salir. Todo se imprime con colores para distinguir estados.
- Al registrar, el cliente pide usuario y mensaje, valida el límite local y manda un JSON al servidor. Luego interpreta la respuesta y muestra el total acumulado.
- Al listar, pide la lista completa y formatea cada registro como `usuario: texto`.
- Cuando se sale, el cliente envía `{"accion": "salir"}` para que el servidor registre el cierre y después apaga el socket.

## Evidencias de ejecución

### Registro y listado exitoso
```
[CLIENTE] Intentando conectar a 127.0.0.1:50000...
[CLIENTE] Conexion establecida con el servidor.
=== Menu Cliente ===
1) Registrar mensaje
2) Listar mensajes
3) Salir
Seleccione una opcion: 1
... (se ingresan usuario y mensaje) ...
[+] Mensaje registrado
[#] Total mensajes: 3
=== Menu Cliente ===
Seleccione una opcion: 2
[/] Mensajes registrados:
- yeremy: holaaaaaaaaaaaa
- alice: hola server
- bob: segundo
```
Explicación: aquí se ve el flujo completo. El servidor acepta la conexión, el cliente registra mensajes y después lista todo el historial que vive en la memoria compartida.

### Validación por longitud
```
[CLIENTE] Intentando conectar a 127.0.0.1:50000...
[CLIENTE] Conexion establecida con el servidor.
=== Menu Cliente ===
Seleccione una opcion: 1
... (mensaje con más de 280 caracteres) ...
[!] El mensaje excede el máximo permitido de 280 caracteres
```
Explicación: el cliente detecta que el texto es muy grande, muestra el aviso y no llega a molestar al servidor. Así probamos el requisito del límite configurable.

## Preguntas de análisis

1. **¿Qué desafíos surgen al gestionar varias solicitudes simultáneas en un mismo servicio?**  
   Cuesta mantener los datos consistentes cuando dos clientes modifican la misma estructura al mismo tiempo. Sin un `Lock` o algo similar pueden aparecer carreras y mensajes mezclados.

2. **¿Cómo contribuye el uso de hilos a mejorar la capacidad de respuesta de un servicio?**  
   Cada hilo atiende a un cliente independiente, así que si alguien tarda en escribir o su conexión va lenta, los demás siguen siendo atendidos por sus propios hilos.

3. **¿Por qué es importante utilizar estructuras organizadas como JSON?**  
   Porque el cliente y el servidor necesitan un “idioma” claro. JSON es simple, legible y se convierte fácil a diccionarios en Python, lo que facilita validar y depurar.

4. **¿Qué mecanismos permiten identificar estructuras inválidas antes de procesarlas?**  
   Primero tratamos de parsear el texto con `json.loads` dentro de un `try/except`; si falla, respondemos con un error. Después revisamos que existan las claves obligatorias (`accion`, `usuario`, `mensaje`).

5. **¿Qué consideraciones deben tenerse al diseñar un sistema que almacena datos recibidos desde varias sesiones simultáneas?**  
   Hay que asegurar que el acceso a la estructura compartida sea atómico (locks), limitar tamaños para evitar desbordes, y decidir qué hacer si un cliente se cae en medio de una operación.

6. **¿Qué elementos serían necesarios para extender el servicio hacia almacenamiento persistente?**  
   Necesitaríamos una base de datos o al menos escribir en archivos. Además habría que definir cómo serializar cada mensaje, manejar migraciones y probablemente agregar índices o filtros para no leer todo en memoria cada vez.

---

Este reporte se basa en las pruebas y el código actual. Podemos ampliarlo con capturas reales y los códigos estudiantiles definitivos antes de entregar el taller.
